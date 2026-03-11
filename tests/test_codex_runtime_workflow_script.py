from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from openprecedent.config import get_db_path
from openprecedent.services import OpenPrecedentService


def test_codex_runtime_workflow_script_returns_brief_and_logs_invocation(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    fixture_root = repo_root / "tests" / "fixtures"
    runtime_home = tmp_path / "runtime-home"
    runtime_home.mkdir()

    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    env["OPENPRECEDENT_HOME"] = str(runtime_home)
    env["OPENPRECEDENT_PYTHON_BIN"] = str(repo_root / ".venv" / "bin" / "python")
    old_home = os.environ.get("OPENPRECEDENT_HOME")
    old_db = os.environ.get("OPENPRECEDENT_DB")
    os.environ["OPENPRECEDENT_HOME"] = str(runtime_home)
    os.environ.pop("OPENPRECEDENT_DB", None)
    try:
        service = OpenPrecedentService.from_path(get_db_path())
        for case_id, title, filename in (
            ("case_codex_precedent_current", "Current Codex docs-only recommendation", "codex_rollout_precedent_current.jsonl"),
            ("case_codex_precedent_semantic", "Semantic Codex docs-only precedent", "codex_rollout_precedent_semantic_match.jsonl"),
        ):
            service.import_codex_rollout_jsonl(
                fixture_root / filename,
                case_id=case_id,
                title=title,
                user_id="u1",
            )
            service.extract_decisions(case_id)
    finally:
        if old_home is None:
            os.environ.pop("OPENPRECEDENT_HOME", None)
        else:
            os.environ["OPENPRECEDENT_HOME"] = old_home
        if old_db is None:
            os.environ.pop("OPENPRECEDENT_DB", None)
        else:
            os.environ["OPENPRECEDENT_DB"] = old_db

    result = subprocess.run(
        [
            "./scripts/run-codex-decision-lineage-workflow.sh",
            "--query-reason",
            "initial_planning",
            "--task-summary",
            "Do not edit code. Provide a short written recommendation only and keep it consistent with earlier Codex runtime decisions.",
        ],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    brief = json.loads(result.stdout)
    assert brief["matched_cases"]
    assert "case_codex_precedent_semantic" in [item["case_id"] for item in brief["matched_cases"]]
    assert brief["accepted_constraints"]

    list_result = subprocess.run(
        [
            str(repo_root / ".venv" / "bin" / "python"),
            "-c",
            "from openprecedent.cli import run; run()",
            "runtime",
            "list-decision-lineage-invocations",
        ],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    invocations = json.loads(list_result.stdout)
    assert invocations
    assert invocations[0]["query_reason"] == "initial_planning"

    inspect_result = subprocess.run(
        [
            "./scripts/run-codex-decision-lineage-workflow.sh",
            "--inspect-latest",
            "--query-reason",
            "before_file_write",
            "--task-summary",
            "Do not edit code. Provide a short written recommendation only and keep it consistent with earlier Codex runtime decisions.",
            "--candidate-action",
            "Edit docs/engineering/codex-runtime-boundary.md",
        ],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    assert '"invocation"' in inspect_result.stdout
    assert '"query_reason": "before_file_write"' in inspect_result.stdout
