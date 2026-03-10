from __future__ import annotations

import subprocess
from pathlib import Path


def _git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True)


def test_branch_freshness_script_passes_when_head_contains_base(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    script = repo_root / "scripts" / "check_branch_freshness.py"

    _git(tmp_path, "init", "-b", "main")
    _git(tmp_path, "config", "user.name", "Test User")
    _git(tmp_path, "config", "user.email", "test@example.com")
    (tmp_path / "README.md").write_text("base\n", encoding="utf-8")
    _git(tmp_path, "add", "README.md")
    _git(tmp_path, "commit", "-m", "base")
    _git(tmp_path, "remote", "add", "upstream", str(tmp_path))
    _git(tmp_path, "fetch", "upstream")

    result = subprocess.run(
        ["python3", str(script), "--base-ref", "upstream/main"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "Branch freshness check passed" in result.stdout


def test_branch_freshness_script_fails_when_branch_is_behind_base(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    script = repo_root / "scripts" / "check_branch_freshness.py"

    _git(tmp_path, "init", "-b", "main")
    _git(tmp_path, "config", "user.name", "Test User")
    _git(tmp_path, "config", "user.email", "test@example.com")
    (tmp_path / "README.md").write_text("base\n", encoding="utf-8")
    _git(tmp_path, "add", "README.md")
    _git(tmp_path, "commit", "-m", "base")

    # Create a bare upstream remote with one extra commit so the local branch becomes stale.
    upstream_remote = tmp_path / "upstream.git"
    _git(tmp_path, "clone", "--bare", str(tmp_path), str(upstream_remote))
    _git(tmp_path, "remote", "add", "upstream", str(upstream_remote))
    _git(tmp_path, "push", "upstream", "main")

    worktree = tmp_path / "upstream-worktree"
    _git(tmp_path, "clone", str(upstream_remote), str(worktree))
    _git(worktree, "config", "user.name", "Test User")
    _git(worktree, "config", "user.email", "test@example.com")
    (worktree / "README.md").write_text("base\nupstream change\n", encoding="utf-8")
    _git(worktree, "add", "README.md")
    _git(worktree, "commit", "-m", "upstream change")
    _git(worktree, "push", "origin", "main")
    _git(tmp_path, "fetch", "upstream")

    result = subprocess.run(
        ["python3", str(script), "--base-ref", "upstream/main"],
        cwd=tmp_path,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "does not contain the latest upstream/main" in result.stdout
