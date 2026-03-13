from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def _python_bin(repo_root: Path) -> Path:
    candidate = repo_root / ".venv" / "bin" / "python"
    if candidate.exists():
        return candidate
    return repo_root.parent / "openprecedent" / ".venv" / "bin" / "python"


def _openprecedent_bin(repo_root: Path) -> Path:
    release_candidate = repo_root / "target" / "release" / "openprecedent"
    if release_candidate.exists():
        return release_candidate
    debug_candidate = repo_root / "target" / "debug" / "openprecedent"
    if debug_candidate.exists():
        return debug_candidate
    subprocess.run(
        ["cargo", "build", "-q", "-p", "openprecedent-cli"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return debug_candidate


def _write_round_files(repo_root: Path, issue: int, title: str) -> tuple[Path, Path]:
    slug = title.lower().replace(" ", "-")
    task_path = repo_root / ".codex" / "pm" / "tasks" / "product-direction" / f"{slug}.md"
    state_path = repo_root / ".codex" / "pm" / "issue-state" / f"{issue}-{slug}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        "\n".join(
            [
                "---",
                "type: task",
                "epic: product-direction",
                f"slug: {slug}",
                f"title: {title}",
                "status: done",
                "task_type: implementation",
                "labels: feature,test",
                f"issue: {issue}",
                f"state_path: {state_path.relative_to(repo_root)}",
                "---",
                "",
                "## Deliverable",
                "",
                title,
                "",
                "## Scope",
                "",
                "- keep the change narrow",
                "- keep operator-facing behavior explicit",
                "",
                "## Acceptance Criteria",
                "",
                "- the round is completed",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    state_path.write_text(
        "\n".join(
            [
                "---",
                "type: issue_state",
                f"issue: {issue}",
                f"task: {task_path.relative_to(repo_root)}",
                f"title: {title}",
                "status: done",
                "---",
                "",
                "## Summary",
                "",
                title,
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return task_path, state_path


def _commit_round(repo_root: Path, issue: int, title: str, touched_file: str) -> None:
    file_path = repo_root / touched_file
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(f"{title}\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=repo_root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", title], cwd=repo_root, check=True, capture_output=True, text=True)


def _init_fake_harnesshub_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "HarnessHub"
    repo_root.mkdir()
    subprocess.run(["git", "init", "-b", "main"], cwd=repo_root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "codex@example.com"], cwd=repo_root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.name", "Codex"], cwd=repo_root, check=True, capture_output=True, text=True)
    (repo_root / "README.md").write_text("# HarnessHub\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo_root, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "bootstrap"], cwd=repo_root, check=True, capture_output=True, text=True)
    return repo_root


def test_sync_harnesshub_shared_runtime_backfills_and_imports_new_rounds(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    python_bin = _python_bin(repo_root)
    fake_repo = _init_fake_harnesshub_repo(tmp_path)

    _write_round_files(fake_repo, 53, "Refine verification into explicit readiness classes")
    _commit_round(fake_repo, 53, "Refine verification into explicit readiness classes", "src/readiness.txt")
    _write_round_files(fake_repo, 59, "Close the inspect-to-export operator workflow")
    _commit_round(fake_repo, 59, "Close the inspect-to-export operator workflow", "src/inspect.txt")

    runtime_home = tmp_path / "runtime"
    result = subprocess.run(
        [
            str(python_bin),
            str(repo_root / "scripts" / "sync_harnesshub_shared_runtime.py"),
            "--repo-root",
            str(fake_repo),
            "--runtime-home",
            str(runtime_home),
            "--python-bin",
            str(python_bin),
            "--export-output-root",
            str(tmp_path / "bundles"),
        ],
        cwd=repo_root,
        env={**os.environ, "PYTHONPATH": str(repo_root / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    summary = json.loads(result.stdout)
    assert summary["imported_count"] == 2
    assert summary["db_counts"]["cases"] == 2
    assert summary["db_counts"]["events"] > 0
    assert summary["db_counts"]["decisions"] > 0

    _write_round_files(fake_repo, 61, "Add remediation guidance to verify readiness output")
    _commit_round(fake_repo, 61, "Add remediation guidance to verify readiness output", "src/remediation.txt")

    second = subprocess.run(
        [
            str(python_bin),
            str(repo_root / "scripts" / "sync_harnesshub_shared_runtime.py"),
            "--repo-root",
            str(fake_repo),
            "--runtime-home",
            str(runtime_home),
            "--python-bin",
            str(python_bin),
            "--export-output-root",
            str(tmp_path / "bundles"),
        ],
        cwd=repo_root,
        env={**os.environ, "PYTHONPATH": str(repo_root / "src")},
        capture_output=True,
        text=True,
        check=True,
    )
    second_summary = json.loads(second.stdout)
    assert second_summary["imported_count"] == 1
    assert second_summary["skipped_existing_count"] == 2
    assert second_summary["db_counts"]["cases"] == 3


def test_harnesshub_workflow_auto_syncs_before_brief_query(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    python_bin = _python_bin(repo_root)
    openprecedent_bin = _openprecedent_bin(repo_root)
    fake_repo = _init_fake_harnesshub_repo(tmp_path)

    _write_round_files(fake_repo, 53, "Refine verification into explicit readiness classes")
    _commit_round(fake_repo, 53, "Refine verification into explicit readiness classes", "src/readiness.txt")

    runtime_home = tmp_path / "runtime"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    env["OPENPRECEDENT_HOME"] = str(runtime_home)
    env["OPENPRECEDENT_PYTHON_BIN"] = str(python_bin)
    env["OPENPRECEDENT_HARNESSHUB_REPO_ROOT"] = str(fake_repo)
    env["OPENPRECEDENT_HARNESSHUB_SYNC_SUMMARY_PATH"] = str(tmp_path / "sync-summary.json")
    env["OPENPRECEDENT_BIN"] = str(openprecedent_bin)

    result = subprocess.run(
        [
            "./scripts/run-harnesshub-decision-lineage-workflow.sh",
            "--query-reason",
            "before_file_write",
            "--task-summary",
            "Replace a yes/no readiness signal with operator-facing stages that explain what extra setup reused images still need.",
        ],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    brief = json.loads(result.stdout)
    sync_summary = json.loads(Path(env["OPENPRECEDENT_HARNESSHUB_SYNC_SUMMARY_PATH"]).read_text(encoding="utf-8"))
    assert brief["matched_cases"]
    assert sync_summary["imported_count"] == 1
    assert sync_summary["db_counts"]["cases"] == 1
