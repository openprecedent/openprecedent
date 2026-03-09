import httpx
import pytest

from openprecedent.api import app


async def _client() -> httpx.AsyncClient:
    transport = httpx.ASGITransport(app=app)
    return httpx.AsyncClient(transport=transport, base_url="http://testserver")


@pytest.mark.anyio
async def test_healthcheck() -> None:
    async with await _client() as client:
        response = await client.get("/healthz")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


@pytest.mark.anyio
async def test_schema_catalog_contains_core_objects() -> None:
    async with await _client() as client:
        response = await client.get("/schemas")

        assert response.status_code == 200
        body = response.json()
        assert "case" in body
        assert "event" in body
        assert "decision" in body
        assert "artifact" in body
        assert "precedent" in body


@pytest.mark.anyio
async def test_case_ingestion_replay_and_precedent_flow(db_path) -> None:
    async with await _client() as client:
        first_case = await client.post(
            "/cases",
            json={"case_id": "case_alpha", "title": "Alpha task", "user_id": "u1", "agent_id": "openclaw"},
        )
        assert first_case.status_code == 201

        second_case = await client.post(
            "/cases",
            json={"case_id": "case_beta", "title": "Beta task", "user_id": "u1", "agent_id": "openclaw"},
        )
        assert second_case.status_code == 201

        alpha_events = [
            {"event_type": "message.user", "actor": "user", "payload": {"message": "Summarize docs"}},
            {"event_type": "message.agent", "actor": "agent", "payload": {"message": "I will inspect docs and summarize."}},
            {"event_type": "tool.called", "actor": "agent", "payload": {"tool_name": "rg", "reason": "search files"}},
            {"event_type": "file.write", "actor": "agent", "payload": {"path": "docs/out.md", "summary": "wrote summary"}},
            {"event_type": "case.completed", "actor": "system", "payload": {"summary": "summary delivered"}},
        ]
        for event in alpha_events:
            response = await client.post("/cases/case_alpha/events", json=event)
            assert response.status_code == 201

        beta_events = [
            {"event_type": "message.user", "actor": "user", "payload": {"message": "Summarize docs again"}},
            {"event_type": "message.agent", "actor": "agent", "payload": {"message": "I will inspect docs and summarize."}},
            {"event_type": "tool.called", "actor": "agent", "payload": {"tool_name": "rg", "reason": "search files"}},
            {"event_type": "file.write", "actor": "agent", "payload": {"path": "docs/out-2.md", "summary": "wrote summary"}},
            {"event_type": "case.completed", "actor": "system", "payload": {"summary": "second summary delivered"}},
        ]
        for event in beta_events:
            response = await client.post("/cases/case_beta/events", json=event)
            assert response.status_code == 201

        extracted = await client.post("/cases/case_alpha/extract-decisions")
        assert extracted.status_code == 200
        assert len(extracted.json()["decisions"]) >= 3
        first_decision = extracted.json()["decisions"][0]
        assert "explanation" in first_decision
        assert "goal" in first_decision["explanation"]
        assert "selection_reason" in first_decision["explanation"]
        assert isinstance(first_decision["confidence"], float)

        extracted_beta = await client.post("/cases/case_beta/extract-decisions")
        assert extracted_beta.status_code == 200

        replay = await client.get("/cases/case_alpha/replay")
        assert replay.status_code == 200
        body = replay.json()
        assert body["case"]["case_id"] == "case_alpha"
        assert len(body["events"]) == 5
        assert len(body["decisions"]) >= 3
        assert body["summary"] == "summary delivered"

        precedents = await client.get("/cases/case_alpha/precedents")
        assert precedents.status_code == 200
        precedent_body = precedents.json()
        assert len(precedent_body) == 1
        assert precedent_body[0]["case_id"] == "case_beta"
        assert precedent_body[0]["similarity_score"] > 0
        assert precedent_body[0]["similarities"]
        assert "summary" in precedent_body[0]


@pytest.mark.anyio
async def test_duplicate_case_returns_conflict(db_path) -> None:
    async with await _client() as client:
        response = await client.post("/cases", json={"case_id": "case_dup", "title": "Duplicate"})
        assert response.status_code == 201

        duplicate = await client.post("/cases", json={"case_id": "case_dup", "title": "Duplicate"})
        assert duplicate.status_code == 409
