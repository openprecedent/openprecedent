from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class CaseStatus(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    title: str
    status: CaseStatus
    user_id: str | None = None
    agent_id: str | None = None
    started_at: datetime
    ended_at: datetime | None = None
    final_summary: str | None = None
