from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class EventType(StrEnum):
    CASE_STARTED = "case.started"
    CHECKPOINT_SAVED = "checkpoint.saved"
    MESSAGE_USER = "message.user"
    MESSAGE_AGENT = "message.agent"
    MODEL_INVOKED = "model.invoked"
    MODEL_COMPLETED = "model.completed"
    TOOL_CALLED = "tool.called"
    TOOL_COMPLETED = "tool.completed"
    COMMAND_STARTED = "command.started"
    COMMAND_COMPLETED = "command.completed"
    FILE_READ = "file.read"
    FILE_WRITE = "file.write"
    USER_CONFIRMED = "user.confirmed"
    CASE_COMPLETED = "case.completed"
    CASE_FAILED = "case.failed"


class EventActor(StrEnum):
    USER = "user"
    AGENT = "agent"
    SYSTEM = "system"
    TOOL = "tool"


class Event(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str
    case_id: str
    event_type: EventType
    actor: EventActor
    timestamp: datetime
    sequence_no: int
    parent_event_id: str | None = None
    payload: dict[str, object] = Field(default_factory=dict)
