from pydantic import BaseModel, ConfigDict


class Precedent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    title: str
    similarity_reason: str
    differences: list[str]
    historical_outcome: str | None = None
