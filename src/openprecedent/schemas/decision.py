from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class DecisionType(StrEnum):
    TASK_FRAME_DEFINED = "task_frame_defined"
    CONSTRAINT_ADOPTED = "constraint_adopted"
    SUCCESS_CRITERIA_SET = "success_criteria_set"
    CLARIFICATION_RESOLVED = "clarification_resolved"
    OPTION_REJECTED = "option_rejected"
    AUTHORITY_CONFIRMED = "authority_confirmed"


class DecisionExplanation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    goal: str
    evidence: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    selection_reason: str
    result: str | None = None


class Decision(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision_id: str
    case_id: str
    decision_type: DecisionType
    title: str
    question: str
    chosen_action: str
    alternatives: list[str] = Field(default_factory=list)
    evidence_event_ids: list[str] = Field(default_factory=list)
    constraint_summary: str | None = None
    requires_human_confirmation: bool = False
    outcome: str | None = None
    confidence: float = 0.5
    explanation: DecisionExplanation
    sequence_no: int
