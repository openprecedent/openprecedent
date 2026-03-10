from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def test_live_validation_script_prepares_workspace_and_summary(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env["OPENPRECEDENT_LIVE_ROOT"] = str(tmp_path / "live")
    env["PYTHONPATH"] = str(repo_root / "src")

    result = subprocess.run(
        ["./scripts/run-openclaw-live-validation.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    live_root = Path(env["OPENPRECEDENT_LIVE_ROOT"])
    output_root = live_root / "output"
    manifest = json.loads((output_root / "manifest.json").read_text(encoding="utf-8"))
    summary = json.loads((output_root / "03-invocation-summary.json").read_text(encoding="utf-8"))

    assert manifest["profile"] == "opv80"
    assert manifest["runtime_home"] == str(live_root / "runtime-home")
    assert (live_root / "launch-openclaw-gateway.sh").exists()
    assert (live_root / "next-steps.txt").exists()
    assert (live_root / "prompt.txt").exists()
    assert summary["invocation_count"] == 0


def test_live_validation_script_seeds_history_and_summarizes_invocations(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env["OPENPRECEDENT_LIVE_ROOT"] = str(tmp_path / "live")
    env["OPENPRECEDENT_LIVE_RESET"] = "1"
    env["OPENPRECEDENT_LIVE_SEED_SESSION_FILE"] = str(
        repo_root / "tests" / "fixtures" / "openclaw_sessions" / "search-read-session.jsonl"
    )
    env["OPENPRECEDENT_LIVE_SEED_SESSION_ID"] = "search-read-session"
    env["OPENPRECEDENT_LIVE_SEED_CASE_ID"] = "case_live_seed_search_read"
    env["PYTHONPATH"] = str(repo_root / "src")

    first_run = subprocess.run(
        ["./scripts/run-openclaw-live-validation.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert first_run.returncode == 0, first_run.stderr
    output_root = Path(env["OPENPRECEDENT_LIVE_ROOT"]) / "output"
    assert (output_root / "01-seed-import.json").exists()
    assert (output_root / "02-seed-extract.json").exists()

    invocation_log = Path(env["OPENPRECEDENT_LIVE_ROOT"]) / "runtime-home" / "openprecedent-runtime-invocations.jsonl"
    invocation_log.write_text(
        json.dumps(
            {
                "invocation_id": "rtinv_demo",
                "recorded_at": "2026-03-11T10:00:00Z",
                "query_reason": "initial_planning",
                "matched_case_ids": ["case_live_seed_search_read"],
                "task_summary": "Use prior history before recommending repository navigation changes.",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    second_run = subprocess.run(
        ["./scripts/run-openclaw-live-validation.sh"],
        cwd=repo_root,
        env={**env, "OPENPRECEDENT_LIVE_RESET": "0"},
        capture_output=True,
        text=True,
        check=False,
    )

    assert second_run.returncode == 0, second_run.stderr
    summary = json.loads((output_root / "03-invocation-summary.json").read_text(encoding="utf-8"))
    assert summary["invocation_count"] == 1
    assert summary["latest_matched_case_ids"] == ["case_live_seed_search_read"]
    assert "Seed prior history already initialized" in second_run.stdout


def test_tooling_doc_references_live_validation_harness() -> None:
    repo_root = Path(__file__).parent.parent
    content = (repo_root / "docs" / "engineering" / "tooling-setup.md").read_text(encoding="utf-8")

    assert "./scripts/run-openclaw-live-validation.sh" in content
    assert "Issue-Scoped Development State" in content
