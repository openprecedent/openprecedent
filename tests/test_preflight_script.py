from __future__ import annotations

import os
import subprocess
from pathlib import Path


def test_preflight_script_fails_without_codex_review(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env["OPENPRECEDENT_REVIEW_FILE"] = str(tmp_path / ".codex-review")
    env["OPENPRECEDENT_PYTHON_BIN"] = str(repo_root / ".venv" / "bin" / "python")
    env["OPENPRECEDENT_PREFLIGHT_BASE_REF"] = "HEAD"

    result = subprocess.run(
        ["./scripts/run-agent-preflight.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "missing .codex-review" in result.stdout


def test_preflight_script_runs_and_skips_markdownlint_when_unavailable(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    review_file = tmp_path / ".codex-review"
    review_file.write_text(
        "scope reviewed: preflight script\nfindings: no findings\nremaining risks: markdownlint unavailable locally\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["OPENPRECEDENT_REVIEW_FILE"] = str(review_file)
    env["OPENPRECEDENT_PYTHON_BIN"] = str(repo_root / ".venv" / "bin" / "python")
    env["PATH"] = "/usr/bin:/bin"
    env["OPENPRECEDENT_PREFLIGHT_BASE_REF"] = "HEAD"

    result = subprocess.run(
        ["./scripts/run-agent-preflight.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Skipping markdownlint" in result.stdout
    assert "Agent preflight passed." in result.stdout
