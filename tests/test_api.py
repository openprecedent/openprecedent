import httpx
import pytest
from pathlib import Path

from openprecedent.api import app
from openprecedent.services import OpenPrecedentService
from openprecedent.config import get_db_path


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
        assert len(body["artifacts"]) >= 3
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


def test_service_imports_openclaw_runtime_trace(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    fixture_path = Path(__file__).parent / "fixtures" / "openclaw_trace.jsonl"

    result = service.import_openclaw_jsonl(
        fixture_path,
        case_id="case_runtime",
        title="Runtime import",
        user_id="u1",
    )

    assert result.case.case_id == "case_runtime"
    assert len(result.imported_events) == 6

    decisions = service.extract_decisions("case_runtime")
    assert len(decisions) >= 4

    replay = service.replay_case("case_runtime")
    assert replay.case.status.value == "completed"
    assert replay.summary == "Provided the context-graph document summary."
    assert replay.artifacts

def test_service_lists_and_imports_openclaw_session(db_path, tmp_path: Path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    fixture_dir = Path(__file__).parent / "fixtures" / "openclaw_sessions"
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()

    transcript_path = sessions_dir / "sample-session.jsonl"
    transcript_path.write_text(
        (fixture_dir / "sample-session.jsonl").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    index_text = (fixture_dir / "sessions.json").read_text(encoding="utf-8").replace(
        "__FIXTURE_DIR__",
        str(sessions_dir),
    )
    (sessions_dir / "sessions.json").write_text(index_text, encoding="utf-8")

    sessions = service.list_openclaw_sessions(sessions_dir)
    assert len(sessions) == 1
    assert sessions[0].session_id == "sample-session"
    assert sessions[0].label == "User session: summarize context graph"

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session",
        title="Imported OpenClaw session",
        user_id="u1",
    )
    assert result.case.case_id == "case_session"
    assert len(result.imported_events) == 9

    events = service.list_events("case_session")
    assert events[0].event_type.value == "case.started"
    assert any(event.event_type.value == "message.user" for event in events)
    assert any(event.event_type.value == "tool.called" for event in events)
    assert any(event.event_type.value == "tool.completed" for event in events)
    assert any(event.event_type.value == "command.started" for event in events)
    assert any(event.event_type.value == "command.completed" for event in events)

    decisions = service.extract_decisions("case_session")
    assert any(item.decision_type.value == "plan" for item in decisions)
    assert any(item.decision_type.value == "select_tool" for item in decisions)

    replay = service.replay_case("case_session")
    assert replay.summary == "Imported OpenClaw session: 9 events, 2 decisions, status=started"


def test_service_collects_latest_unseen_openclaw_session(db_path, tmp_path: Path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    fixture_dir = Path(__file__).parent / "fixtures" / "openclaw_sessions"
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    transcript_path = sessions_dir / "sample-session.jsonl"
    transcript_path.write_text(
        (fixture_dir / "sample-session.jsonl").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (sessions_dir / "sessions.json").write_text(
        (fixture_dir / "sessions.json").read_text(encoding="utf-8").replace(
            "__FIXTURE_DIR__",
            str(sessions_dir),
        ),
        encoding="utf-8",
    )
    state_path = tmp_path / "collector-state.json"

    first = service.collect_openclaw_sessions(
        sessions_dir,
        state_path=state_path,
        limit=1,
        user_id="u1",
    )
    assert len(first.imported) == 1
    assert first.imported[0].session_id == "sample-session"
    assert first.imported[0].case_id == "openclaw_samplesession"
    assert state_path.exists()

    second = service.collect_openclaw_sessions(
        sessions_dir,
        state_path=state_path,
        limit=1,
        user_id="u1",
    )
    assert second.imported == []
    assert "sample-session" in second.skipped_session_ids


def test_service_evaluates_fixture_suite(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "suite.json"

    report = service.evaluate_openclaw_fixture_suite(suite_path)

    assert report.total_cases == 3
    assert report.failed_cases == 0
    assert report.passed_cases == 3
