from __future__ import annotations

import json
import sqlite3
import shlex
import statistics
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
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
    source_format: str = "openclaw_trace"
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


class DecisionLineageQueryReason(StrEnum):
    INITIAL_PLANNING = "initial_planning"
    BEFORE_FILE_WRITE = "before_file_write"
    AFTER_FAILURE = "after_failure"
    MANUAL = "manual"


class DecisionLineageBriefInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_reason: DecisionLineageQueryReason
    task_summary: str
    current_plan: str | None = None
    candidate_action: str | None = None
    known_files: list[str] = Field(default_factory=list)
    limit: int = 3


class DecisionLineageMatchedCase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    title: str
    similarity_score: int
    summary: str


class DecisionLineageRelevantDecision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    decision_type: DecisionType
    title: str
    chosen_action: str
    outcome: str | None = None


class DecisionLineageBrief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    query_reason: DecisionLineageQueryReason
    task_summary: str
    suggested_focus: str | None = None
    matched_cases: list[DecisionLineageMatchedCase]
    task_frame: str | None = None
    accepted_constraints: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    rejected_options: list[str] = Field(default_factory=list)
    authority_signals: list[str] = Field(default_factory=list)
    cautions: list[str] = Field(default_factory=list)


class RuntimeDecisionLineageInvocation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    invocation_id: str
    recorded_at: datetime
    query_reason: DecisionLineageQueryReason
    task_summary: str
    current_plan: str | None = None
    candidate_action: str | None = None
    known_files: list[str] = Field(default_factory=list)
    case_id: str | None = None
    session_id: str | None = None


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
            raw_entries = json.loads(index_path.read_text(encoding="utf-8"))
            if isinstance(raw_entries, dict):
                entries = raw_entries.values()
            elif isinstance(raw_entries, list):
                entries = raw_entries
            else:
                entries = []
            for item in entries:
                if not isinstance(item, dict):
                    continue
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
        normalized_imports: list[AppendEventInput] = []
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
                normalized_imports.extend(normalized_events)

        session_id = _openclaw_session_id_from_import(
            normalized_imports,
            default=transcript_path.stem,
        )
        existing_case_id = self.store.find_case_id_by_openclaw_session_id(session_id)
        if existing_case_id is not None:
            existing_case = self.store.get_case(existing_case_id)
            if existing_case is None:
                raise KeyError(existing_case_id)
            return RuntimeTraceImportResult(
                case=existing_case,
                imported_events=[],
                unsupported_record_type_counts=dict(sorted(unsupported_record_type_counts.items())),
            )

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
        for normalized in normalized_imports:
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
        existing_case_ids = [
            case_spec.case_id for case_spec in suite.cases if self.store.get_case(case_spec.case_id) is not None
        ]
        if existing_case_ids:
            duplicated = ", ".join(sorted(existing_case_ids))
            raise ValueError(
                "fixture evaluation requires an isolated database; "
                f"existing evaluation case ids found: {duplicated}"
            )

        imported_case_ids: list[str] = []
        for case_spec in suite.cases:
            trace_path = (base_dir / case_spec.trace_path).resolve()
            if case_spec.source_format == "openclaw_trace":
                self.import_openclaw_jsonl(
                    trace_path,
                    case_id=case_spec.case_id,
                    title=case_spec.title,
                )
            elif case_spec.source_format == "openclaw_session":
                self.import_openclaw_session(
                    trace_path,
                    case_id=case_spec.case_id,
                    title=case_spec.title,
                )
            else:
                raise ValueError(
                    f"unsupported evaluation source_format '{case_spec.source_format}'"
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
                        event.event_type == EventType.COMMAND_COMPLETED
                        and isinstance(event.payload.get("exit_code"), int)
                        and int(event.payload.get("exit_code")) != 0
                        for event in events
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
        seen_task_frame = False
        prior_user_messages: list[str] = []

        for event in events:
            event_payload = event.payload
            if event.event_type == EventType.MESSAGE_USER:
                message = _string_or_none(event_payload.get("message"))
                is_new_user_intent = (
                    message is not None
                    and (
                        not prior_user_messages
                        or _normalize_message_intent(message)
                        != _normalize_message_intent(prior_user_messages[-1])
                    )
                )
                if message is not None and prior_user_messages and _is_meaningful_clarification(
                    message,
                    prior_user_messages[-1],
                ):
                    extracted.append(
                        self._build_decision(
                            case_id=case_id,
                            decision_type=DecisionType.CLARIFICATION_RESOLVED,
                            title="Task ambiguity resolved",
                            question="How did follow-up guidance change the task understanding?",
                            chosen_action=message,
                            evidence_event_ids=[event.event_id],
                            constraints=["Later user guidance can refine or narrow task understanding"],
                            selection_reason="A meaningful follow-up user message changed the task framing compared with the earlier request.",
                            outcome=message,
                            confidence=0.85,
                        )
                    )
                if message is not None and is_new_user_intent and _looks_like_constraint(message):
                    extracted.append(
                        self._build_decision(
                            case_id=case_id,
                            decision_type=DecisionType.CONSTRAINT_ADOPTED,
                            title="Constraint adopted",
                            question="What constraint or guardrail is now part of the task?",
                            chosen_action=message,
                            evidence_event_ids=[event.event_id],
                            constraints=["User-stated constraints should shape subsequent execution"],
                            selection_reason="The user message introduced or narrowed a concrete task constraint.",
                            outcome=message,
                            confidence=0.84,
                        )
                    )
                if message is not None and is_new_user_intent and _looks_like_success_criteria(message):
                    extracted.append(
                        self._build_decision(
                            case_id=case_id,
                            decision_type=DecisionType.SUCCESS_CRITERIA_SET,
                            title="Success criteria established",
                            question="What explicit standard now defines done or acceptable output?",
                            chosen_action=message,
                            evidence_event_ids=[event.event_id],
                            constraints=["The task should be evaluated against explicit success criteria"],
                            selection_reason="The user message made the expected output shape or acceptance bar explicit.",
                            outcome=message,
                            confidence=0.83,
                        )
                    )
                if message is not None and is_new_user_intent and _looks_like_option_rejection(message):
                    extracted.append(
                        self._build_decision(
                            case_id=case_id,
                            decision_type=DecisionType.OPTION_REJECTED,
                            title="Option rejected",
                            question="Which candidate path was explicitly ruled out?",
                            chosen_action=message,
                            evidence_event_ids=[event.event_id],
                            constraints=["Rejected options should remain out of scope"],
                            selection_reason="The message explicitly rejected one path in favor of a different direction.",
                            outcome=message,
                            confidence=0.82,
                        )
                    )
                if message is not None:
                    prior_user_messages.append(message)
            elif event.event_type == EventType.USER_CONFIRMED:
                extracted.append(
                    self._build_decision(
                        case_id=case_id,
                        decision_type=DecisionType.AUTHORITY_CONFIRMED,
                        title="Authority confirmed",
                        question="What approval or decision authority was confirmed?",
                        chosen_action=_string_or_default(
                            event_payload.get("message"),
                            "Continue within the approved boundary",
                        ),
                        evidence_event_ids=[event.event_id],
                        constraints=["Human confirmation established the allowed path forward"],
                        selection_reason="A user confirmation event signals explicit approval or authority for the chosen direction.",
                        outcome=_string_or_none(event_payload.get("message")),
                        confidence=0.9,
                    ).model_copy(update={"requires_human_confirmation": True})
                )
            elif event.event_type == EventType.MESSAGE_AGENT:
                message = _string_or_none(event_payload.get("message"))
                if message is None:
                    continue
                if not seen_task_frame and _looks_like_task_frame(message):
                    extracted.append(
                        self._build_decision(
                            case_id=case_id,
                            decision_type=DecisionType.TASK_FRAME_DEFINED,
                            title="Task frame established",
                            question="How is the task being framed for execution?",
                            chosen_action=message,
                            evidence_event_ids=[event.event_id],
                            constraints=["The first substantive agent framing sets the working interpretation of the task"],
                            selection_reason="The agent explicitly restated how it understood the task and what boundary it would operate within.",
                            outcome="Initial task frame captured from agent response",
                            confidence=0.7,
                        )
                    )
                    seen_task_frame = True
                if _looks_like_option_rejection(message):
                    extracted.append(
                        self._build_decision(
                            case_id=case_id,
                            decision_type=DecisionType.OPTION_REJECTED,
                            title="Alternative path rejected",
                            question="Which path did the agent explicitly decide not to pursue?",
                            chosen_action=message,
                            evidence_event_ids=[event.event_id],
                            constraints=["Explicitly rejected paths should remain out of scope"],
                            selection_reason="The agent message ruled out one approach while committing to another.",
                            outcome=message,
                            confidence=0.77,
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

    def build_decision_lineage_brief(
        self,
        input_data: DecisionLineageBriefInput,
    ) -> DecisionLineageBrief:
        query_tokens = self._decision_lineage_query_tokens(input_data)
        if not query_tokens:
            raise ValueError("decision-lineage brief requires non-empty task context")

        ranked_cases: list[tuple[int, Case, list[Event], list[Decision]]] = []
        for case in self.store.list_cases():
            events = self.store.list_events(case.case_id)
            decisions = self.store.list_decisions(case.case_id)
            if not decisions:
                continue

            case_keywords = self._case_keywords(case, events, decisions)
            decision_keywords = self._decision_keywords(decisions)
            semantic_overlap = query_tokens & decision_keywords
            contextual_overlap = query_tokens & case_keywords
            score = len(semantic_overlap) * 3 + len(contextual_overlap)
            if score <= 0:
                continue
            ranked_cases.append((score, case, events, decisions))

        ranked_cases.sort(key=lambda item: (-item[0], item[1].case_id))
        selected = ranked_cases[: max(1, input_data.limit)]

        matched_cases: list[DecisionLineageMatchedCase] = []
        relevant_decisions: list[DecisionLineageRelevantDecision] = []
        for score, case, events, decisions in selected:
            matched_cases.append(
                DecisionLineageMatchedCase(
                    case_id=case.case_id,
                    title=case.title,
                    similarity_score=score,
                    summary=self._build_case_summary(case, events, decisions),
                )
            )
            for decision in decisions:
                relevant_decisions.append(
                    DecisionLineageRelevantDecision(
                        case_id=case.case_id,
                        decision_type=decision.decision_type,
                        title=decision.title,
                        chosen_action=decision.chosen_action,
                        outcome=decision.outcome,
                    )
                )

        task_frame = _first_decision_text(relevant_decisions, DecisionType.TASK_FRAME_DEFINED)
        accepted_constraints = _decision_texts(relevant_decisions, DecisionType.CONSTRAINT_ADOPTED)
        success_criteria = _decision_texts(relevant_decisions, DecisionType.SUCCESS_CRITERIA_SET)
        rejected_options = _decision_texts(relevant_decisions, DecisionType.OPTION_REJECTED)
        authority_signals = _decision_texts(relevant_decisions, DecisionType.AUTHORITY_CONFIRMED)

        suggested_focus = (
            task_frame
            or (accepted_constraints[0] if accepted_constraints else None)
            or (success_criteria[0] if success_criteria else None)
        )
        cautions = [
            text
            for text in rejected_options + accepted_constraints
            if any(marker in _normalize_message_intent(text) for marker in ("do not", "don't", "instead of"))
        ][:3]

        return DecisionLineageBrief(
            query_reason=input_data.query_reason,
            task_summary=input_data.task_summary,
            suggested_focus=suggested_focus,
            matched_cases=matched_cases,
            task_frame=task_frame,
            accepted_constraints=accepted_constraints[:5],
            success_criteria=success_criteria[:5],
            rejected_options=rejected_options[:5],
            authority_signals=authority_signals[:5],
            cautions=cautions,
        )

    def record_runtime_decision_lineage_invocation(
        self,
        input_data: DecisionLineageBriefInput,
        *,
        log_path: Path,
        case_id: str | None = None,
        session_id: str | None = None,
    ) -> RuntimeDecisionLineageInvocation:
        invocation = RuntimeDecisionLineageInvocation(
            invocation_id=f"rtinv_{uuid4().hex[:12]}",
            recorded_at=datetime.now(UTC),
            query_reason=input_data.query_reason,
            task_summary=input_data.task_summary,
            current_plan=input_data.current_plan,
            candidate_action=input_data.candidate_action,
            known_files=input_data.known_files,
            case_id=case_id,
            session_id=session_id,
        )
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(invocation.model_dump_json())
            handle.write("\n")
        return invocation

    def list_runtime_decision_lineage_invocations(
        self,
        log_path: Path,
    ) -> list[RuntimeDecisionLineageInvocation]:
        if not log_path.exists():
            return []

        invocations: list[RuntimeDecisionLineageInvocation] = []
        with log_path.open("r", encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    invocations.append(RuntimeDecisionLineageInvocation.model_validate_json(stripped))
                except ValueError as error:
                    raise ValueError(
                        f"invalid runtime decision-lineage invocation log at line {line_no}"
                    ) from error
        return invocations

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
        file_read_paths = sorted(
            {
                Path(path).name
                for event in events
                if event.event_type == EventType.FILE_READ
                and (path := _string_or_none(event.payload.get("path"))) is not None
            }
        )
        keywords = sorted(self._case_keywords(case, events, decisions))
        decision_keywords = sorted(self._decision_keywords(decisions))
        return {
            "status": case.status.value,
            "has_file_write": event_types[EventType.FILE_WRITE.value] > 0,
            "has_recovery": any(
                event.event_type == EventType.COMMAND_COMPLETED
                and isinstance(event.payload.get("exit_code"), int)
                and int(event.payload.get("exit_code")) != 0
                for event in events
            ),
            "tool_count": event_types[EventType.TOOL_CALLED.value],
            "tool_names": tool_names,
            "file_paths": file_paths,
            "file_read_paths": file_read_paths,
            "keywords": keywords,
            "decision_keywords": decision_keywords,
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

        if current["status"] == other["status"]:
            score += 1
            similarities.append("same status")
        else:
            differences.append("different status")

        for key in ("has_file_write", "has_recovery"):
            if current[key] == other[key]:
                if current[key]:
                    score += 1
                    similarities.append(f"same {key}")
            else:
                differences.append(f"different {key}")

        current_decisions = current["decision_types"]
        other_decisions = other["decision_types"]
        if current_decisions == other_decisions:
            score += 6
            similarities.append("same decision shape")
        else:
            current_decision_keys = set(current_decisions)
            other_decision_keys = set(other_decisions)
            shared_decisions = sorted(current_decision_keys & other_decision_keys)
            if shared_decisions:
                score += min(len(shared_decisions) * 2, 6)
                similarities.append("shared decision types: " + ",".join(shared_decisions))
            else:
                differences.append("different decision shape")

        shared_decision_keywords = sorted(
            set(current["decision_keywords"]) & set(other["decision_keywords"])
        )
        if shared_decision_keywords:
            score += min(len(shared_decision_keywords) * 2, 8)
            similarities.append(
                "shared decision language: " + ",".join(shared_decision_keywords[:4])
            )
        else:
            differences.append("different decision language")

        tool_delta = abs(int(current["tool_count"]) - int(other["tool_count"]))
        if tool_delta == 0:
            score += 1
            similarities.append("same tool call count")
        elif tool_delta == 1:
            similarities.append("nearby tool call count")
        else:
            differences.append("different tool call count")

        shared_tools = sorted(set(current["tool_names"]) & set(other["tool_names"]))
        if shared_tools:
            score += 1
            similarities.append("shared tools: " + ",".join(shared_tools[:3]))
        else:
            differences.append("different tools")

        shared_paths = sorted(set(current["file_paths"]) & set(other["file_paths"]))
        if shared_paths:
            score += 1
            similarities.append("shared file targets: " + ",".join(shared_paths[:3]))

        shared_read_paths = sorted(set(current["file_read_paths"]) & set(other["file_read_paths"]))
        if shared_read_paths:
            score += min(len(shared_read_paths), 2)
            similarities.append("shared read targets: " + ",".join(shared_read_paths[:3]))

        shared_keywords = sorted(set(current["keywords"]) & set(other["keywords"]))
        if shared_keywords:
            score += min(len(shared_keywords), 4)
            similarities.append("shared keywords: " + ",".join(shared_keywords[:4]))
        else:
            differences.append("different task keywords")

        current_decision_keys = set(current["decision_types"])
        other_decision_keys = set(other["decision_types"])
        clarification_mismatch = DecisionType.CLARIFICATION_RESOLVED.value in (
            current_decision_keys ^ other_decision_keys
        )
        if clarification_mismatch:
            score -= 1
            differences.append("different clarification pattern")

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

    def _decision_keywords(self, decisions: list[Decision]) -> set[str]:
        keywords: set[str] = set()
        for decision in decisions:
            keywords.update(_tokenize_keywords(decision.title))
            keywords.update(_tokenize_keywords(decision.chosen_action))
            if decision.outcome:
                keywords.update(_tokenize_keywords(decision.outcome))
        return keywords

    def _decision_lineage_query_tokens(
        self,
        input_data: DecisionLineageBriefInput,
    ) -> set[str]:
        texts = [input_data.task_summary]
        if input_data.current_plan:
            texts.append(input_data.current_plan)
        if input_data.candidate_action:
            texts.append(input_data.candidate_action)
        texts.extend(input_data.known_files)

        tokens: set[str] = set()
        for text in texts:
            tokens.update(_tokenize_keywords(text))
        return tokens

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

        if record_type == "checkpoint":
            return ([
                AppendEventInput(
                    event_id=f"evt_checkpoint_{record_id}",
                    event_type=EventType.CHECKPOINT_SAVED,
                    actor=EventActor.SYSTEM,
                    timestamp=timestamp,
                    parent_event_id=parent_id,
                    payload={
                        "checkpoint_id": _string_or_default(raw_item.get("id"), record_id),
                        "status": _string_or_none(raw_item.get("status")),
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

        if record_type == "thinking_level_change":
            return ([
                AppendEventInput(
                    event_id=f"evt_thinking_level_{record_id}",
                    event_type=EventType.MODEL_INVOKED,
                    actor=EventActor.SYSTEM,
                    timestamp=timestamp,
                    parent_event_id=parent_id,
                    payload={
                        "thinking_level": _string_or_none(raw_item.get("thinkingLevel"))
                        or _string_or_none(raw_item.get("level")),
                        "changed_by": _string_or_none(raw_item.get("source")),
                        "trigger": _string_or_none(raw_item.get("trigger")),
                        "source": "openclaw.session",
                    },
                )
            ], None)

        if record_type == "custom":
            normalized_custom_event = _normalize_openclaw_custom_record(
                raw_item=raw_item,
                record_id=record_id,
                parent_id=parent_id,
                timestamp=timestamp,
            )
            if normalized_custom_event is None:
                return [], record_type
            return [normalized_custom_event], None

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
            text = _sanitize_openclaw_message_text("\n".join(text_chunks).strip())
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
            visible_text = _sanitize_openclaw_message_text("\n".join(visible_chunks).strip())
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


_OPENCLAW_NOISE_TAG_RE = re.compile(
    r"(?is)<(?P<tag>operator_policy|transport_metadata)>\s*.*?\s*</(?P=tag)>"
)
_OPENCLAW_NOISE_LINE_PREFIXES = (
    "operator policy",
    "transport metadata",
    "[operator policy]",
    "[transport metadata]",
)


def _sanitize_openclaw_message_text(text: str) -> str | None:
    cleaned = _OPENCLAW_NOISE_TAG_RE.sub("\n", text.replace("\r\n", "\n")).strip()
    if not cleaned:
        return None

    kept_lines: list[str] = []
    dropping_noise_block = False
    for raw_line in cleaned.splitlines():
        line = raw_line.strip()
        normalized = line.lower()
        if any(normalized.startswith(prefix) for prefix in _OPENCLAW_NOISE_LINE_PREFIXES):
            dropping_noise_block = True
            continue
        if dropping_noise_block:
            if not line:
                dropping_noise_block = False
            continue
        kept_lines.append(raw_line)

    sanitized = "\n".join(kept_lines).strip()
    return sanitized or None


def _is_meaningful_clarification(message: str, prior_message: str) -> bool:
    current = _normalize_message_intent(message)
    previous = _normalize_message_intent(prior_message)
    if not current or not previous:
        return current != previous
    if current == previous:
        return False

    current_tokens = _tokenize_keywords(current)
    previous_tokens = _tokenize_keywords(previous)
    if not current_tokens or not previous_tokens:
        return current != previous

    shared = current_tokens & previous_tokens
    overlap_ratio = len(shared) / min(len(current_tokens), len(previous_tokens))
    if overlap_ratio >= 0.8:
        return False
    return True


def _normalize_message_intent(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


_TASK_FRAME_PREFIXES = (
    "i will ",
    "i'll ",
    "i can ",
    "i found ",
    "i am going to ",
    "i'm going to ",
    "let me ",
)
_CONSTRAINT_MARKERS = (
    "focus on",
    "only ",
    "do not",
    "don't",
    "without ",
    "must ",
    "need to",
    "avoid ",
    "instead of",
)
_SUCCESS_CRITERIA_MARKERS = (
    "done when",
    "success means",
    "return ",
    "provide ",
    "give me",
    "output ",
    "summary ",
    "summarize ",
    "nothing else",
)
_OPTION_REJECTION_MARKERS = (
    "do not",
    "don't",
    "instead of",
    "rather than",
    "skip ",
)


def _looks_like_task_frame(message: str) -> bool:
    normalized = _normalize_message_intent(message)
    return normalized.startswith(_TASK_FRAME_PREFIXES) or " i will " in normalized


def _looks_like_constraint(message: str) -> bool:
    normalized = _normalize_message_intent(message)
    return any(marker in normalized for marker in _CONSTRAINT_MARKERS)


def _looks_like_success_criteria(message: str) -> bool:
    normalized = _normalize_message_intent(message)
    return any(marker in normalized for marker in _SUCCESS_CRITERIA_MARKERS)


def _looks_like_option_rejection(message: str) -> bool:
    normalized = _normalize_message_intent(message)
    return any(marker in normalized for marker in _OPTION_REJECTION_MARKERS)


def _decision_texts(
    decisions: list[DecisionLineageRelevantDecision],
    decision_type: DecisionType,
) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for decision in decisions:
        if decision.decision_type != decision_type:
            continue
        text = decision.outcome or decision.chosen_action
        normalized = _normalize_message_intent(text)
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        values.append(text)
    return values


def _first_decision_text(
    decisions: list[DecisionLineageRelevantDecision],
    decision_type: DecisionType,
) -> str | None:
    values = _decision_texts(decisions, decision_type)
    return values[0] if values else None


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


def _normalize_openclaw_custom_record(
    *,
    raw_item: dict[str, object],
    record_id: str,
    parent_id: str | None,
    timestamp: datetime | None,
) -> AppendEventInput | None:
    tool_name = (
        _string_or_none(raw_item.get("name"))
        or _string_or_none(raw_item.get("customType"))
        or _string_or_none(raw_item.get("event"))
    )
    details = raw_item.get("data")
    if not isinstance(details, dict):
        details = raw_item.get("details")
    normalized_details = details if isinstance(details, dict) else {}
    content = (
        _string_or_none(raw_item.get("text"))
        or _string_or_none(raw_item.get("summary"))
        or _string_or_none(raw_item.get("content"))
    )

    if tool_name is None and content is None and not normalized_details:
        return None

    return AppendEventInput(
        event_id=f"evt_custom_{record_id}",
        event_type=EventType.TOOL_COMPLETED,
        actor=EventActor.TOOL,
        timestamp=timestamp,
        parent_event_id=parent_id,
        payload={
            "tool_name": tool_name or "custom",
            "tool_call_id": _string_or_none(raw_item.get("toolCallId")),
            "content": content,
            "details": normalized_details,
            "source": "openclaw.session.custom",
        },
    )


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


def _openclaw_session_id_from_import(events: list[AppendEventInput], *, default: str) -> str:
    for event in events:
        if event.event_type != EventType.CASE_STARTED:
            continue
        session_id = _string_or_none(event.payload.get("session_id"))
        if session_id is not None:
            return session_id
    return default


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
