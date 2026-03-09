from fastapi import FastAPI

from openprecedent.schemas import Artifact, Case, Decision, Event, Precedent


app = FastAPI(title="OpenPrecedent", version="0.1.0")


@app.get("/healthz")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/schemas")
def schema_catalog() -> dict[str, object]:
    return {
        "case": Case.model_json_schema(),
        "event": Event.model_json_schema(),
        "decision": Decision.model_json_schema(),
        "artifact": Artifact.model_json_schema(),
        "precedent": Precedent.model_json_schema(),
    }
