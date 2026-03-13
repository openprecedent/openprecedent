from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_preflight_script_fails_without_codex_review(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env["OPENPRECEDENT_REVIEW_FILE"] = str(tmp_path / ".codex-review")
    env["OPENPRECEDENT_PYTHON_BIN"] = sys.executable
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
    proof_file = tmp_path / ".codex-review-proof"
    head_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    proof_file.write_text(
        f"branch={subprocess.run(['git', 'branch', '--show-current'], cwd=repo_root, capture_output=True, text=True, check=True).stdout.strip()}\n"
        f"head_sha={head_sha}\n"
        "base_ref=HEAD\n"
        "generated_at=2026-03-11T00:00:00Z\n",
        encoding="utf-8",
    )
    review_file.write_text(
        "scope reviewed: preflight script\nfindings: no findings\nremaining risks: markdownlint unavailable locally\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["OPENPRECEDENT_REVIEW_FILE"] = str(review_file)
    env["OPENPRECEDENT_REVIEW_PROOF_FILE"] = str(proof_file)
    env["OPENPRECEDENT_PYTHON_BIN"] = sys.executable
    env["PATH"] = "/usr/bin:/bin"
    env["OPENPRECEDENT_PREFLIGHT_BASE_REF"] = "HEAD"
    env["OPENPRECEDENT_PREFLIGHT_PYTEST_ARGS"] = "tests/test_codex_review_checkpoint.py"

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


def test_preflight_script_fails_without_review_proof(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    review_file = tmp_path / ".codex-review"
    review_file.write_text(
        "scope reviewed: preflight script\nfindings: no findings\nremaining risks: updated after review\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["OPENPRECEDENT_REVIEW_FILE"] = str(review_file)
    env["OPENPRECEDENT_REVIEW_PROOF_FILE"] = str(tmp_path / ".codex-review-proof")
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
    assert "missing .codex-review-proof" in result.stdout


def test_preflight_script_runs_rust_tests_when_forced(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    review_file = tmp_path / ".codex-review"
    proof_file = tmp_path / ".codex-review-proof"
    cargo_log = tmp_path / "cargo.log"
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    cargo_script = fake_bin / "cargo"
    cargo_script.write_text(
        f"#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >> {str(cargo_log)!r}\nexit 0\n",
        encoding="utf-8",
    )
    cargo_script.chmod(0o755)

    head_sha = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    branch_name = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    proof_file.write_text(
        f"branch={branch_name}\nhead_sha={head_sha}\nbase_ref=HEAD\ngenerated_at=2026-03-14T00:00:00Z\n",
        encoding="utf-8",
    )
    review_file.write_text(
        "scope reviewed: preflight rust guardrail\nfindings: no findings\nremaining risks: forced cargo path only\n",
        encoding="utf-8",
    )

    env = os.environ.copy()
    env["OPENPRECEDENT_REVIEW_FILE"] = str(review_file)
    env["OPENPRECEDENT_REVIEW_PROOF_FILE"] = str(proof_file)
    env["OPENPRECEDENT_PYTHON_BIN"] = sys.executable
    env["OPENPRECEDENT_PREFLIGHT_BASE_REF"] = "HEAD"
    env["OPENPRECEDENT_PREFLIGHT_PYTEST_ARGS"] = "tests/test_codex_review_checkpoint.py"
    env["OPENPRECEDENT_FORCE_RUST_TESTS"] = "1"
    env["PATH"] = f"{fake_bin}:{env['PATH']}"

    result = subprocess.run(
        ["./scripts/run-agent-preflight.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Running Rust tests" in result.stdout
    assert cargo_log.read_text(encoding="utf-8").strip() == "test"
