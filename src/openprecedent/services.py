from __future__ import annotations

import json
import sqlite3
import shlex
import statistics
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import re
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from openprecedent.schemas import (
    Artifact,
    ArtifactType,
    Case,
    CaseStatus,
    Decision,
    DecisionExplanation,
    DecisionType,
    Event,
    EventActor,
    EventType,
    Precedent,
)
from openprecedent.storage import SQLiteStore


class CreateCaseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str | None = None
    title: str
    user_id: str | None = None
    agent_id: str | None = None


class AppendEventInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str | None = None
    event_type: EventType
    actor: EventActor
    timestamp: datetime | None = None
    parent_event_id: str | None = None
    sequence_no: int | None = None
    payload: dict[str, object] = Field(default_factory=dict)


class ReplayResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case: Case
    events: list[Event]
    decisions: list[Decision]
    artifacts: list[Artifact]
    summary: str | None = None


class ConflictError(ValueError):
    pass


class RuntimeTraceImportResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case: Case
    imported_events: list[Event]
    unsupported_record_type_counts: dict[str, int] = Field(default_factory=dict)


class OpenClawSessionReference(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    transcript_path: str
    updated_at: datetime | None = None
    label: str | None = None
    key: str | None = None
    model: str | None = None
    is_active: bool = False


class OpenClawCollectionState(BaseModel):
    model_config = ConfigDict(extra="forbid")

    imported_session_ids: list[str] = Field(default_factory=list)


class CollectedSessionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    transcript_path: str
    case_id: str
    title: str
    imported_event_count: int
    unsupported_record_type_counts: dict[str, int] = Field(default_factory=dict)


class OpenClawCollectionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    imported: list[CollectedSessionResult]
    skipped_session_ids: list[str] = Field(default_factory=list)
    state_path: str


class EvaluationCaseSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    title: str
    trace_path: str
    expected_decision_types: list[DecisionType]
    expected_precedent_case_ids: list[str] = Field(default_factory=list)


class EvaluationSuiteSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cases: list[EvaluationCaseSpec]


class EvaluationCaseResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    expected_decision_types: list[DecisionType]
    actual_decision_types: list[DecisionType]
    missing_decision_types: list[DecisionType]
    extra_decision_types: list[DecisionType]
    expected_precedent_case_ids: list[str]
    actual_precedent_case_ids: list[str]
    missing_precedent_case_ids: list[str]
    passed: bool


class EvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_cases: int
    passed_cases: int
    failed_cases: int
    results: list[EvaluationCaseResult]


class CollectedSessionEvaluationResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    case_id: str
    title: str
    transcript_path: str
    status: str
    event_count: int
    decision_count: int
    precedent_count: int
    top_precedent_case_id: str | None = None
    top_precedent_score: int | None = None
    has_file_write: bool = False
    has_recovery: bool = False
    final_summary: str | None = None
    unsupported_record_type_counts: dict[str, int] = Field(default_factory=dict)


class CollectedSessionEvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generated_at: datetime
    sessions_root: str
    state_path: str
    total_sessions: int
    evaluated_cases: int
    completed_cases: int
    failed_cases: int
    cases_with_precedents: int
    cases_with_file_writes: int
    cases_with_recovery: int
    average_event_count: float
    average_decision_count: float
    decision_type_counts: dict[str, int]
    unsupported_record_type_counts: dict[str, int] = Field(default_factory=dict)
    missing_session_ids: list[str] = Field(default_factory=list)
    results: list[CollectedSessionEvaluationResult]


@dataclass
class OpenPrecedentService:
    store: SQLiteStore

    @classmethod
    def from_path(cls, db_path: Path) -> "OpenPrecedentService":
        return cls(store=SQLiteStore(db_path))

    def create_case(self, payload: CreateCaseInput) -> Case:
        case_id = payload.case_id or f"case_{uuid4().hex[:12]}"
        case = Case(
            case_id=case_id,
            title=payload.title,
            status=CaseStatus.STARTED,
            user_id=payload.user_id,
            agent_id=payload.agent_id,
            started_at=datetime.now(UTC),
            ended_at=None,
            final_summary=None,
        )
        try:
            return self.store.create_case(case)
        except sqlite3.IntegrityError as error:
            raise ConflictError(f"case already exists: {case_id}") from error

    def list_cases(self) -> list[Case]:
        return self.store.list_cases()

    def get_case(self, case_id: str) -> Case | None:
        return self.store.get_case(case_id)

    def append_event(self, case_id: str, payload: AppendEventInput) -> Event:
        case = self.store.get_case(case_id)
        if case is None:
            raise KeyError(case_id)

        event = Event(
            event_id=payload.event_id or f"evt_{uuid4().hex[:12]}",
            case_id=case_id,
            event_type=payload.event_type,
            actor=payload.actor,
            timestamp=payload.timestamp or datetime.now(UTC),
            sequence_no=payload.sequence_no or self.store.next_event_sequence(case_id),
            parent_event_id=payload.parent_event_id,
            payload=payload.payload,
        )
        try:
            return self.store.append_event(event)
        except sqlite3.IntegrityError as error:
            raise ConflictError(
                f"event conflict for case {case_id}: event_id or sequence_no already exists"
            ) from error

    def import_events_jsonl(self, path: Path, default_case_id: str | None = None) -> list[Event]:
        imported: list[Event] = []
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                item = json.loads(stripped)
                case_id = item.get("case_id") or default_case_id
                if not isinstance(case_id, str) or not case_id:
                    raise ValueError(f"line {line_no}: case_id is required")
                normalized_item = dict(item)
                normalized_item.pop("case_id", None)
                payload = AppendEventInput.model_validate(normalized_item)
                imported.append(self.append_event(case_id, payload))
        return imported

    def import_openclaw_jsonl(
        self,
        path: Path,
        *,
        case_id: str,
        title: str,
        user_id: str | None = None,
        agent_id: str = "openclaw",
    ) -> RuntimeTraceImportResult:
        case = self.store.get_case(case_id)
        if case is None:
            case = self.create_case(
                CreateCaseInput(
                    case_id=case_id,
                    title=title,
                    user_id=user_id,
                    agent_id=agent_id,
                )
            )

        imported: list[Event] = []
        with path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                raw_item = json.loads(stripped)
                normalized = self._normalize_openclaw_trace_line(raw_item, line_no)
                imported.append(self.append_event(case_id, normalized))

        return RuntimeTraceImportResult(case=case, imported_events=imported)

    def list_openclaw_sessions(self, sessions_root: Path, limit: int = 10) -> list[OpenClawSessionReference]:
        references: list[OpenClawSessionReference] = []
        index_path = sessions_root / "sessions.json"
        if index_path.exists():
            entries = json.loads(index_path.read_text(encoding="utf-8"))
            for item in entries:
                session_id = _string_or_none(item.get("sessionId"))
                transcript_path = _string_or_none(item.get("sessionFile")) or _string_or_none(
                    item.get("transcriptPath")
                )
                if session_id is None or transcript_path is None:
                    continue
                resolved_path = Path(transcript_path)
                if not resolved_path.is_absolute():
                    resolved_path = sessions_root / resolved_path
                updated_at = _parse_epoch_millis(item.get("updatedAt"))
                references.append(
                    OpenClawSessionReference(
                        session_id=session_id,
                        transcript_path=str(resolved_path),
                        updated_at=updated_at,
                        label=_string_or_none(item.get("label")) or _string_or_none(item.get("displayName")),
                        key=_string_or_none(item.get("key")),
                        model=_string_or_none(item.get("model")),
                        is_active=bool(item.get("isActive", False)),
                    )
                )
        else:
            for transcript_path in sorted(sessions_root.glob("*.jsonl")):
                references.append(
                    OpenClawSessionReference(
                        session_id=transcript_path.stem,
                        transcript_path=str(transcript_path),
                        updated_at=datetime.fromtimestamp(
                            transcript_path.stat().st_mtime,
                            tz=UTC,
                        ),
                        label=transcript_path.stem,
                    )
                )

        references.sort(
            key=lambda item: (
                item.updated_at or datetime.fromtimestamp(0, tz=UTC),
                item.session_id,
            ),
            reverse=True,
        )
        return references[:limit]

    def import_openclaw_session(
        self,
        transcript_path: Path,
        *,
        case_id: str,
        title: str,
        user_id: str | None = None,
        agent_id: str = "openclaw",
    ) -> RuntimeTraceImportResult:
        case = self.store.get_case(case_id)
        if case is None:
            case = self.create_case(
                CreateCaseInput(
                    case_id=case_id,
                    title=title,
                    user_id=user_id,
                    agent_id=agent_id,
                )
            )

        imported: list[Event] = []
        unsupported_record_type_counts: Counter[str] = Counter()
        with transcript_path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                raw_item = json.loads(stripped)
                normalized_events, unsupported_record_type = self._normalize_openclaw_session_line(
                    raw_item,
                    line_no,
                    transcript_path=transcript_path,
                )
                if unsupported_record_type is not None:
                    unsupported_record_type_counts[unsupported_record_type] += 1
                for normalized in normalized_events:
                    imported.append(self.append_event(case_id, normalized))

        return RuntimeTraceImportResult(
            case=case,
            imported_events=imported,
            unsupported_record_type_counts=dict(sorted(unsupported_record_type_counts.items())),
        )

    def collect_openclaw_sessions(
        self,
        sessions_root: Path,
        *,
        state_path: Path,
        limit: int = 1,
        user_id: str | None = None,
        agent_id: str = "openclaw",
    ) -> OpenClawCollectionResult:
        references = self.list_openclaw_sessions(sessions_root, limit=200)
        state = self._load_openclaw_collection_state(state_path)
        seen = set(state.imported_session_ids)

        imported: list[CollectedSessionResult] = []
        skipped: list[str] = []

        for reference in references:
            if reference.session_id in seen:
                skipped.append(reference.session_id)
                continue
            result = self.import_openclaw_session(
                Path(reference.transcript_path),
                case_id=_case_id_for_openclaw_session(reference.session_id),
                title=reference.label or f"OpenClaw session {reference.session_id}",
                user_id=user_id,
                agent_id=agent_id,
            )
            imported.append(
                CollectedSessionResult(
                    session_id=reference.session_id,
                    transcript_path=reference.transcript_path,
                    case_id=result.case.case_id,
                    title=result.case.title,
                    imported_event_count=len(result.imported_events),
                    unsupported_record_type_counts=result.unsupported_record_type_counts,
                )
            )
            seen.add(reference.session_id)
            state.imported_session_ids.append(reference.session_id)
            if len(imported) >= limit:
                break

        self._write_openclaw_collection_state(state_path, state)
        return OpenClawCollectionResult(
            imported=imported,
            skipped_session_ids=skipped,
            state_path=str(state_path),
        )

    def evaluate_openclaw_fixture_suite(self, suite_path: Path) -> EvaluationReport:
        suite = EvaluationSuiteSpec.model_validate_json(suite_path.read_text(encoding="utf-8"))
        base_dir = suite_path.parent

        imported_case_ids: list[str] = []
        for case_spec in suite.cases:
            trace_path = (base_dir / case_spec.trace_path).resolve()
            self.import_openclaw_jsonl(
                trace_path,
                case_id=case_spec.case_id,
                title=case_spec.title,
            )
            self.extract_decisions(case_spec.case_id)
            imported_case_ids.append(case_spec.case_id)

        results: list[EvaluationCaseResult] = []
        for case_spec in suite.cases:
            actual_decisions = self.list_decisions(case_spec.case_id)
            actual_decision_types = [decision.decision_type for decision in actual_decisions]
            expected_decision_types = case_spec.expected_decision_types

            missing_decision_types = [
                item for item in expected_decision_types if item not in actual_decision_types
            ]
            extra_decision_types = [
                item for item in actual_decision_types if item not in expected_decision_types
            ]

            precedents = self.find_precedents(case_spec.case_id, limit=5)
            actual_precedent_case_ids = [precedent.case_id for precedent in precedents]
            missing_precedent_case_ids = [
                item
                for item in case_spec.expected_precedent_case_ids
                if item not in actual_precedent_case_ids
            ]

            passed = not missing_decision_types and not missing_precedent_case_ids
            results.append(
                EvaluationCaseResult(
                    case_id=case_spec.case_id,
                    expected_decision_types=expected_decision_types,
                    actual_decision_types=actual_decision_types,
                    missing_decision_types=missing_decision_types,
                    extra_decision_types=extra_decision_types,
                    expected_precedent_case_ids=case_spec.expected_precedent_case_ids,
                    actual_precedent_case_ids=actual_precedent_case_ids,
                    missing_precedent_case_ids=missing_precedent_case_ids,
                    passed=passed,
                )
            )

        passed_cases = sum(1 for result in results if result.passed)
        return EvaluationReport(
            total_cases=len(results),
            passed_cases=passed_cases,
            failed_cases=len(results) - passed_cases,
            results=results,
        )

    def evaluate_collected_openclaw_sessions(
        self,
        sessions_root: Path,
        *,
        state_path: Path,
        limit: int | None = None,
        user_id: str | None = None,
        agent_id: str = "openclaw",
    ) -> CollectedSessionEvaluationReport:
        state = self._load_openclaw_collection_state(state_path)
        imported_session_ids = set(state.imported_session_ids)
        references = self.list_openclaw_sessions(sessions_root, limit=max(len(imported_session_ids), 1_000))
        selected_references = [item for item in references if item.session_id in imported_session_ids]
        if limit is not None:
            selected_references = selected_references[:limit]

        decision_type_counts: Counter[str] = Counter()
        unsupported_record_type_counts: Counter[str] = Counter()
        results: list[CollectedSessionEvaluationResult] = []
        missing_session_ids: list[str] = []

        for reference in selected_references:
            case_id = _case_id_for_openclaw_session(reference.session_id)
            case = self.store.get_case(case_id)
            if case is None:
                import_result = self.import_openclaw_session(
                    Path(reference.transcript_path),
                    case_id=case_id,
                    title=reference.label or f"OpenClaw session {reference.session_id}",
                    user_id=user_id,
                    agent_id=agent_id,
                )
                case = import_result.case
            else:
                import_result = RuntimeTraceImportResult(
                    case=case,
                    imported_events=[],
                    unsupported_record_type_counts=self._summarize_unsupported_openclaw_session_record_types(
                        Path(reference.transcript_path)
                    ),
                )

            events = self.list_events(case_id)
            decisions = self.extract_decisions(case_id)
            precedents = self.find_precedents(case_id, limit=3)
            decision_type_counts.update(decision.decision_type.value for decision in decisions)
            unsupported_record_type_counts.update(import_result.unsupported_record_type_counts)

            results.append(
                CollectedSessionEvaluationResult(
                    session_id=reference.session_id,
                    case_id=case_id,
                    title=case.title,
                    transcript_path=reference.transcript_path,
                    status=case.status.value,
                    event_count=len(events),
                    decision_count=len(decisions),
                    precedent_count=len(precedents),
                    top_precedent_case_id=precedents[0].case_id if precedents else None,
                    top_precedent_score=precedents[0].similarity_score if precedents else None,
                    has_file_write=any(event.event_type == EventType.FILE_WRITE for event in events),
                    has_recovery=any(
                        decision.decision_type == DecisionType.RETRY_OR_RECOVER
                        for decision in decisions
                    ),
                    final_summary=case.final_summary,
                    unsupported_record_type_counts=import_result.unsupported_record_type_counts,
                )
            )

        selected_session_ids = {item.session_id for item in selected_references}
        for session_id in state.imported_session_ids:
            if session_id not in selected_session_ids:
                missing_session_ids.append(session_id)

        event_counts = [item.event_count for item in results]
        decision_counts = [item.decision_count for item in results]
        return CollectedSessionEvaluationReport(
            generated_at=datetime.now(UTC),
            sessions_root=str(sessions_root),
            state_path=str(state_path),
            total_sessions=len(state.imported_session_ids) if limit is None else len(selected_references),
            evaluated_cases=len(results),
            completed_cases=sum(1 for item in results if item.status == CaseStatus.COMPLETED.value),
            failed_cases=sum(1 for item in results if item.status == CaseStatus.FAILED.value),
            cases_with_precedents=sum(1 for item in results if item.precedent_count > 0),
            cases_with_file_writes=sum(1 for item in results if item.has_file_write),
            cases_with_recovery=sum(1 for item in results if item.has_recovery),
            average_event_count=statistics.fmean(event_counts) if event_counts else 0.0,
            average_decision_count=statistics.fmean(decision_counts) if decision_counts else 0.0,
            decision_type_counts=dict(sorted(decision_type_counts.items())),
            unsupported_record_type_counts=dict(sorted(unsupported_record_type_counts.items())),
            missing_session_ids=missing_session_ids,
            results=results,
        )

    def list_events(self, case_id: str) -> list[Event]:
        case = self.store.get_case(case_id)
        if case is None:
            raise KeyError(case_id)
        return self.store.list_events(case_id)

    def extract_decisions(self, case_id: str) -> list[Decision]:
        events = self.list_events(case_id)
        extracted: list[Decision] = []
        seen_plan = False

        for event in events:
            event_payload = event.payload
            if event.event_type == EventType.USER_CONFIRMED:
                extracted.append(
                    self._build_decision(
                        case_id=case_id,
                        decision_type=DecisionType.CLARIFY,
                        title="User confirmation recorded",
                        question="Did the user confirm a constraint or proposed next step?",
                        chosen_action="Continue with confirmed instruction",
                        evidence_event_ids=[event.event_id],
                        constraints=["User confirmation received"],
                        selection_reason="The user explicitly confirmed the next step or constraint.",
                        outcome=_string_or_none(event_payload.get("message")),
                        confidence=0.9,
                    )
                )
            elif event.event_type == EventType.MESSAGE_AGENT and not seen_plan:
                extracted.append(
                    self._build_decision(
                        case_id=case_id,
                        decision_type=DecisionType.PLAN,
                        title="Initial execution plan",
                        question="What path should the agent take first?",
                        chosen_action=_string_or_default(event_payload.get("message"), "Proceed with the first stated plan"),
                        evidence_event_ids=[event.event_id],
                        constraints=["Use the first explicit agent plan as the baseline path"],
                        selection_reason="The first substantive agent response usually establishes the initial execution path.",
                        outcome="Initial plan captured from agent response",
                        confidence=0.7,
                    )
                )
                seen_plan = True
            elif event.event_type == EventType.TOOL_CALLED:
                tool_name = _string_or_default(event_payload.get("tool_name"), "unknown_tool")
                extracted.append(
                    self._build_decision(
                        case_id=case_id,
                        decision_type=DecisionType.SELECT_TOOL,
                        title=f"Selected tool: {tool_name}",
                        question="Which tool should be used next?",
                        chosen_action=f"Use {tool_name}",
                        evidence_event_ids=[event.event_id],
                        constraints=["Prefer the tool explicitly chosen by the runtime"],
                        selection_reason=f"The runtime selected {tool_name} for the next operation.",
                        outcome=_string_or_none(event_payload.get("reason")),
                        confidence=0.8,
                    )
                )
            elif event.event_type == EventType.FILE_WRITE:
                file_path = _string_or_default(event_payload.get("path"), "unknown_path")
                extracted.append(
                    self._build_decision(
                        case_id=case_id,
                        decision_type=DecisionType.APPLY_CHANGE,
                        title=f"Applied file change: {file_path}",
                        question="Should the agent modify repository state?",
                        chosen_action=f"Write {file_path}",
                        evidence_event_ids=[event.event_id],
                        constraints=["File write indicates a committed repository change"],
                        selection_reason=f"The runtime wrote {file_path}, which marks an applied change decision.",
                        outcome=_string_or_none(event_payload.get("summary")),
                        confidence=0.85,
                    )
                )
            elif event.event_type == EventType.COMMAND_COMPLETED:
                exit_code = event_payload.get("exit_code")
                if isinstance(exit_code, int) and exit_code != 0:
                    extracted.append(
                        self._build_decision(
                            case_id=case_id,
                            decision_type=DecisionType.RETRY_OR_RECOVER,
                            title="Recovered from command failure",
                            question="How should execution proceed after a failing command?",
                            chosen_action="Inspect failure and choose a narrower recovery path",
                            evidence_event_ids=[event.event_id],
                            constraints=["Non-zero command exit indicates recovery is required"],
                            selection_reason="The command failed, so the next meaningful step is a recovery choice rather than normal continuation.",
                            outcome=_string_or_none(event_payload.get("stderr")) or f"exit_code={exit_code}",
                            confidence=0.9,
                        )
                    )
            elif event.event_type == EventType.CASE_COMPLETED:
                extracted.append(
                    self._build_decision(
                        case_id=case_id,
                        decision_type=DecisionType.FINALIZE,
                        title="Case finalized successfully",
                        question="Is the case ready to conclude?",
                        chosen_action="Return the final result",
                        evidence_event_ids=[event.event_id],
                        constraints=["Case completion event closes execution"],
                        selection_reason="The runtime emitted a completion event, so the case should be finalized successfully.",
                        outcome=_string_or_none(event_payload.get("summary")) or "Case completed",
                        confidence=0.95,
                    )
                )
            elif event.event_type == EventType.CASE_FAILED:
                extracted.append(
                    self._build_decision(
                        case_id=case_id,
                        decision_type=DecisionType.FINALIZE,
                        title="Case finalized with failure",
                        question="Should the case terminate with a failure outcome?",
                        chosen_action="Stop execution and surface failure",
                        evidence_event_ids=[event.event_id],
                        constraints=["Case failure event closes execution with an error state"],
                        selection_reason="The runtime emitted a failure event, so execution should stop and surface the failure.",
                        outcome=_string_or_none(event_payload.get("summary")) or "Case failed",
                        confidence=0.95,
                    )
                )

        numbered: list[Decision] = []
        for index, decision in enumerate(extracted, start=1):
            numbered.append(decision.model_copy(update={"sequence_no": index}))

        self.store.replace_decisions(case_id, numbered)
        return numbered

    def list_decisions(self, case_id: str) -> list[Decision]:
        case = self.store.get_case(case_id)
        if case is None:
            raise KeyError(case_id)
        return self.store.list_decisions(case_id)

    def replay_case(self, case_id: str) -> ReplayResponse:
        case = self.store.get_case(case_id)
        if case is None:
            raise KeyError(case_id)
        events = self.store.list_events(case_id)
        decisions = self.store.list_decisions(case_id)
        artifacts = self._derive_artifacts(case_id, events)
        summary = case.final_summary or self._build_case_summary(case, events, decisions)
        return ReplayResponse(case=case, events=events, decisions=decisions, artifacts=artifacts, summary=summary)

    def find_precedents(self, case_id: str, limit: int = 3) -> list[Precedent]:
        current_case = self.store.get_case(case_id)
        if current_case is None:
            raise KeyError(case_id)

        current_events = self.store.list_events(case_id)
        current_decisions = self.store.list_decisions(case_id)
        current_fingerprint = self._fingerprint(current_case, current_events, current_decisions)

        candidates: list[tuple[int, Precedent]] = []
        for other_case in self.store.list_cases():
            if other_case.case_id == case_id:
                continue
            other_events = self.store.list_events(other_case.case_id)
            other_decisions = self.store.list_decisions(other_case.case_id)
            other_fingerprint = self._fingerprint(other_case, other_events, other_decisions)
            score, similarities, differences = self._compare_fingerprints(
                current_fingerprint,
                other_fingerprint,
            )
            if score <= 0:
                continue
            candidates.append(
                (
                    score,
                    Precedent(
                        case_id=other_case.case_id,
                        title=other_case.title,
                        summary=self._build_case_summary(other_case, other_events, other_decisions),
                        similarity_score=score,
                        similarities=similarities,
                        differences=differences,
                        reusable_takeaway=self._build_reusable_takeaway(other_case, other_decisions),
                        historical_outcome=other_case.final_summary,
                    ),
                )
            )

        candidates.sort(key=lambda item: (-item[0], item[1].case_id))
        return [precedent for _, precedent in candidates[:limit]]

    def _build_decision(
        self,
        *,
        case_id: str,
        decision_type: DecisionType,
        title: str,
        question: str,
        chosen_action: str,
        evidence_event_ids: list[str],
        constraints: list[str],
        selection_reason: str,
        outcome: str | None,
        confidence: float,
    ) -> Decision:
        explanation = DecisionExplanation(
            goal=question,
            evidence=[f"event:{event_id}" for event_id in evidence_event_ids],
            constraints=constraints,
            selection_reason=selection_reason,
            result=outcome,
        )
        return Decision(
            decision_id=f"dec_{uuid4().hex[:12]}",
            case_id=case_id,
            decision_type=decision_type,
            title=title,
            question=question,
            chosen_action=chosen_action,
            alternatives=[],
            evidence_event_ids=evidence_event_ids,
            constraint_summary="; ".join(constraints) if constraints else None,
            requires_human_confirmation=False,
            outcome=outcome,
            confidence=confidence,
            explanation=explanation,
            sequence_no=0,
        )

    def _build_case_summary(self, case: Case, events: list[Event], decisions: list[Decision]) -> str:
        event_count = len(events)
        decision_count = len(decisions)
        return (
            f"{case.title}: {event_count} events, {decision_count} decisions, "
            f"status={case.status.value}"
        )

    def _fingerprint(self, case: Case, events: list[Event], decisions: list[Decision]) -> dict[str, object]:
        event_types = Counter(event.event_type.value for event in events)
        decision_types = Counter(decision.decision_type.value for decision in decisions)
        tool_names = sorted(
            {
                tool_name
                for event in events
                if (tool_name := _string_or_none(event.payload.get("tool_name"))) is not None
            }
        )
        file_paths = sorted(
            {
                Path(path).name
                for event in events
                if (path := _string_or_none(event.payload.get("path"))) is not None
            }
        )
        keywords = sorted(self._case_keywords(case, events, decisions))
        return {
            "status": case.status.value,
            "has_file_write": event_types[EventType.FILE_WRITE.value] > 0,
            "has_recovery": decision_types[DecisionType.RETRY_OR_RECOVER.value] > 0,
            "tool_count": event_types[EventType.TOOL_CALLED.value],
            "tool_names": tool_names,
            "file_paths": file_paths,
            "keywords": keywords,
            "decision_types": dict(decision_types),
        }

    def _compare_fingerprints(
        self,
        current: dict[str, object],
        other: dict[str, object],
    ) -> tuple[int, list[str], list[str]]:
        score = 0
        similarities: list[str] = []
        differences: list[str] = []

        for key in ("has_file_write", "has_recovery", "status"):
            if current[key] == other[key]:
                score += 2
                similarities.append(f"same {key}")
            else:
                differences.append(f"different {key}")

        current_decisions = current["decision_types"]
        other_decisions = other["decision_types"]
        if current_decisions == other_decisions:
            score += 3
            similarities.append("same decision shape")
        else:
            current_decision_keys = set(current_decisions)
            other_decision_keys = set(other_decisions)
            shared_decisions = sorted(current_decision_keys & other_decision_keys)
            if shared_decisions:
                score += min(len(shared_decisions), 3)
                similarities.append("shared decision types: " + ",".join(shared_decisions))
            else:
                differences.append("different decision shape")

        tool_delta = abs(int(current["tool_count"]) - int(other["tool_count"]))
        if tool_delta == 0:
            score += 2
            similarities.append("same tool call count")
        elif tool_delta == 1:
            score += 1
            similarities.append("nearby tool call count")
        else:
            differences.append("different tool call count")

        shared_tools = sorted(set(current["tool_names"]) & set(other["tool_names"]))
        if shared_tools:
            score += min(len(shared_tools), 2)
            similarities.append("shared tools: " + ",".join(shared_tools[:3]))
        else:
            differences.append("different tools")

        shared_paths = sorted(set(current["file_paths"]) & set(other["file_paths"]))
        if shared_paths:
            score += min(len(shared_paths), 2)
            similarities.append("shared file targets: " + ",".join(shared_paths[:3]))

        shared_keywords = sorted(set(current["keywords"]) & set(other["keywords"]))
        if shared_keywords:
            score += min(len(shared_keywords), 4)
            similarities.append("shared keywords: " + ",".join(shared_keywords[:4]))
        else:
            differences.append("different task keywords")

        return score, similarities or ["similar case structure"], differences

    def _case_keywords(self, case: Case, events: list[Event], decisions: list[Decision]) -> set[str]:
        texts: list[str] = [case.title]
        if case.final_summary:
            texts.append(case.final_summary)

        for event in events:
            for key in ("message", "path", "tool_name", "command"):
                value = _string_or_none(event.payload.get(key))
                if value:
                    texts.append(value)

        for decision in decisions:
            texts.append(decision.title)
            texts.append(decision.chosen_action)
            if decision.outcome:
                texts.append(decision.outcome)

        keywords: set[str] = set()
        for text in texts:
            keywords.update(_tokenize_keywords(text))
        return keywords

    def _build_reusable_takeaway(self, case: Case, decisions: list[Decision]) -> str | None:
        if decisions:
            return decisions[-1].chosen_action
        if case.final_summary:
            return case.final_summary
        return None

    def _derive_artifacts(self, case_id: str, events: list[Event]) -> list[Artifact]:
        derived: list[Artifact] = []
        seen_ids: set[str] = set()

        for event in events:
            payload = event.payload
            artifact: Artifact | None = None

            if event.event_type == EventType.FILE_WRITE:
                path = _string_or_none(payload.get("path"))
                if path:
                    artifact = Artifact(
                        artifact_id=f"artifact_{event.event_id}",
                        case_id=case_id,
                        artifact_type=ArtifactType.FILE,
                        uri_or_path=path,
                        summary=_string_or_none(payload.get("summary")),
                    )
            elif event.event_type == EventType.COMMAND_COMPLETED:
                command = _string_or_none(payload.get("command"))
                if command:
                    artifact = Artifact(
                        artifact_id=f"artifact_{event.event_id}",
                        case_id=case_id,
                        artifact_type=ArtifactType.COMMAND_OUTPUT,
                        uri_or_path=command,
                        summary=_string_or_none(payload.get("stdout"))
                        or _string_or_none(payload.get("stderr")),
                    )
            elif event.event_type in (EventType.MESSAGE_USER, EventType.MESSAGE_AGENT):
                message = _string_or_none(payload.get("message"))
                if message:
                    artifact = Artifact(
                        artifact_id=f"artifact_{event.event_id}",
                        case_id=case_id,
                        artifact_type=ArtifactType.MESSAGE,
                        uri_or_path=f"{event.event_type.value}:{event.event_id}",
                        summary=message,
                    )

            if artifact is None or artifact.artifact_id in seen_ids:
                continue

            self.store.upsert_artifact(artifact)
            seen_ids.add(artifact.artifact_id)
            derived.append(artifact)

        return derived

    def _normalize_openclaw_trace_line(
        self,
        raw_item: dict[str, object],
        line_no: int,
    ) -> AppendEventInput:
        kind = raw_item.get("kind")
        if not isinstance(kind, str) or not kind:
            raise ValueError(f"line {line_no}: kind is required for openclaw import")

        timestamp = self._parse_optional_timestamp(raw_item.get("timestamp"), line_no)
        event_id = _string_or_none(raw_item.get("event_id"))
        payload = dict(raw_item)
        payload.pop("kind", None)
        payload.pop("timestamp", None)
        payload.pop("event_id", None)

        if kind == "user_message":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.MESSAGE_USER,
                actor=EventActor.USER,
                timestamp=timestamp,
                payload={
                    "message": _string_or_default(raw_item.get("content"), ""),
                    "source": "openclaw",
                },
            )
        if kind == "agent_message":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.MESSAGE_AGENT,
                actor=EventActor.AGENT,
                timestamp=timestamp,
                payload={
                    "message": _string_or_default(raw_item.get("content"), ""),
                    "source": "openclaw",
                },
            )
        if kind == "tool_call":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.TOOL_CALLED,
                actor=EventActor.AGENT,
                timestamp=timestamp,
                payload={
                    "tool_name": _string_or_default(raw_item.get("tool_name"), "unknown_tool"),
                    "reason": _string_or_none(raw_item.get("reason")),
                    "arguments": raw_item.get("arguments") if isinstance(raw_item.get("arguments"), dict) else {},
                    "source": "openclaw",
                },
            )
        if kind == "tool_result":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.TOOL_COMPLETED,
                actor=EventActor.TOOL,
                timestamp=timestamp,
                payload=payload,
            )
        if kind == "command":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.COMMAND_COMPLETED,
                actor=EventActor.SYSTEM,
                timestamp=timestamp,
                payload={
                    "command": _string_or_default(raw_item.get("command"), ""),
                    "exit_code": int(raw_item.get("exit_code", 0)),
                    "stdout": _string_or_none(raw_item.get("stdout")),
                    "stderr": _string_or_none(raw_item.get("stderr")),
                    "source": "openclaw",
                },
            )
        if kind == "file_write":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.FILE_WRITE,
                actor=EventActor.AGENT,
                timestamp=timestamp,
                payload={
                    "path": _string_or_default(raw_item.get("path"), "unknown_path"),
                    "summary": _string_or_none(raw_item.get("summary")),
                    "source": "openclaw",
                },
            )
        if kind == "confirmation":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.USER_CONFIRMED,
                actor=EventActor.USER,
                timestamp=timestamp,
                payload={
                    "message": _string_or_default(raw_item.get("content"), ""),
                    "source": "openclaw",
                },
            )
        if kind == "completed":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.CASE_COMPLETED,
                actor=EventActor.SYSTEM,
                timestamp=timestamp,
                payload={
                    "summary": _string_or_none(raw_item.get("summary")) or "OpenClaw task completed",
                    "source": "openclaw",
                },
            )
        if kind == "failed":
            return AppendEventInput(
                event_id=event_id,
                event_type=EventType.CASE_FAILED,
                actor=EventActor.SYSTEM,
                timestamp=timestamp,
                payload={
                    "summary": _string_or_none(raw_item.get("summary")) or "OpenClaw task failed",
                    "source": "openclaw",
                },
            )

        raise ValueError(f"line {line_no}: unsupported openclaw kind '{kind}'")

    def _normalize_openclaw_session_line(
        self,
        raw_item: dict[str, object],
        line_no: int,
        *,
        transcript_path: Path,
    ) -> tuple[list[AppendEventInput], str | None]:
        record_type = raw_item.get("type")
        if not isinstance(record_type, str) or not record_type:
            raise ValueError(f"line {line_no}: type is required for openclaw session import")

        timestamp = self._parse_optional_timestamp(raw_item.get("timestamp"), line_no)
        record_id = _string_or_none(raw_item.get("id")) or f"session_line_{line_no}"
        parent_id = _string_or_none(raw_item.get("parentId"))

        if record_type == "session":
            return ([
                AppendEventInput(
                    event_id=f"evt_session_{record_id}",
                    event_type=EventType.CASE_STARTED,
                    actor=EventActor.SYSTEM,
                    timestamp=timestamp,
                    parent_event_id=parent_id,
                    payload={
                        "session_id": _string_or_default(raw_item.get("id"), transcript_path.stem),
                        "transcript_version": raw_item.get("version"),
                        "cwd": _string_or_none(raw_item.get("cwd")),
                        "source": "openclaw.session",
                    },
                )
            ], None)

        if record_type == "model_change":
            return ([
                AppendEventInput(
                    event_id=f"evt_model_{record_id}",
                    event_type=EventType.MODEL_COMPLETED,
                    actor=EventActor.SYSTEM,
                    timestamp=timestamp,
                    parent_event_id=parent_id,
                    payload={
                        "provider": _string_or_none(raw_item.get("provider")),
                        "model_id": _string_or_none(raw_item.get("modelId")),
                        "source": "openclaw.session",
                    },
                )
            ], None)

        if record_type != "message":
            return [], record_type

        message = raw_item.get("message")
        if not isinstance(message, dict):
            return [], None

        role = _string_or_none(message.get("role"))
        content = message.get("content")
        if not isinstance(content, list):
            content = []

        normalized_events: list[AppendEventInput] = []
        text_chunks = _extract_openclaw_text_segments(content)

        if role == "user":
            text = "\n".join(text_chunks).strip()
            if text:
                normalized_events.append(
                    AppendEventInput(
                        event_id=f"evt_message_{record_id}",
                        event_type=EventType.MESSAGE_USER,
                        actor=EventActor.USER,
                        timestamp=timestamp,
                        parent_event_id=parent_id,
                        payload={
                            "message": text,
                            "source": "openclaw.session",
                        },
                    )
                )
            return normalized_events, None

        if role == "assistant":
            visible_chunks = _extract_openclaw_visible_assistant_text(content)
            visible_text = "\n".join(visible_chunks).strip()
            if visible_text:
                normalized_events.append(
                    AppendEventInput(
                        event_id=f"evt_message_{record_id}",
                        event_type=EventType.MESSAGE_AGENT,
                        actor=EventActor.AGENT,
                        timestamp=timestamp,
                        parent_event_id=parent_id,
                        payload={
                            "message": visible_text,
                            "source": "openclaw.session",
                        },
                    )
                )

            for index, item in enumerate(content, start=1):
                if not isinstance(item, dict):
                    continue
                if item.get("type") != "toolCall":
                    continue
                tool_name = _string_or_default(item.get("name"), "unknown_tool")
                arguments = item.get("arguments") if isinstance(item.get("arguments"), dict) else {}
                tool_call_id = _string_or_none(item.get("id"))
                normalized_events.append(
                    AppendEventInput(
                        event_id=f"evt_tool_{record_id}_{index}",
                        event_type=EventType.TOOL_CALLED,
                        actor=EventActor.AGENT,
                        timestamp=timestamp,
                        parent_event_id=parent_id,
                        payload={
                            "tool_name": tool_name,
                            "arguments": arguments,
                            "tool_call_id": tool_call_id,
                            "source": "openclaw.session",
                        },
                    )
                )
                normalized_events.extend(
                    _normalize_openclaw_tool_call_events(
                        record_id=record_id,
                        index=index,
                        parent_id=parent_id,
                        timestamp=timestamp,
                        tool_name=tool_name,
                        tool_call_id=tool_call_id,
                        arguments=arguments,
                    )
                )
            return normalized_events, None

        if role == "toolResult":
            text = "\n".join(text_chunks).strip()
            normalized_events.append(
                AppendEventInput(
                    event_id=f"evt_tool_result_{record_id}",
                    event_type=EventType.TOOL_COMPLETED,
                    actor=EventActor.TOOL,
                    timestamp=timestamp,
                    parent_event_id=parent_id,
                    payload={
                        "tool_name": _string_or_none(message.get("toolName")),
                        "tool_call_id": _string_or_none(message.get("toolCallId")),
                        "content": text or None,
                        "is_error": bool(message.get("isError", False)),
                        "details": message.get("details") if isinstance(message.get("details"), dict) else {},
                        "source": "openclaw.session",
                    },
                )
            )
            normalized_events.extend(
                _normalize_openclaw_tool_result_events(
                    record_id=record_id,
                    parent_id=parent_id,
                    timestamp=timestamp,
                    tool_name=_string_or_none(message.get("toolName")),
                    tool_call_id=_string_or_none(message.get("toolCallId")),
                    text=text or None,
                    details=message.get("details") if isinstance(message.get("details"), dict) else {},
                )
            )
            return normalized_events, None

        return [], None

    def _summarize_unsupported_openclaw_session_record_types(
        self,
        transcript_path: Path,
    ) -> dict[str, int]:
        unsupported_record_type_counts: Counter[str] = Counter()
        with transcript_path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                raw_item = json.loads(stripped)
                _, unsupported_record_type = self._normalize_openclaw_session_line(
                    raw_item,
                    line_no,
                    transcript_path=transcript_path,
                )
                if unsupported_record_type is not None:
                    unsupported_record_type_counts[unsupported_record_type] += 1
        return dict(sorted(unsupported_record_type_counts.items()))

    def _load_openclaw_collection_state(self, state_path: Path) -> OpenClawCollectionState:
        if not state_path.exists():
            return OpenClawCollectionState()
        return OpenClawCollectionState.model_validate_json(state_path.read_text(encoding="utf-8"))

    def _write_openclaw_collection_state(
        self,
        state_path: Path,
        state: OpenClawCollectionState,
    ) -> None:
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            state.model_dump_json(indent=2),
            encoding="utf-8",
        )

    def _parse_optional_timestamp(self, value: object, line_no: int) -> datetime | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError(f"line {line_no}: timestamp must be an ISO-8601 string")
        return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _string_or_default(value: object, default: str) -> str:
    parsed = _string_or_none(value)
    return parsed or default


def _parse_epoch_millis(value: object) -> datetime | None:
    if isinstance(value, int):
        return datetime.fromtimestamp(value / 1000, tz=UTC)
    return None


def _tokenize_keywords(text: str) -> set[str]:
    tokens = {
        item
        for item in re.findall(r"[a-z0-9_./-]+", text.lower())
        if len(item) >= 3 and item not in _STOP_WORDS
    }
    expanded: set[str] = set()
    for token in tokens:
        expanded.add(token)
        if "/" in token or "." in token or "-" in token or "_" in token:
            expanded.update(
                part
                for part in re.split(r"[/._-]+", token)
                if len(part) >= 3 and part not in _STOP_WORDS
            )
    return expanded


def _extract_openclaw_text_segments(content: list[object]) -> list[str]:
    segments: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == "text":
            text = _string_or_none(item.get("text"))
            if text:
                segments.append(text)
        elif item_type == "thinking":
            thinking = _string_or_none(item.get("thinking"))
            if thinking:
                segments.append(thinking)
    return segments


def _extract_openclaw_visible_assistant_text(content: list[object]) -> list[str]:
    segments: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == "text":
            text = _string_or_none(item.get("text"))
            if text:
                segments.append(text)
        elif item_type == "thinking":
            summary = item.get("summary")
            if isinstance(summary, list):
                for part in summary:
                    if not isinstance(part, dict):
                        continue
                    if part.get("type") != "summary_text":
                        continue
                    text = _string_or_none(part.get("text"))
                    if text:
                        segments.append(text)
    return segments


def _normalize_openclaw_tool_call_events(
    *,
    record_id: str,
    index: int,
    parent_id: str | None,
    timestamp: datetime | None,
    tool_name: str,
    tool_call_id: str | None,
    arguments: dict[str, object],
) -> list[AppendEventInput]:
    if tool_name == "exec_command":
        command = _string_or_none(arguments.get("cmd"))
        if command is None:
            return []

        events = [
            AppendEventInput(
                event_id=f"evt_command_started_{record_id}_{index}",
                event_type=EventType.COMMAND_STARTED,
                actor=EventActor.AGENT,
                timestamp=timestamp,
                parent_event_id=parent_id,
                payload={
                    "command": command,
                    "tool_call_id": tool_call_id,
                    "source": "openclaw.session",
                },
            )
        ]
        for read_index, path in enumerate(_extract_file_reads_from_command(command), start=1):
            events.append(
                AppendEventInput(
                    event_id=f"evt_file_read_{record_id}_{index}_{read_index}",
                    event_type=EventType.FILE_READ,
                    actor=EventActor.AGENT,
                    timestamp=timestamp,
                    parent_event_id=parent_id,
                    payload={
                        "path": path,
                        "command": command,
                        "tool_call_id": tool_call_id,
                        "source": "openclaw.session",
                    },
                )
            )
        return events

    if tool_name == "apply_patch":
        patch_text = _string_or_none(arguments.get("patch"))
        if patch_text is None:
            return []
        paths = _extract_paths_from_apply_patch(patch_text)
        return [
            AppendEventInput(
                event_id=f"evt_file_write_{record_id}_{index}_{path_index}",
                event_type=EventType.FILE_WRITE,
                actor=EventActor.AGENT,
                timestamp=timestamp,
                parent_event_id=parent_id,
                payload={
                    "path": path,
                    "summary": "Modified via apply_patch",
                    "tool_call_id": tool_call_id,
                    "source": "openclaw.session",
                },
            )
            for path_index, path in enumerate(paths, start=1)
        ]

    if tool_name == "view_image":
        path = _string_or_none(arguments.get("path"))
        if path is None:
            return []
        return [
            AppendEventInput(
                event_id=f"evt_file_read_{record_id}_{index}_image",
                event_type=EventType.FILE_READ,
                actor=EventActor.AGENT,
                timestamp=timestamp,
                parent_event_id=parent_id,
                payload={
                    "path": path,
                    "tool_call_id": tool_call_id,
                    "source": "openclaw.session",
                },
            )
        ]

    return []


def _normalize_openclaw_tool_result_events(
    *,
    record_id: str,
    parent_id: str | None,
    timestamp: datetime | None,
    tool_name: str | None,
    tool_call_id: str | None,
    text: str | None,
    details: dict[str, object],
) -> list[AppendEventInput]:
    if tool_name != "exec_command":
        return []

    command = _string_or_none(details.get("cmd")) or _string_or_none(details.get("command"))
    exit_code = details.get("exit_code")
    normalized_exit_code = exit_code if isinstance(exit_code, int) else 0
    stderr = _string_or_none(details.get("stderr"))
    stdout = text
    # Preserve command completion for silent failures where OpenClaw records only an exit code.
    if stdout is None and stderr is None and not isinstance(exit_code, int):
        return []

    return [
        AppendEventInput(
            event_id=f"evt_command_completed_{record_id}",
            event_type=EventType.COMMAND_COMPLETED,
            actor=EventActor.SYSTEM,
            timestamp=timestamp,
            parent_event_id=parent_id,
            payload={
                "command": command or "exec_command",
                "exit_code": normalized_exit_code,
                "stdout": stdout,
                "stderr": stderr,
                "tool_call_id": tool_call_id,
                "source": "openclaw.session",
            },
        )
    ]


_STOP_WORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "will",
    "then",
    "case",
    "openclaw",
    "session",
    "docs",
    "file",
    "tool",
    "command",
    "agent",
}


def _case_id_for_openclaw_session(session_id: str) -> str:
    normalized = "".join(ch for ch in session_id.lower() if ch.isalnum())
    return f"openclaw_{normalized[:24]}"


def _extract_file_reads_from_command(command: str) -> list[str]:
    try:
        tokens = shlex.split(command)
    except ValueError:
        return []

    if not tokens:
        return []

    command_name = tokens[0]

    if command_name in {"cat", "head", "tail"}:
        return _dedupe_preserve_order(_extract_path_like_tokens(tokens[1:]))

    if command_name == "sed":
        return _dedupe_preserve_order(_extract_path_like_tokens(tokens[1:]))

    if command_name in {"rg", "grep"}:
        return _dedupe_preserve_order(_extract_search_command_paths(tokens[1:]))

    return []


def _extract_paths_from_apply_patch(patch_text: str) -> list[str]:
    paths: list[str] = []
    for raw_line in patch_text.splitlines():
        line = raw_line.strip()
        for prefix in ("*** Update File: ", "*** Add File: ", "*** Delete File: ", "*** Move to: "):
            if line.startswith(prefix):
                path = line.removeprefix(prefix).strip()
                if path:
                    paths.append(path)
    return _dedupe_preserve_order(paths)


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        deduped.append(value)
    return deduped


def _extract_path_like_tokens(tokens: list[str]) -> list[str]:
    paths: list[str] = []
    for token in tokens:
        if token.startswith("-"):
            continue
        if "/" not in token and "." not in Path(token).name:
            continue
        paths.append(token)
    return paths


def _extract_search_command_paths(tokens: list[str]) -> list[str]:
    paths: list[str] = []
    saw_pattern = False
    skip_next = False

    for token in tokens:
        if skip_next:
            skip_next = False
            continue

        if token in {"-g", "-e", "-f", "--glob", "--regexp", "--file"}:
            skip_next = True
            continue

        if token.startswith("-"):
            continue

        if not saw_pattern:
            saw_pattern = True
            continue

        if "/" not in token and "." not in Path(token).name:
            continue
        paths.append(token)

    return paths
