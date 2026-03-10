from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def test_run_e2e_script_completes_and_writes_expected_outputs(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env["OPENPRECEDENT_E2E_ROOT"] = str(tmp_path / "journey")
    env["PYTHONPATH"] = str(repo_root / "src")

    result = subprocess.run(
        ["./scripts/run-e2e.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    output_root = Path(env["OPENPRECEDENT_E2E_ROOT"]) / "output"
    assert (output_root / "01-list-openclaw-sessions.json").exists()
    assert (output_root / "10-eval-fixtures.json").exists()
    assert (output_root / "11-eval-collected-openclaw-sessions.json").exists()

    listed_sessions = json.loads((output_root / "01-list-openclaw-sessions.json").read_text(encoding="utf-8"))
    assert [item["session_id"] for item in listed_sessions] == [
        "file-ops-session",
        "search-read-session",
        "sample-session",
    ]

    fixture_report = json.loads((output_root / "10-eval-fixtures.json").read_text(encoding="utf-8"))
    assert fixture_report["failed_cases"] == 0

    collected_report = json.loads(
        (output_root / "11-eval-collected-openclaw-sessions.json").read_text(encoding="utf-8")
    )
    assert collected_report["evaluated_cases"] == 1


def test_merge_validation_doc_references_standard_e2e_script() -> None:
    path = Path(__file__).parent.parent / "docs" / "engineering" / "merge-validation.md"

    content = path.read_text(encoding="utf-8")

    assert "./scripts/run-e2e.sh" in content
    assert "When To Run It" in content
