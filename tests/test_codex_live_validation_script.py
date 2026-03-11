from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def test_codex_live_validation_script_records_multiple_invocations(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env["OPENPRECEDENT_CODEX_LIVE_ROOT"] = str(tmp_path / "codex-live")
    env["OPENPRECEDENT_CODEX_LIVE_RESET"] = "1"
    env["OPENPRECEDENT_CODEX_LIVE_AUTO_RUN"] = "1"
    env["PYTHONPATH"] = str(repo_root / "src")

    result = subprocess.run(
        ["./scripts/run-codex-live-validation.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    output_root = Path(env["OPENPRECEDENT_CODEX_LIVE_ROOT"]) / "output"
    manifest = json.loads((output_root / "manifest.json").read_text(encoding="utf-8"))
    invocation_list = json.loads((output_root / "20-invocation-list.json").read_text(encoding="utf-8"))
    summary = json.loads((output_root / "21-latest-invocation-summary.json").read_text(encoding="utf-8"))
    inspection = json.loads((output_root / "22-latest-invocation-inspection.json").read_text(encoding="utf-8"))

    assert manifest["auto_run"] is True
    assert manifest["runtime_home"] == str(Path(env["OPENPRECEDENT_CODEX_LIVE_ROOT"]) / "runtime-home")
    assert len(invocation_list) == 3
    assert summary["invocation_count"] == 3
    assert summary["latest_query_reason"] == "after_failure"
    assert summary["latest_matched_case_ids"]
    assert inspection["invocation"]["query_reason"] == "after_failure"
    assert (Path(env["OPENPRECEDENT_CODEX_LIVE_ROOT"]) / "prompts" / "01-initial-planning.txt").exists()
    assert (Path(env["OPENPRECEDENT_CODEX_LIVE_ROOT"]) / "next-steps.txt").exists()
