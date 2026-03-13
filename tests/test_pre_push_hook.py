from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


def _prepare_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-b", "main")
    _git(repo, "config", "user.name", "Test User")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "remote", "add", "origin", "git@github.com:test/openprecedent.git")

    source_root = Path(__file__).parent.parent

    hook_path = repo / ".githooks" / "pre-push"
    hook_path.parent.mkdir(parents=True, exist_ok=True)
    hook_path.write_text((source_root / ".githooks" / "pre-push").read_text(encoding="utf-8"), encoding="utf-8")
    hook_path.chmod(0o755)

    src_pkg = repo / "src" / "openprecedent"
    src_pkg.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_root / "src" / "openprecedent" / "codex_pm.py", src_pkg / "codex_pm.py")
    (src_pkg / "__init__.py").write_text("", encoding="utf-8")

    task_path = repo / ".codex" / "pm" / "tasks" / "test-epic" / "sample-task.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        """---
type: task
epic: test-epic
slug: sample-task
title: Sample task
status: in_progress
labels: feature
issue: 999
---

## Context

Test task.
""",
        encoding="utf-8",
    )

    (repo / "README.md").write_text("base\n", encoding="utf-8")
    _git(repo, "add", ".")
    _git(repo, "commit", "-m", "base")

    _git(repo, "checkout", "-b", "feature")
    task_path.write_text(task_path.read_text(encoding="utf-8") + "\nMore task body.\n", encoding="utf-8")
    _git(repo, "add", str(task_path.relative_to(repo)))
    _git(repo, "commit", "-m", "update task")

    head_sha = _git(repo, "rev-parse", "HEAD").stdout.strip()
    proof_file = repo / ".codex-review-proof"
    proof_file.write_text(
        f"branch=feature\nhead_sha={head_sha}\nbase_ref=main\ngenerated_at=2026-03-11T00:00:00Z\n",
        encoding="utf-8",
    )

    review_file = repo / ".codex-review"
    review_file.write_text(
        "scope reviewed: pre-push hook\nfindings: no findings\nremaining risks: local closure sync test only\n",
        encoding="utf-8",
    )

    return repo


def _write_fake_gh(bin_dir: Path, *, pr_body: str) -> Path:
    script = bin_dir / "gh"
    script.write_text(
        f"""#!/usr/bin/env bash
set -euo pipefail
if [[ "$1" == "pr" && "$2" == "list" ]]; then
  echo '[]'
  exit 0
fi
if [[ "$1" == "pr" && "$2" == "view" ]]; then
  printf '%s' {pr_body!r}
  exit 0
fi
echo "unexpected gh invocation: $*" >&2
exit 1
""",
        encoding="utf-8",
    )
    script.chmod(0o755)
    return script


def test_pre_push_hook_blocks_local_closure_sync_mismatch(tmp_path: Path) -> None:
    repo = _prepare_repo(tmp_path)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    _write_fake_gh(fake_bin, pr_body="Closes #999")

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    env["BYPASS_BRANCH_FRESHNESS_CHECK"] = "1"
    env["OPENPRECEDENT_BASE_REF"] = "main"
    env["OPENPRECEDENT_PYTHON_BIN"] = "python3"

    result = subprocess.run(
        [str(repo / ".githooks" / "pre-push")],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "matching task file is not marked done" in result.stderr


def test_pre_push_hook_skips_local_closure_sync_when_pr_body_is_unavailable(tmp_path: Path) -> None:
    repo = _prepare_repo(tmp_path)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    _write_fake_gh(fake_bin, pr_body="")

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    env["BYPASS_BRANCH_FRESHNESS_CHECK"] = "1"
    env["OPENPRECEDENT_BASE_REF"] = "main"
    env["OPENPRECEDENT_PYTHON_BIN"] = "python3"

    result = subprocess.run(
        [str(repo / ".githooks" / "pre-push")],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Skipping local closure sync check: PR body is unavailable" in result.stdout
    assert "Codex review note detected." in result.stdout


def test_pre_push_hook_blocks_missing_review_proof(tmp_path: Path) -> None:
    repo = _prepare_repo(tmp_path)
    (repo / ".codex-review-proof").unlink()
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    _write_fake_gh(fake_bin, pr_body="")

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    env["BYPASS_BRANCH_FRESHNESS_CHECK"] = "1"
    env["OPENPRECEDENT_BASE_REF"] = "main"
    env["OPENPRECEDENT_PYTHON_BIN"] = "python3"

    result = subprocess.run(
        [str(repo / ".githooks" / "pre-push")],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "missing .codex-review-proof" in result.stdout


def test_pre_push_hook_blocks_stale_review_proof(tmp_path: Path) -> None:
    repo = _prepare_repo(tmp_path)
    (repo / ".codex-review-proof").write_text(
        "branch=feature\nhead_sha=deadbeef\nbase_ref=main\ngenerated_at=2026-03-11T00:00:00Z\n",
        encoding="utf-8",
    )
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    _write_fake_gh(fake_bin, pr_body="")

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    env["BYPASS_BRANCH_FRESHNESS_CHECK"] = "1"
    env["OPENPRECEDENT_BASE_REF"] = "main"
    env["OPENPRECEDENT_PYTHON_BIN"] = "python3"

    result = subprocess.run(
        [str(repo / ".githooks" / "pre-push")],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "does not match the current HEAD" in result.stdout


def test_pre_push_hook_runs_rust_tests_when_forced(tmp_path: Path) -> None:
    repo = _prepare_repo(tmp_path)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    _write_fake_gh(fake_bin, pr_body="")
    cargo_log = tmp_path / "cargo.log"
    cargo_script = fake_bin / "cargo"
    cargo_script.write_text(
        f"#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >> {str(cargo_log)!r}\nexit 0\n",
        encoding="utf-8",
    )
    cargo_script.chmod(0o755)

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}:{env['PATH']}"
    env["BYPASS_BRANCH_FRESHNESS_CHECK"] = "1"
    env["OPENPRECEDENT_BASE_REF"] = "main"
    env["OPENPRECEDENT_PYTHON_BIN"] = "python3"
    env["OPENPRECEDENT_FORCE_RUST_TESTS"] = "1"

    result = subprocess.run(
        [str(repo / ".githooks" / "pre-push")],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Running Rust tests" in result.stdout
    assert cargo_log.read_text(encoding="utf-8").strip() == "test"
