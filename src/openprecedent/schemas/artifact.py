from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class ArtifactType(StrEnum):
    FILE = "file"
    COMMAND_OUTPUT = "command_output"
    MESSAGE = "message"
    REPORT = "report"
    PATCH = "patch"


class Artifact(BaseModel):
    model_config = ConfigDict(extra="forbid")

    artifact_id: str
    case_id: str
    artifact_type: ArtifactType
    uri_or_path: str
    summary: str | None = None
