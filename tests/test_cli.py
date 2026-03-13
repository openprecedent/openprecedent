from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from openprecedent.cli import main


def test_cli_end_to_end(capsys, db_path) -> None:
    result = main(["case", "create", "--case-id", "case_cli", "--title", "CLI task"])
    assert result == 0
    created = json.loads(capsys.readouterr().out)
    assert created["case_id"] == "case_cli"

    result = main(
        [
            "event",
            "append",
            "case_cli",
            "message.agent",
            "agent",
            "--payload",
            '{"message":"I will inspect files first."}',
        ]
    )
    assert result == 0
    capsys.readouterr()

    result = main(
        [
            "event",
            "append",
            "case_cli",
            "tool.called",
            "agent",
            "--payload",
            '{"tool_name":"rg","reason":"search"}',
        ]
    )
    assert result == 0
    capsys.readouterr()

    result = main(
        [
            "event",
            "append",
            "case_cli",
            "case.completed",
            "system",
            "--payload",
            '{"summary":"done"}',
        ]
    )
    assert result == 0
    capsys.readouterr()

    result = main(["extract", "decisions", "case_cli"])
    assert result == 0
    decisions = json.loads(capsys.readouterr().out)
    assert len(decisions) >= 1
    assert "explanation" in decisions[0]
    assert "selection_reason" in decisions[0]["explanation"]

    result = main(["replay", "case", "case_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert replay["case"]["case_id"] == "case_cli"
    assert replay["summary"] == "done"
    assert replay["artifacts"]

    result = main(["decisions", "show", "case_cli"])
    assert result == 0
    rendered = capsys.readouterr().out
    assert "chosen_action:" in rendered
    assert "why:" in rendered


def test_cli_precedent_output(capsys, db_path) -> None:
    for case_id, title, summary in (
        ("case_prev_a", "Previous A", "done a"),
        ("case_prev_b", "Previous B", "done b"),
    ):
        result = main(["case", "create", "--case-id", case_id, "--title", title])
        assert result == 0
        capsys.readouterr()
        for command in (
            [
                "event",
                "append",
                case_id,
                "message.agent",
                "agent",
                "--payload",
                '{"message":"I will inspect files first."}',
            ],
            [
                "event",
                "append",
                case_id,
                "tool.called",
                "agent",
                "--payload",
                '{"tool_name":"rg","reason":"search"}',
            ],
            [
                "event",
                "append",
                case_id,
                "case.completed",
                "system",
                "--payload",
                f'{{"summary":"{summary}"}}',
            ],
        ):
            result = main(command)
            assert result == 0
            capsys.readouterr()
        result = main(["extract", "decisions", case_id])
        assert result == 0
        capsys.readouterr()

    result = main(["precedent", "find", "case_prev_a"])
    assert result == 0
    precedents = json.loads(capsys.readouterr().out)
    assert len(precedents) == 1
    assert precedents[0]["case_id"] == "case_prev_b"
    assert precedents[0]["similarities"]
    assert precedents[0]["similarity_score"] > 0


def test_cli_import_jsonl(capsys, db_path, tmp_path: Path) -> None:
    result = main(["case", "create", "--case-id", "case_import", "--title", "Import task"])
    assert result == 0
    capsys.readouterr()

    payload_path = tmp_path / "events.jsonl"
    payload_path.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "case_id": "case_import",
                        "event_type": "message.user",
                        "actor": "user",
                        "payload": {"message": "hello"},
                    }
                ),
                json.dumps(
                    {
                        "case_id": "case_import",
                        "event_type": "case.completed",
                        "actor": "system",
                        "payload": {"summary": "imported"},
                    }
                ),
            ]
        ),
        encoding="utf-8",
    )

    result = main(["event", "import-jsonl", str(payload_path)])
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert len(imported) == 2


def test_cli_import_openclaw_runtime_trace(capsys, db_path) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "openclaw_trace.jsonl"

    result = main(
        [
            "runtime",
            "import-openclaw",
            str(fixture_path),
            "--case-id",
            "case_openclaw",
            "--title",
            "OpenClaw imported trace",
            "--user-id",
            "u1",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_openclaw"
    assert imported["imported_event_count"] == 6

    result = main(["extract", "decisions", "case_openclaw"])
    assert result == 0
    decisions = json.loads(capsys.readouterr().out)
    decision_types = [item["decision_type"] for item in decisions]
    assert "task_frame_defined" in decision_types
    assert "success_criteria_set" in decision_types

    result = main(["replay", "case", "case_openclaw", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert replay["case"]["status"] == "completed"
    assert replay["summary"] == "Provided the context-graph document summary."
    assert replay["artifacts"]


def test_cli_import_codex_rollout_trace(capsys, db_path) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "codex_rollout.jsonl"

    result = main(
        [
            "runtime",
            "import-codex-rollout",
            str(fixture_path),
            "--case-id",
            "case_codex_rollout",
            "--title",
            "Codex imported rollout",
            "--user-id",
            "u1",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_codex_rollout"
    assert imported["imported_event_count"] == 6
    assert imported["unsupported_record_type_counts"] == {"event_msg:task_started": 1}

    result = main(["replay", "case", "case_codex_rollout", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert replay["case"]["status"] == "completed"
    assert (
        replay["summary"]
        == "Codex runtime research should stay Codex-specific and avoid generic multi-runtime abstraction for now."
    )
    assert replay["artifacts"]


def test_cli_import_codex_rollout_strips_noise(capsys, db_path) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "codex_rollout_noisy.jsonl"

    result = main(
        [
            "runtime",
            "import-codex-rollout",
            str(fixture_path),
            "--case-id",
            "case_codex_noise",
            "--title",
            "Codex noisy rollout",
            "--user-id",
            "u1",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["imported_event_count"] == 6
    assert imported["unsupported_record_type_counts"] == {
        "event_msg:task_started": 1,
        "event_msg:token_count": 1,
        "response_item:message": 2,
        "response_item:reasoning": 1,
        "turn_context": 1,
    }

    result = main(["replay", "case", "case_codex_noise", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert replay["summary"] == "Codex replay should show semantic evidence without transport wrappers."
    tool_called = next(event for event in replay["events"] if event["event_type"] == "tool.called")
    tool_completed = next(event for event in replay["events"] if event["event_type"] == "tool.completed")
    assert tool_called["payload"]["arguments"] == {
        "cmd": "sed -n '1,40p' docs/engineering/codex-runtime-boundary.md",
        "workdir": "/workspace/02-projects/incubation/openprecedent",
    }
    assert tool_completed["payload"]["output"] == (
        "# Codex Runtime Boundary For Research\n"
        "The goal is not to make OpenPrecedent generic."
    )


def test_cli_extracts_semantic_decisions_from_codex_rollout(capsys, db_path) -> None:
    fixture_path = Path(__file__).parent / "fixtures" / "codex_rollout_semantic.jsonl"

    result = main(
        [
            "runtime",
            "import-codex-rollout",
            str(fixture_path),
            "--case-id",
            "case_codex_semantic",
            "--title",
            "Codex semantic rollout",
            "--user-id",
            "u1",
        ]
    )
    assert result == 0
    capsys.readouterr()

    result = main(["extract", "decisions", "case_codex_semantic"])
    assert result == 0
    decisions = json.loads(capsys.readouterr().out)
    decision_types = [item["decision_type"] for item in decisions]

    assert "constraint_adopted" in decision_types
    assert "success_criteria_set" in decision_types
    assert "option_rejected" in decision_types
    assert "task_frame_defined" in decision_types
    assert "clarification_resolved" in decision_types
    assert "authority_confirmed" in decision_types

    authority = next(item for item in decisions if item["decision_type"] == "authority_confirmed")
    assert authority["requires_human_confirmation"] is True
    assert authority["chosen_action"] == "Approved. Continue within that Codex-only scope."


def test_cli_precedent_prefers_semantically_related_codex_case(capsys, db_path) -> None:
    fixture_root = Path(__file__).parent / "fixtures"
    imports = [
        ("case_codex_precedent_current", "Current Codex docs-only recommendation", "codex_rollout_precedent_current.jsonl"),
        ("case_codex_precedent_semantic", "Semantic Codex docs-only precedent", "codex_rollout_precedent_semantic_match.jsonl"),
        ("case_codex_precedent_operational", "Operationally similar Codex summary", "codex_rollout_precedent_operational_overlap.jsonl"),
    ]

    for case_id, title, filename in imports:
        result = main(
            [
                "runtime",
                "import-codex-rollout",
                str(fixture_root / filename),
                "--case-id",
                case_id,
                "--title",
                title,
                "--user-id",
                "u1",
            ]
        )
        assert result == 0
        capsys.readouterr()
        result = main(["extract", "decisions", case_id])
        assert result == 0
        capsys.readouterr()

    result = main(["precedent", "find", "case_codex_precedent_current", "--limit", "2"])
    assert result == 0
    precedents = json.loads(capsys.readouterr().out)

    assert len(precedents) == 2
    assert precedents[0]["case_id"] == "case_codex_precedent_semantic"
    assert precedents[0]["similarity_score"] > precedents[1]["similarity_score"]
    assert precedents[1]["case_id"] == "case_codex_precedent_operational"

def test_cli_lists_and_imports_openclaw_sessions(capsys, db_path, tmp_path: Path) -> None:
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

    result = main(
        [
            "runtime",
            "list-openclaw-sessions",
            "--sessions-root",
            str(sessions_dir),
        ]
    )
    assert result == 0
    sessions = json.loads(capsys.readouterr().out)
    assert len(sessions) == 1
    assert sessions[0]["session_id"] == "sample-session"

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--sessions-root",
            str(sessions_dir),
            "--latest",
            "--case-id",
            "case_session_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_cli"
    assert imported["imported_event_count"] == 9
    assert imported["transcript_path"] == str(transcript_path)

    result = main(["replay", "case", "case_session_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert replay["events"][0]["event_type"] == "case.started"
    assert any(event["event_type"] == "tool.called" for event in replay["events"])
    assert any(event["event_type"] == "command.started" for event in replay["events"])
    assert any(event["event_type"] == "command.completed" for event in replay["events"])


def test_cli_imports_failing_openclaw_command_without_output(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "failing-command-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_failure_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_failure_cli"
    assert imported["imported_event_count"] == 7

    result = main(["extract", "decisions", "case_session_failure_cli"])
    assert result == 0
    decisions = json.loads(capsys.readouterr().out)
    assert [item["decision_type"] for item in decisions] == ["task_frame_defined"]

    result = main(["replay", "case", "case_session_failure_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    command_completed = [
        event for event in replay["events"] if event["event_type"] == "command.completed"
    ]
    assert len(command_completed) == 1
    assert command_completed[0]["payload"]["exit_code"] == 1


def test_cli_imports_openclaw_file_operations(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "file-ops-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_file_ops_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_file_ops_cli"
    assert imported["imported_event_count"] == 12

    result = main(["extract", "decisions", "case_session_file_ops_cli"])
    assert result == 0
    decisions = json.loads(capsys.readouterr().out)
    assert [item["decision_type"] for item in decisions] == ["task_frame_defined"]

    result = main(["replay", "case", "case_session_file_ops_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert any(
        event["event_type"] == "file.read"
        and event["payload"]["path"] == "docs/product/mvp-roadmap.md"
        for event in replay["events"]
    )
    assert any(
        event["event_type"] == "file.write"
        and event["payload"]["path"] == "docs/architecture/openclaw-silent-collection.md"
        for event in replay["events"]
    )


def test_cli_reports_unsupported_openclaw_session_record_types(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "unsupported-record-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_unsupported_record_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_unsupported_record_cli"
    assert imported["imported_event_count"] == 4
    assert imported["unsupported_record_type_counts"] == {"audit_marker": 1}


def test_cli_imports_openclaw_checkpoint_record_as_event(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "checkpoint-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_checkpoint_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_checkpoint_cli"
    assert imported["imported_event_count"] == 5
    assert imported["unsupported_record_type_counts"] == {}

    result = main(["replay", "case", "case_session_checkpoint_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    checkpoint_events = [event for event in replay["events"] if event["event_type"] == "checkpoint.saved"]
    assert len(checkpoint_events) == 1
    assert checkpoint_events[0]["payload"]["checkpoint_id"] == "checkpoint-record-1"
    assert checkpoint_events[0]["payload"]["status"] == "saved"


def test_cli_imports_additional_live_openclaw_record_types(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "live-record-types-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_live_record_types_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_live_record_types_cli"
    assert imported["imported_event_count"] == 5
    assert imported["unsupported_record_type_counts"] == {}

    result = main(["replay", "case", "case_session_live_record_types_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    thinking_events = [event for event in replay["events"] if event["event_type"] == "model.invoked"]
    custom_events = [event for event in replay["events"] if event["event_type"] == "tool.completed"]
    assert len(thinking_events) == 1
    assert thinking_events[0]["payload"]["thinking_level"] == "high"
    assert thinking_events[0]["payload"]["changed_by"] == "user"
    assert thinking_events[0]["payload"]["trigger"] == "slash_command"
    assert len(custom_events) == 1
    assert custom_events[0]["payload"]["tool_name"] == "web_search"
    assert custom_events[0]["payload"]["details"]["status"] == "error"


def test_cli_extracts_semantic_decisions_from_follow_up_user_message(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "clarify-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_clarify_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_clarify_cli"
    assert imported["imported_event_count"] == 11

    result = main(["extract", "decisions", "case_session_clarify_cli"])
    assert result == 0
    decisions = json.loads(capsys.readouterr().out)
    assert [item["decision_type"] for item in decisions] == [
        "success_criteria_set",
        "task_frame_defined",
        "clarification_resolved",
        "constraint_adopted",
    ]
    clarification = next(item for item in decisions if item["decision_type"] == "clarification_resolved")
    assert clarification["outcome"] == "Focus on collector scheduling and evaluation gaps."
    assert clarification["evidence_event_ids"] == ["evt_message_msg-user-clarify-followup"]


def test_cli_skips_false_clarification_on_wrapped_repeat_message(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent
        / "fixtures"
        / "openclaw_sessions"
        / "wrapped-clarify-false-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_wrapped_clarify_false_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_wrapped_clarify_false_cli"
    assert imported["imported_event_count"] == 10

    result = main(["extract", "decisions", "case_session_wrapped_clarify_false_cli"])
    assert result == 0
    decisions = json.loads(capsys.readouterr().out)
    assert [item["decision_type"] for item in decisions] == [
        "success_criteria_set",
        "task_frame_defined",
    ]


def test_cli_strips_openclaw_message_wrappers_before_import(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "wrapped-message-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_wrapped_messages_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_wrapped_messages_cli"
    assert imported["imported_event_count"] == 4

    result = main(["replay", "case", "case_session_wrapped_messages_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    message_events = [event for event in replay["events"] if event["event_type"] == "message.user"]
    assert len(message_events) == 1
    assert message_events[0]["payload"]["message"] == "Summarize the collector rollout findings."

    result = main(["extract", "decisions", "case_session_wrapped_messages_cli"])
    assert result == 0
    decisions = json.loads(capsys.readouterr().out)
    assert [item["decision_type"] for item in decisions] == [
        "success_criteria_set",
        "task_frame_defined",
    ]


def test_cli_imports_openclaw_view_image_as_file_read(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "view-image-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_view_image_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_view_image_cli"
    assert imported["imported_event_count"] == 6

    result = main(["replay", "case", "case_session_view_image_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert any(
        event["event_type"] == "file.read"
        and event["payload"]["path"]
        == "/workspace/04-assets/exports/browser-tools/playwright/demo-protected.png"
        for event in replay["events"]
    )


def test_cli_imports_openclaw_search_command_as_file_reads(capsys, db_path) -> None:
    fixture_path = (
        Path(__file__).parent / "fixtures" / "openclaw_sessions" / "search-read-session.jsonl"
    )

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(fixture_path),
            "--case-id",
            "case_session_search_read_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_session_search_read_cli"
    assert imported["imported_event_count"] == 9

    result = main(["replay", "case", "case_session_search_read_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    file_reads = [event for event in replay["events"] if event["event_type"] == "file.read"]
    assert [event["payload"]["path"] for event in file_reads] == [
        "docs/product/mvp-roadmap.md",
        "docs/architecture/openclaw-silent-collection.md",
    ]


def test_cli_collects_openclaw_sessions(capsys, db_path, tmp_path: Path) -> None:
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

    result = main(
        [
            "runtime",
            "collect-openclaw-sessions",
            "--sessions-root",
            str(sessions_dir),
            "--state-file",
            str(state_path),
            "--limit",
            "1",
        ]
    )
    assert result == 0
    collected = json.loads(capsys.readouterr().out)
    assert len(collected["imported"]) == 1
    assert collected["imported"][0]["session_id"] == "sample-session"
    assert collected["imported"][0]["transcript_path"] == str(transcript_path)

    result = main(
        [
            "runtime",
            "collect-openclaw-sessions",
            "--sessions-root",
            str(sessions_dir),
            "--state-file",
            str(state_path),
            "--limit",
            "1",
        ]
    )
    assert result == 0
    collected_again = json.loads(capsys.readouterr().out)
    assert collected_again["imported"] == []
    assert "sample-session" in collected_again["skipped_session_ids"]


def test_cli_dedupes_openclaw_transcript_across_manual_import_and_collector(
    capsys, db_path, tmp_path: Path
) -> None:
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

    result = main(
        [
            "runtime",
            "import-openclaw-session",
            "--session-file",
            str(transcript_path),
            "--case-id",
            "case_manual_sample_cli",
        ]
    )
    assert result == 0
    imported = json.loads(capsys.readouterr().out)
    assert imported["case"]["case_id"] == "case_manual_sample_cli"
    assert imported["imported_event_count"] == 9

    result = main(
        [
            "runtime",
            "collect-openclaw-sessions",
            "--sessions-root",
            str(sessions_dir),
            "--state-file",
            str(state_path),
            "--limit",
            "1",
        ]
    )
    assert result == 0
    collected = json.loads(capsys.readouterr().out)
    assert len(collected["imported"]) == 1
    assert collected["imported"][0]["session_id"] == "sample-session"
    assert collected["imported"][0]["case_id"] == "case_manual_sample_cli"
    assert collected["imported"][0]["imported_event_count"] == 0

    result = main(["case", "list"])
    assert result == 0
    cases = json.loads(capsys.readouterr().out)
    assert [case["case_id"] for case in cases] == ["case_manual_sample_cli"]


def test_run_collector_script_prefers_repo_venv_binary(tmp_path: Path) -> None:
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    (sessions_dir / "sessions.json").write_text("[]", encoding="utf-8")

    db_path = tmp_path / "openprecedent.db"
    state_path = tmp_path / "collector-state.json"
    env = os.environ.copy()
    env.pop("OPENPRECEDENT_BIN", None)
    env["OPENPRECEDENT_DB"] = str(db_path)
    env["OPENPRECEDENT_COLLECTOR_STATE"] = str(state_path)
    env["OPENCLAW_SESSIONS_ROOT"] = str(sessions_dir)
    env["PATH"] = "/usr/bin:/bin"
    env["PYTHONPATH"] = str(Path(__file__).parent.parent / "src")

    result = subprocess.run(
        ["./scripts/run-collector.sh"],
        cwd=Path(__file__).parent.parent,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert db_path.exists()
    assert state_path.exists()


def test_cli_evaluates_fixture_suite(capsys, db_path) -> None:
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "suite.json"

    result = main(["eval", "fixtures", str(suite_path), "--json"])
    assert result == 0
    report = json.loads(capsys.readouterr().out)
    assert report["total_cases"] == 5
    assert report["failed_cases"] == 0
    assert report["passed_cases"] == 5
    assert all(not item["extra_decision_types"] for item in report["results"])

    authority_result = next(item for item in report["results"] if item["case_id"] == "eval_authority_scope")
    assert authority_result["actual_decision_types"] == [
        "constraint_adopted",
        "success_criteria_set",
        "option_rejected",
        "task_frame_defined",
        "authority_confirmed",
    ]

    operational_only = next(item for item in report["results"] if item["case_id"] == "eval_operational_only")
    assert operational_only["actual_decision_types"] == []
    assert operational_only["extra_decision_types"] == []


def test_cli_builds_decision_lineage_brief(capsys, db_path) -> None:
    for case_id, title, events in (
        (
            "case_cli_brief_guidance",
            "Docs-only recommendation",
            [
                ["event", "append", "case_cli_brief_guidance", "message.user", "user", "--payload", '{"message":"Do not edit code. Provide a short written recommendation only."}'],
                ["event", "append", "case_cli_brief_guidance", "message.agent", "agent", "--payload", '{"message":"I will stay within docs-only scope and provide a short recommendation."}'],
                ["event", "append", "case_cli_brief_guidance", "user.confirmed", "user", "--payload", '{"message":"Approved. Stay within docs-only scope."}'],
            ],
        ),
    ):
        result = main(["case", "create", "--case-id", case_id, "--title", title])
        assert result == 0
        capsys.readouterr()
        for command in events:
            result = main(command)
            assert result == 0
            capsys.readouterr()
        result = main(["extract", "decisions", case_id])
        assert result == 0
        capsys.readouterr()

    result = main(
        [
            "runtime",
            "decision-lineage-brief",
            "--query-reason",
            "initial_planning",
            "--task-summary",
            "Do not edit code. Provide a short written recommendation only.",
        ]
    )
    assert result == 0
    brief = json.loads(capsys.readouterr().out)
    assert brief["matched_cases"][0]["case_id"] == "case_cli_brief_guidance"
    assert brief["accepted_constraints"]
    assert brief["authority_signals"]


def test_cli_records_runtime_decision_lineage_invocation(capsys, db_path, tmp_path: Path) -> None:
    log_path = tmp_path / "runtime-invocations.jsonl"

    result = main(["case", "create", "--case-id", "case_cli_brief_guidance", "--title", "Docs-only recommendation"])
    assert result == 0
    capsys.readouterr()
    for command in (
        [
            "event",
            "append",
            "case_cli_brief_guidance",
            "message.user",
            "user",
            "--payload",
            '{"message":"Do not edit code. Provide a short written recommendation only."}',
        ],
        [
            "event",
            "append",
            "case_cli_brief_guidance",
            "message.agent",
            "agent",
            "--payload",
            '{"message":"I will stay within docs-only scope and provide a short recommendation."}',
        ],
        [
            "event",
            "append",
            "case_cli_brief_guidance",
            "user.confirmed",
            "user",
            "--payload",
            '{"message":"Approved. Stay within docs-only scope."}',
        ],
    ):
        result = main(command)
        assert result == 0
        capsys.readouterr()
    result = main(["extract", "decisions", "case_cli_brief_guidance"])
    assert result == 0
    capsys.readouterr()

    result = main(["case", "create", "--case-id", "case_runtime_scope", "--title", "Runtime scope case"])
    assert result == 0
    capsys.readouterr()

    result = main(
        [
            "runtime",
            "decision-lineage-brief",
            "--query-reason",
            "initial_planning",
            "--task-summary",
            "Do not edit code. Provide a short written recommendation only.",
            "--case-id",
            "case_runtime_scope",
            "--session-id",
            "session_runtime_scope",
            "--log-file",
            str(log_path),
        ]
    )
    assert result == 0
    capsys.readouterr()

    result = main(["runtime", "list-decision-lineage-invocations", "--log-file", str(log_path)])
    assert result == 0
    invocations = json.loads(capsys.readouterr().out)
    assert len(invocations) == 1
    assert invocations[0]["query_reason"] == "initial_planning"
    assert invocations[0]["case_id"] == "case_runtime_scope"
    assert invocations[0]["session_id"] == "session_runtime_scope"
    assert invocations[0]["matched_case_ids"] == ["case_cli_brief_guidance"]

    result = main(
        [
            "event",
            "append",
            "case_runtime_scope",
            "message.agent",
            "agent",
            "--payload",
            '{"message":"I will keep this docs-only and avoid code edits."}',
        ]
    )
    assert result == 0
    capsys.readouterr()
    result = main(["extract", "decisions", "case_runtime_scope"])
    assert result == 0
    capsys.readouterr()

    result = main(
        [
            "runtime",
            "inspect-decision-lineage-invocation",
            "--invocation-id",
            invocations[0]["invocation_id"],
            "--log-file",
            str(log_path),
        ]
    )
    assert result == 0
    inspection = json.loads(capsys.readouterr().out)
    assert inspection["invocation"]["matched_case_ids"] == ["case_cli_brief_guidance"]
    assert inspection["downstream_events"]
    assert inspection["downstream_decisions"]


def test_cli_runtime_decision_lineage_validation_baseline_exists() -> None:
    path = (
        Path(__file__).parent.parent
        / "docs"
        / "engineering"
        / "openclaw-runtime-decision-lineage-validation.md"
    )

    content = path.read_text(encoding="utf-8")

    assert "initial_planning" in content
    assert "before_file_write" in content
    assert "after_failure" in content
    assert "keep it consistent with earlier repository decisions" in content


def test_openclaw_skill_bundle_exists() -> None:
    skill_path = (
        Path(__file__).parent.parent
        / "skills"
        / "openprecedent-decision-lineage"
        / "SKILL.md"
    )

    content = skill_path.read_text(encoding="utf-8")

    assert content.startswith("---\n")
    assert 'name: openprecedent-decision-lineage' in content
    assert '"bins":["openprecedent"]' in content
    assert "openprecedent runtime decision-lineage-brief" in content
    assert "Do not wait for the user to explicitly say \"use OpenPrecedent\"." in content
    assert "keep it consistent with earlier repository decisions if relevant" in content


def test_research_harness_skill_exists() -> None:
    skill_path = (
        Path(__file__).parent.parent
        / ".codex"
        / "skills"
        / "research-harness"
        / "SKILL.md"
    )
    template_root = skill_path.parent / "templates"

    content = skill_path.read_text(encoding="utf-8")

    assert content.startswith("---\n")
    assert "name: research-harness" in content
    assert "Parent framework: #100" in content
    assert "issue-state-init" in content
    assert (template_root / "research-experiment-template.md").exists()
    assert (template_root / "research-issue-template.md").exists()
    assert (template_root / "research-result-template.md").exists()


def test_mvp_status_mentions_research_harness_skill() -> None:
    path = Path(__file__).parent.parent / "docs" / "product" / "mvp-status.md"

    content = path.read_text(encoding="utf-8")

    assert ".codex/skills/research-harness/SKILL.md" in content


def test_openclaw_live_validation_skill_exists() -> None:
    skill_path = (
        Path(__file__).parent.parent
        / ".codex"
        / "skills"
        / "openclaw-live-validation"
        / "SKILL.md"
    )

    content = skill_path.read_text(encoding="utf-8")

    assert content.startswith("---\n")
    assert "name: openclaw-live-validation" in content
    assert "./scripts/run-openclaw-live-validation.sh" in content
    assert "not triggered" in content
    assert "triggered with non-empty brief" in content


def test_codex_runtime_decision_lineage_skill_exists() -> None:
    skill_path = (
        Path(__file__).parent.parent
        / ".codex"
        / "skills"
        / "codex-runtime-decision-lineage"
        / "SKILL.md"
    )
    workflow_path = (
        Path(__file__).parent.parent
        / "docs"
        / "engineering"
        / "codex-runtime-decision-lineage-workflow.md"
    )

    content = skill_path.read_text(encoding="utf-8")
    workflow = workflow_path.read_text(encoding="utf-8")

    assert content.startswith("---\n")
    assert "name: codex-runtime-decision-lineage" in content
    assert "./scripts/run-codex-decision-lineage-workflow.sh" in content
    assert "--inspect-latest" in content
    assert "Codex-driven development work" in content
    assert "minimal Codex-facing runtime workflow" in workflow
    assert "openprecedent runtime list-decision-lineage-invocations" in workflow
    assert "python3 -m openprecedent.cli runtime" not in workflow


def test_codex_runtime_startup_docs_exist() -> None:
    repo_root = Path(__file__).parent.parent
    guide_path = repo_root / "docs" / "engineering" / "codex-runtime-startup-guide.md"
    validation_path = repo_root / "docs" / "engineering" / "codex-runtime-startup-validation.md"
    readme_path = repo_root / "README.md"
    usage_path = repo_root / "docs" / "engineering" / "using-openprecedent.md"

    guide = guide_path.read_text(encoding="utf-8")
    validation = validation_path.read_text(encoding="utf-8")
    readme = readme_path.read_text(encoding="utf-8")
    usage = usage_path.read_text(encoding="utf-8")

    assert "./scripts/run-codex-live-validation.sh" in guide
    assert "For Humans" in guide
    assert "For Agents" in guide
    assert "three runtime invocations were recorded" in validation
    assert "Codex runtime startup guide" in readme
    assert "codex-runtime-startup-guide.md" in usage
    assert "codex-runtime-startup-validation.md" in usage


def test_tooling_setup_mentions_live_validation_skill() -> None:
    path = Path(__file__).parent.parent / "docs" / "engineering" / "tooling-setup.md"

    content = path.read_text(encoding="utf-8")

    assert ".codex/skills/openclaw-live-validation/SKILL.md" in content


def test_tooling_setup_mentions_session_start_workflow() -> None:
    path = Path(__file__).parent.parent / "docs" / "engineering" / "tooling-setup.md"

    content = path.read_text(encoding="utf-8")

    assert "./scripts/run-codex-session-start.sh" in content
    assert "directly diagnose, implement, verify, and close the loop" in content


def test_agents_mentions_default_direct_fix_behavior() -> None:
    path = Path(__file__).parent.parent / "AGENTS.md"

    content = path.read_text(encoding="utf-8")

    assert "default to directly diagnosing and fixing it through implementation, verification, and workflow closure" in content


def test_harness_reuse_guide_exists() -> None:
    path = Path(__file__).parent.parent / "docs" / "engineering" / "harness-reuse-guide.md"

    content = path.read_text(encoding="utf-8")

    assert "Current Harness Inventory" in content
    assert "Export Strategy" in content
    assert "existing repository" in content
    assert "brand new repository" in content


def test_openclaw_runtime_trigger_rerun_doc_exists() -> None:
    path = (
        Path(__file__).parent.parent
        / "docs"
        / "engineering"
        / "openclaw-runtime-decision-lineage-trigger-rerun.md"
    )

    content = path.read_text(encoding="utf-8")

    assert "matched_case_ids = [\"case_opv80_prior_readme\"]" in content
    assert "Prompt Under Test: Implicit Prior-Decision Consistency" in content
    assert "This validation closes the trigger-policy change tracked in `#94`." in content


def test_cli_runtime_brief_uses_configured_openprecedent_home(
    capsys,
    tmp_path: Path,
    monkeypatch,
) -> None:
    shared_home = tmp_path / "shared-openprecedent"
    workspace = tmp_path / "openclaw-workspace"
    shared_db = shared_home / "openprecedent.db"
    shared_log = shared_home / "openprecedent-runtime-invocations.jsonl"

    workspace.mkdir()
    monkeypatch.chdir(workspace)
    monkeypatch.setenv("OPENPRECEDENT_HOME", str(shared_home))
    monkeypatch.delenv("OPENPRECEDENT_DB", raising=False)
    monkeypatch.delenv("OPENPRECEDENT_RUNTIME_INVOCATION_LOG", raising=False)

    result = main(["case", "create", "--case-id", "case_shared_guidance", "--title", "Shared DB guidance"])
    assert result == 0
    capsys.readouterr()
    for command in (
        [
            "event",
            "append",
            "case_shared_guidance",
            "message.user",
            "user",
            "--payload",
            '{"message":"Do not edit code. Provide a short written recommendation only."}',
        ],
        [
            "event",
            "append",
            "case_shared_guidance",
            "message.agent",
            "agent",
            "--payload",
            '{"message":"I will stay within docs-only scope and provide a short recommendation."}',
        ],
        [
            "event",
            "append",
            "case_shared_guidance",
            "user.confirmed",
            "user",
            "--payload",
            '{"message":"Approved. Stay within docs-only scope."}',
        ],
    ):
        result = main(command)
        assert result == 0
        capsys.readouterr()
    result = main(["extract", "decisions", "case_shared_guidance"])
    assert result == 0
    capsys.readouterr()

    result = main(
        [
            "runtime",
            "decision-lineage-brief",
            "--query-reason",
            "initial_planning",
            "--task-summary",
            "Do not edit code. Provide a short written recommendation only.",
        ]
    )
    assert result == 0
    brief = json.loads(capsys.readouterr().out)

    assert brief["matched_cases"][0]["case_id"] == "case_shared_guidance"
    assert shared_db.exists()
    assert shared_log.exists()
    assert not (workspace / "openprecedent.db").exists()
    assert not (workspace / "openprecedent-runtime-invocations.jsonl").exists()

    result = main(["runtime", "list-decision-lineage-invocations"])
    assert result == 0
    invocations = json.loads(capsys.readouterr().out)
    assert len(invocations) == 1
    assert invocations[0]["matched_case_ids"] == ["case_shared_guidance"]


def test_cli_runtime_paths_explicit_env_vars_override_openprecedent_home(
    capsys,
    tmp_path: Path,
    monkeypatch,
) -> None:
    shared_home = tmp_path / "shared-openprecedent"
    explicit_db = tmp_path / "custom" / "runtime.db"
    explicit_log = tmp_path / "custom" / "runtime-log.jsonl"
    workspace = tmp_path / "openclaw-workspace"

    workspace.mkdir()
    monkeypatch.chdir(workspace)
    monkeypatch.setenv("OPENPRECEDENT_HOME", str(shared_home))
    monkeypatch.setenv("OPENPRECEDENT_DB", str(explicit_db))
    monkeypatch.setenv("OPENPRECEDENT_RUNTIME_INVOCATION_LOG", str(explicit_log))

    result = main(["case", "create", "--case-id", "case_override_guidance", "--title", "Override guidance"])
    assert result == 0
    capsys.readouterr()
    for command in (
        [
            "event",
            "append",
            "case_override_guidance",
            "message.user",
            "user",
            "--payload",
            '{"message":"Do not edit code. Provide a short written recommendation only."}',
        ],
        [
            "event",
            "append",
            "case_override_guidance",
            "message.agent",
            "agent",
            "--payload",
            '{"message":"I will stay within docs-only scope and provide a short recommendation."}',
        ],
        [
            "event",
            "append",
            "case_override_guidance",
            "user.confirmed",
            "user",
            "--payload",
            '{"message":"Approved. Stay within docs-only scope."}',
        ],
    ):
        result = main(command)
        assert result == 0
        capsys.readouterr()
    result = main(["extract", "decisions", "case_override_guidance"])
    assert result == 0
    capsys.readouterr()

    result = main(
        [
            "runtime",
            "decision-lineage-brief",
            "--query-reason",
            "initial_planning",
            "--task-summary",
            "Do not edit code. Provide a short written recommendation only.",
        ]
    )
    assert result == 0
    capsys.readouterr()

    assert explicit_db.exists()
    assert explicit_log.exists()
    assert not (shared_home / "openprecedent.db").exists()
    assert not (shared_home / "openprecedent-runtime-invocations.jsonl").exists()


def test_cli_evaluates_real_session_fixture_suite(capsys, db_path) -> None:
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "real_session_suite.json"

    result = main(["eval", "fixtures", str(suite_path), "--json"])
    assert result == 0
    report = json.loads(capsys.readouterr().out)
    assert report["total_cases"] == 3
    assert report["failed_cases"] == 0
    assert report["passed_cases"] == 3
    assert all(not item["extra_decision_types"] for item in report["results"])


def test_cli_fixture_evaluation_fails_fast_on_reused_database(capsys, db_path) -> None:
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "real_session_suite.json"

    first = main(["eval", "fixtures", str(suite_path), "--json"])
    assert first == 0
    capsys.readouterr()

    second = main(["eval", "fixtures", str(suite_path), "--json"])
    assert second == 1
    stderr = capsys.readouterr().err
    assert "fixture evaluation requires an isolated database" in stderr

    result = main(["case", "list"])
    assert result == 0
    cases = json.loads(capsys.readouterr().out)
    assert sorted(case["case_id"] for case in cases) == [
        "eval_real_clarify",
        "eval_real_file_ops",
        "eval_real_search_read",
    ]


def test_cli_evaluates_collected_openclaw_sessions(capsys, db_path, tmp_path: Path) -> None:
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
    report_path = tmp_path / "collected-report.json"

    result = main(
        [
            "eval",
            "collected-openclaw-sessions",
            "--sessions-root",
            str(sessions_dir),
            "--state-file",
            str(state_path),
            "--report-file",
            str(report_path),
            "--json",
        ]
    )
    assert result == 0
    report = json.loads(capsys.readouterr().out)
    assert report["total_sessions"] == 3
    assert report["evaluated_cases"] == 3
    assert "task_frame_defined" in report["decision_type_counts"]
    assert report["unsupported_record_type_counts"] == {"audit_marker": 1}
    assert report_path.exists()


def test_cli_renders_unsupported_record_type_summary_for_collected_sessions(capsys, db_path, tmp_path: Path) -> None:
    fixture_dir = Path(__file__).parent / "fixtures" / "openclaw_sessions"
    sessions_dir = tmp_path / "sessions"
    sessions_dir.mkdir()
    name = "unsupported-record-session.jsonl"
    (sessions_dir / name).write_text(
        (fixture_dir / name).read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (sessions_dir / "sessions.json").write_text(
        json.dumps(
            [
                {
                    "sessionId": "unsupported-record-session",
                    "sessionFile": str(sessions_dir / name),
                    "updatedAt": 1741499000000,
                    "label": "User session: unsupported record",
                }
            ]
        ),
        encoding="utf-8",
    )
    state_path = tmp_path / "collector-state.json"
    state_path.write_text(
        json.dumps({"imported_session_ids": ["unsupported-record-session"]}),
        encoding="utf-8",
    )

    result = main(
        [
            "eval",
            "collected-openclaw-sessions",
            "--sessions-root",
            str(sessions_dir),
            "--state-file",
            str(state_path),
        ]
    )
    assert result == 0
    rendered = capsys.readouterr().out
    assert "Unsupported record types: audit_marker=1" in rendered
    assert "unsupported record types: audit_marker=1" in rendered
