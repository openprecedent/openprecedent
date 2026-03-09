from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict

from openprecedent.config import get_db_path
from openprecedent.schemas import Artifact, Case, Decision, Event, Precedent
from openprecedent.services import (
    AppendEventInput,
    ConflictError,
    CreateCaseInput,
    OpenPrecedentService,
    ReplayResponse,
)


app = FastAPI(title="OpenPrecedent", version="0.1.0")


class ExtractionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    case_id: str
    decisions: list[Decision]


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/schemas")
async def schema_catalog() -> dict[str, object]:
    return {
        "case": Case.model_json_schema(),
        "event": Event.model_json_schema(),
        "decision": Decision.model_json_schema(),
        "artifact": Artifact.model_json_schema(),
        "precedent": Precedent.model_json_schema(),
    }


def get_service() -> OpenPrecedentService:
    return OpenPrecedentService.from_path(get_db_path())


@app.post("/cases", response_model=Case, status_code=201)
async def create_case(payload: CreateCaseInput) -> Case:
    try:
        return get_service().create_case(payload)
    except ConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@app.get("/cases", response_model=list[Case])
async def list_cases() -> list[Case]:
    return get_service().list_cases()


@app.get("/cases/{case_id}", response_model=Case)
async def get_case(case_id: str) -> Case:
    case = get_service().get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="case not found")
    return case


@app.post("/cases/{case_id}/events", response_model=Event, status_code=201)
async def append_event(case_id: str, payload: AppendEventInput) -> Event:
    try:
        return get_service().append_event(case_id, payload)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="case not found") from error
    except ConflictError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@app.get("/cases/{case_id}/events", response_model=list[Event])
async def list_events(case_id: str) -> list[Event]:
    try:
        return get_service().list_events(case_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="case not found") from error


@app.get("/cases/{case_id}/replay", response_model=ReplayResponse)
async def replay_case(case_id: str) -> ReplayResponse:
    try:
        return get_service().replay_case(case_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="case not found") from error


@app.post("/cases/{case_id}/extract-decisions", response_model=ExtractionResponse)
async def extract_decisions(case_id: str) -> ExtractionResponse:
    try:
        decisions = get_service().extract_decisions(case_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="case not found") from error
    return ExtractionResponse(case_id=case_id, decisions=decisions)


@app.get("/cases/{case_id}/decisions", response_model=list[Decision])
async def list_decisions(case_id: str) -> list[Decision]:
    try:
        return get_service().list_decisions(case_id)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="case not found") from error


@app.get("/cases/{case_id}/precedents", response_model=list[Precedent])
async def find_precedents(case_id: str, limit: int = 3) -> list[Precedent]:
    try:
        return get_service().find_precedents(case_id, limit=limit)
    except KeyError as error:
        raise HTTPException(status_code=404, detail="case not found") from error
