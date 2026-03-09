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

    result = main(["replay", "case", "case_cli", "--json"])
    assert result == 0
    replay = json.loads(capsys.readouterr().out)
    assert replay["case"]["case_id"] == "case_cli"
    assert replay["summary"] == "done"


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
