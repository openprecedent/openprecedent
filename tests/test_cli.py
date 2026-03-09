from __future__ import annotations

import json
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
    assert len(decisions) >= 2
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
    assert any(item["decision_type"] == "plan" for item in decisions)
    assert any(item["decision_type"] == "select_tool" for item in decisions)
    assert any(item["decision_type"] == "apply_change" for item in decisions)
    assert any(item["decision_type"] == "finalize" for item in decisions)

    result = main(["replay", "case", "case_openclaw", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert replay["case"]["status"] == "completed"
    assert replay["summary"] == "Provided the context-graph document summary."
    assert replay["artifacts"]

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
    assert any(item["decision_type"] == "retry_or_recover" for item in decisions)

    result = main(["replay", "case", "case_session_failure_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    command_completed = [
        event for event in replay["events"] if event["event_type"] == "command.completed"
    ]
    assert len(command_completed) == 1
    assert command_completed[0]["payload"]["exit_code"] == 1


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


def test_cli_evaluates_fixture_suite(capsys, db_path) -> None:
    suite_path = Path(__file__).parent / "fixtures" / "evaluation" / "suite.json"

    result = main(["eval", "fixtures", str(suite_path), "--json"])
    assert result == 0
    report = json.loads(capsys.readouterr().out)
    assert report["total_cases"] == 3
    assert report["failed_cases"] == 0
    assert report["passed_cases"] == 3
