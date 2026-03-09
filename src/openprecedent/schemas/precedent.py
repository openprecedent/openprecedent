from pydantic import BaseModel, ConfigDict


class Precedent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    title: str
    summary: str
    similarity_score: int
    similarities: list[str]
    differences: list[str]
    reusable_takeaway: str | None = None
    historical_outcome: str | None = None
