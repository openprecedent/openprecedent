from __future__ import annotations

import json
import sqlite3
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field

from openprecedent.schemas import (
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
    summary: str | None = None


class ConflictError(ValueError):
    pass


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
        summary = case.final_summary or self._build_case_summary(case, events, decisions)
        return ReplayResponse(case=case, events=events, decisions=decisions, summary=summary)

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
        return {
            "status": case.status.value,
            "has_file_write": event_types[EventType.FILE_WRITE.value] > 0,
            "has_recovery": decision_types[DecisionType.RETRY_OR_RECOVER.value] > 0,
            "tool_count": event_types[EventType.TOOL_CALLED.value],
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

        return score, similarities or ["similar case structure"], differences

    def _build_reusable_takeaway(self, case: Case, decisions: list[Decision]) -> str | None:
        if decisions:
            return decisions[-1].chosen_action
        if case.final_summary:
            return case.final_summary
        return None


def _string_or_none(value: object) -> str | None:
    if isinstance(value, str) and value.strip():
        return value
    return None


def _string_or_default(value: object, default: str) -> str:
    parsed = _string_or_none(value)
    return parsed or default
