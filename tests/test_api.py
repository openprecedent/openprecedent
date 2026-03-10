import json
import httpx
import pytest
from pathlib import Path

from openprecedent.api import app
from openprecedent.services import OpenPrecedentService
from openprecedent.services import AppendEventInput, CreateCaseInput
from openprecedent.config import get_db_path
from openprecedent.schemas import EventActor, EventType


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
        assert len(extracted.json()["decisions"]) >= 2
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
        assert len(body["decisions"]) >= 2
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
    assert len(decisions) >= 2

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
    decision_types = [item.decision_type.value for item in decisions]
    assert "task_frame_defined" in decision_types
    assert "success_criteria_set" in decision_types

    replay = service.replay_case("case_session")
    assert replay.summary == "Imported OpenClaw session: 9 events, 2 decisions, status=started"


def test_service_lists_openclaw_sessions_from_dict_index(db_path, tmp_path: Path) -> None:
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
        json.dumps(
            {
                "agent:main:main": {
                    "sessionId": "sample-session",
                    "sessionFile": str(transcript_path),
                    "updatedAt": 1730948045000,
                    "model": "gpt-5.3-codex",
                }
            }
        ),
        encoding="utf-8",
    )

    sessions = service.list_openclaw_sessions(sessions_dir)

    assert len(sessions) == 1
    assert sessions[0].session_id == "sample-session"
    assert sessions[0].transcript_path == str(transcript_path)


def test_service_imports_failing_openclaw_command_without_output(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "failing-command-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_failure",
        title="Imported failing OpenClaw session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_failure"
    assert len(result.imported_events) == 7

    events = service.list_events("case_session_failure")
    command_completed = [
        event for event in events if event.event_type.value == "command.completed"
    ]
    assert len(command_completed) == 1
    assert command_completed[0].payload["command"] == "exec_command"
    assert command_completed[0].payload["exit_code"] == 1
    assert command_completed[0].payload["stdout"] is None
    assert command_completed[0].payload["stderr"] is None

    decisions = service.extract_decisions("case_session_failure")
    assert [item.decision_type.value for item in decisions] == ["task_frame_defined"]


def test_service_reports_unsupported_openclaw_session_record_types(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "unsupported-record-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_unsupported_record",
        title="Imported OpenClaw session with unsupported record",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_unsupported_record"
    assert len(result.imported_events) == 4
    assert result.unsupported_record_type_counts == {"audit_marker": 1}


def test_service_imports_openclaw_checkpoint_record_as_event(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "checkpoint-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_checkpoint",
        title="Imported OpenClaw checkpoint session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_checkpoint"
    assert len(result.imported_events) == 5
    assert result.unsupported_record_type_counts == {}

    events = service.list_events("case_session_checkpoint")
    checkpoint_events = [event for event in events if event.event_type.value == "checkpoint.saved"]
    assert len(checkpoint_events) == 1
    assert checkpoint_events[0].payload["checkpoint_id"] == "checkpoint-record-1"
    assert checkpoint_events[0].payload["status"] == "saved"


def test_service_imports_additional_live_openclaw_record_types(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "live-record-types-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_live_record_types",
        title="Imported OpenClaw live record types session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_live_record_types"
    assert len(result.imported_events) == 5
    assert result.unsupported_record_type_counts == {}

    events = service.list_events("case_session_live_record_types")
    thinking_events = [event for event in events if event.event_type.value == "model.invoked"]
    custom_events = [event for event in events if event.event_type.value == "tool.completed"]
    assert len(thinking_events) == 1
    assert thinking_events[0].payload["thinking_level"] == "high"
    assert thinking_events[0].payload["changed_by"] == "user"
    assert thinking_events[0].payload["trigger"] == "slash_command"
    assert len(custom_events) == 1
    assert custom_events[0].payload["tool_name"] == "web_search"
    assert custom_events[0].payload["content"] == "web_search failed because the network was unavailable."
    assert custom_events[0].payload["details"] == {
        "query": "repo governance openprecedent",
        "status": "error",
        "error": "network unavailable",
    }

    decisions = service.extract_decisions("case_session_live_record_types")
    assert [item.decision_type.value for item in decisions] == ["task_frame_defined"]


def test_service_extracts_semantic_decisions_from_follow_up_user_message(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "clarify-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_clarify",
        title="Imported OpenClaw clarify session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_clarify"
    assert len(result.imported_events) == 11

    decisions = service.extract_decisions("case_session_clarify")
    decision_types = [item.decision_type.value for item in decisions]
    assert decision_types == [
        "success_criteria_set",
        "task_frame_defined",
        "clarification_resolved",
        "constraint_adopted",
    ]
    clarification = next(
        item for item in decisions if item.decision_type.value == "clarification_resolved"
    )
    assert clarification.outcome == "Focus on collector scheduling and evaluation gaps."
    assert clarification.evidence_event_ids == ["evt_message_msg-user-clarify-followup"]
    assert clarification.explanation.selection_reason


def test_service_skips_false_clarification_on_wrapped_repeat_message(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent
        / "fixtures"
        / "openclaw_sessions"
        / "wrapped-clarify-false-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_wrapped_clarify_false",
        title="Imported OpenClaw wrapped false clarify session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_wrapped_clarify_false"
    assert len(result.imported_events) == 10

    decisions = service.extract_decisions("case_session_wrapped_clarify_false")
    assert [item.decision_type.value for item in decisions] == [
        "success_criteria_set",
        "task_frame_defined",
    ]


def test_service_strips_openclaw_message_wrappers_before_import(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "wrapped-message-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_wrapped_messages",
        title="Imported OpenClaw wrapped message session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_wrapped_messages"
    assert len(result.imported_events) == 4

    replay = service.replay_case("case_session_wrapped_messages")
    message_events = [event for event in replay.events if event.event_type.value == "message.user"]
    assert len(message_events) == 1
    assert message_events[0].payload["message"] == "Summarize the collector rollout findings."

    assistant_messages = [event for event in replay.events if event.event_type.value == "message.agent"]
    assert [event.payload["message"] for event in assistant_messages] == [
        "I will summarize the collector rollout findings.",
        "The collector rollout validated scheduled imports without duplicate sessions.",
    ]

    decisions = service.extract_decisions("case_session_wrapped_messages")
    assert [item.decision_type.value for item in decisions] == [
        "success_criteria_set",
        "task_frame_defined",
    ]


def test_service_imports_openclaw_file_operations(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = Path(__file__).parent / "fixtures" / "openclaw_sessions" / "file-ops-session.jsonl"

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_file_ops",
        title="Imported OpenClaw file ops session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_file_ops"
    assert len(result.imported_events) == 12

    events = service.list_events("case_session_file_ops")
    file_reads = [event for event in events if event.event_type.value == "file.read"]
    file_writes = [event for event in events if event.event_type.value == "file.write"]
    assert len(file_reads) == 1
    assert file_reads[0].payload["path"] == "docs/product/mvp-roadmap.md"
    assert len(file_writes) == 1
    assert file_writes[0].payload["path"] == "docs/architecture/openclaw-silent-collection.md"

    decisions = service.extract_decisions("case_session_file_ops")
    assert [item.decision_type.value for item in decisions] == ["task_frame_defined"]


def test_service_extracts_authority_and_option_rejection_semantics(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    service.create_case(
        CreateCaseInput(case_id="case_semantic_authority", title="Semantic authority test")
    )

    service.append_event(
        "case_semantic_authority",
        AppendEventInput(
            event_type=EventType.MESSAGE_USER,
            actor=EventActor.USER,
            payload={"message": "Do not edit code. Provide a short written recommendation only."},
        ),
    )
    service.append_event(
        "case_semantic_authority",
        AppendEventInput(
            event_type=EventType.USER_CONFIRMED,
            actor=EventActor.USER,
            payload={"message": "Approved. Stay within docs-only scope."},
        ),
    )

    decisions = service.extract_decisions("case_semantic_authority")
    decision_types = [item.decision_type.value for item in decisions]
    assert decision_types == [
        "constraint_adopted",
        "success_criteria_set",
        "option_rejected",
        "authority_confirmed",
    ]
    authority = next(item for item in decisions if item.decision_type.value == "authority_confirmed")
    assert authority.requires_human_confirmation is True


def test_service_imports_openclaw_view_image_as_file_read(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "view-image-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_view_image",
        title="Imported OpenClaw image session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_view_image"
    assert len(result.imported_events) == 6

    events = service.list_events("case_session_view_image")
    file_reads = [event for event in events if event.event_type.value == "file.read"]
    assert len(file_reads) == 1
    assert (
        file_reads[0].payload["path"]
        == "/workspace/04-assets/exports/browser-tools/playwright/demo-protected.png"
    )


def test_service_imports_openclaw_search_command_as_file_reads(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    transcript_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "search-read-session.jsonl"
    )

    result = service.import_openclaw_session(
        transcript_path,
        case_id="case_session_search_read",
        title="Imported OpenClaw search session",
        user_id="u1",
    )

    assert result.case.case_id == "case_session_search_read"
    assert len(result.imported_events) == 9

    events = service.list_events("case_session_search_read")
    file_reads = [event for event in events if event.event_type.value == "file.read"]
    assert len(file_reads) == 2
    assert [event.payload["path"] for event in file_reads] == [
        "docs/product/mvp-roadmap.md",
        "docs/architecture/openclaw-silent-collection.md",
    ]


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


def test_service_dedupes_openclaw_transcript_across_manual_import_and_collector(
    db_path, tmp_path: Path
) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    fixture_dir = Path(__file__).parent / "fixtures" / "openclaw_sessions"
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    transcript_name = "sample-session.jsonl"
    transcript_path = sessions_dir / transcript_name
    transcript_path.write_text(
        (fixture_dir / transcript_name).read_text(encoding="utf-8"),
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

    manual = service.import_openclaw_session(
        transcript_path,
        case_id="case_manual_sample",
        title="Manual sample import",
        user_id="u1",
    )
    assert manual.case.case_id == "case_manual_sample"
    assert len(manual.imported_events) == 9

    collected = service.collect_openclaw_sessions(
        sessions_dir,
        state_path=state_path,
        limit=1,
        user_id="u1",
    )
    assert len(collected.imported) == 1
    assert collected.imported[0].session_id == "sample-session"
    assert collected.imported[0].case_id == "case_manual_sample"
    assert collected.imported[0].imported_event_count == 0

    cases = service.list_cases()
    assert [case.case_id for case in cases] == ["case_manual_sample"]
    replay = service.replay_case("case_manual_sample")
    assert len(replay.events) == 9


def test_service_evaluates_fixture_suite(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "suite.json"

    report = service.evaluate_openclaw_fixture_suite(suite_path)

    assert report.total_cases == 5
    assert report.failed_cases == 0
    assert report.passed_cases == 5
    assert all(not item.extra_decision_types for item in report.results)

    authority_result = next(item for item in report.results if item.case_id == "eval_authority_scope")
    assert [decision_type.value for decision_type in authority_result.actual_decision_types] == [
        "constraint_adopted",
        "success_criteria_set",
        "option_rejected",
        "task_frame_defined",
        "authority_confirmed",
    ]

    operational_only = next(item for item in report.results if item.case_id == "eval_operational_only")
    assert operational_only.actual_decision_types == []
    assert operational_only.extra_decision_types == []


def test_service_evaluates_real_session_fixture_suite(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "real_session_suite.json"

    report = service.evaluate_openclaw_fixture_suite(suite_path)

    assert report.total_cases == 3
    assert report.failed_cases == 0
    assert report.passed_cases == 3
    assert all(not item.extra_decision_types for item in report.results)
    clarify_result = next(item for item in report.results if item.case_id == "eval_real_clarify")
    assert "clarification_resolved" in [
        decision_type.value for decision_type in clarify_result.actual_decision_types
    ]


def test_service_fixture_evaluation_fails_fast_on_reused_database(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "real_session_suite.json"

    first = service.evaluate_openclaw_fixture_suite(suite_path)
    assert first.passed_cases == 3

    with pytest.raises(ValueError, match="fixture evaluation requires an isolated database"):
        service.evaluate_openclaw_fixture_suite(suite_path)

    cases = service.list_cases()
    assert sorted(case.case_id for case in cases) == [
        "eval_real_clarify",
        "eval_real_file_ops",
        "eval_real_search_read",
    ]


def test_service_precedent_prefers_shared_read_targets_for_real_session_search(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "real_session_suite.json"

    service.evaluate_openclaw_fixture_suite(suite_path)

    precedents = service.find_precedents("eval_real_search_read", limit=2)

    assert len(precedents) == 2
    assert precedents[0].case_id == "eval_real_file_ops"
    assert precedents[0].similarity_score >= precedents[1].similarity_score


def test_service_evaluates_collected_openclaw_sessions(db_path, tmp_path: Path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    fixture_dir = Path(__file__).parent / "fixtures" / "openclaw_sessions"
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    for name in (
        "sample-session.jsonl",
        "failing-command-session.jsonl",
        "unsupported-record-session.jsonl",
    ):
        (sessions_dir / name).write_text(
            (fixture_dir / name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    (sessions_dir / "sessions.json").write_text(
        json.dumps(
            [
                {
                    "sessionId": "sample-session",
                    "sessionFile": str(sessions_dir / "sample-session.jsonl"),
                    "updatedAt": 1741497000000,
                    "label": "User session: summarize context graph",
                },
                {
                    "sessionId": "failing-command-session",
                    "sessionFile": str(sessions_dir / "failing-command-session.jsonl"),
                    "updatedAt": 1741498000000,
                    "label": "User session: failing command",
                },
                {
                    "sessionId": "unsupported-record-session",
                    "sessionFile": str(sessions_dir / "unsupported-record-session.jsonl"),
                    "updatedAt": 1741499000000,
                    "label": "User session: unsupported record",
                },
            ]
        ),
        encoding="utf-8",
    )
    state_path = tmp_path / "collector-state.json"
    state_path.write_text(
        json.dumps(
            {
                "imported_session_ids": [
                    "failing-command-session",
                    "sample-session",
                    "unsupported-record-session",
                ]
            }
        ),
        encoding="utf-8",
    )

    report = service.evaluate_collected_openclaw_sessions(
        sessions_dir,
        state_path=state_path,
        user_id="u1",
    )

    assert report.total_sessions == 3
    assert report.evaluated_cases == 3
    assert report.failed_cases == 0
    assert report.cases_with_precedents >= 1
    assert "task_frame_defined" in report.decision_type_counts
    assert report.unsupported_record_type_counts == {"audit_marker": 1}
    assert {item.session_id for item in report.results} == {
        "sample-session",
        "failing-command-session",
        "unsupported-record-session",
    }
    failing_result = next(item for item in report.results if item.session_id == "failing-command-session")
    assert failing_result.has_recovery is True
    unsupported_result = next(item for item in report.results if item.session_id == "unsupported-record-session")
    assert unsupported_result.unsupported_record_type_counts == {"audit_marker": 1}


def test_service_precedent_prefers_semantically_related_case(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())

    cases = [
        (
            "case_semantic_current",
            "Summarize roadmap docs",
            [
                ("message.user", "user", {"message": "Summarize the roadmap docs and collection guidance"}),
                ("message.agent", "agent", {"message": "I will inspect the roadmap docs and summarize them."}),
                ("tool.called", "agent", {"tool_name": "rg", "reason": "search roadmap docs"}),
                ("file.write", "agent", {"path": "docs/roadmap-summary.md", "summary": "wrote roadmap summary"}),
                ("case.completed", "system", {"summary": "roadmap summary delivered"}),
            ],
        ),
        (
            "case_semantic_related",
            "Summarize collection docs",
            [
                ("message.user", "user", {"message": "Summarize the collection docs for OpenClaw"}),
                ("message.agent", "agent", {"message": "I will inspect collection docs and summarize them."}),
                ("tool.called", "agent", {"tool_name": "rg", "reason": "search collection docs"}),
                ("file.write", "agent", {"path": "docs/collection-summary.md", "summary": "wrote collection summary"}),
                ("case.completed", "system", {"summary": "collection summary delivered"}),
            ],
        ),
        (
            "case_semantic_irrelevant",
            "Fix failing tests",
            [
                ("message.user", "user", {"message": "Fix the failing pytest suite"}),
                ("message.agent", "agent", {"message": "I will inspect the failing tests and patch them."}),
                ("tool.called", "agent", {"tool_name": "pytest", "reason": "run test suite"}),
                ("file.write", "agent", {"path": "tests/test_cli.py", "summary": "fixed failing tests"}),
                ("case.completed", "system", {"summary": "tests fixed"}),
            ],
        ),
    ]

    for case_id, title, events in cases:
        service.create_case(CreateCaseInput(case_id=case_id, title=title))
        for index, (event_type, actor, payload) in enumerate(events, start=1):
            service.append_event(
                case_id,
                AppendEventInput(
                    event_type=EventType(event_type),
                    actor=EventActor(actor),
                    payload=payload,
                    sequence_no=index,
                ),
            )
        service.extract_decisions(case_id)

    precedents = service.find_precedents("case_semantic_current", limit=2)
    assert len(precedents) == 2
    assert precedents[0].case_id == "case_semantic_related"
    assert precedents[0].similarity_score > precedents[1].similarity_score


def test_service_fixture_suite_includes_operational_negative_case(db_path) -> None:
    service = OpenPrecedentService.from_path(get_db_path())
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "suite.json"

    report = service.evaluate_openclaw_fixture_suite(suite_path)

    operational_only = next(item for item in report.results if item.case_id == "eval_operational_only")
    assert operational_only.expected_decision_types == []
    assert operational_only.actual_decision_types == []
    assert operational_only.missing_decision_types == []
    assert operational_only.extra_decision_types == []
