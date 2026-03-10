from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from openprecedent.codex_pm import main


def test_codex_pm_init_creates_workspace(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    result = main(["init"])

    assert result == 0
    assert (tmp_path / ".codex" / "pm" / "prds").exists()
    assert (tmp_path / ".codex" / "pm" / "epics").exists()
    assert (tmp_path / ".codex" / "pm" / "tasks").exists()


def test_codex_pm_module_invocation_runs_cli(tmp_path: Path) -> None:
    repo_root = Path("/workspace/02-projects/incubation/openprecedent")
    result = subprocess.run(
        [sys.executable, "-m", "openprecedent.codex_pm", "init"],
        cwd=tmp_path,
        env={"PYTHONPATH": str(repo_root / "src")},
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (tmp_path / ".codex" / "pm" / "prds").exists()


def test_codex_pm_scaffolds_and_selects_next_task(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    capsys.readouterr()
    assert main(["prd-new", "runtime-validation", "--title", "Runtime validation"]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "epic-new",
                "runtime-validation",
                "--title",
                "Runtime validation",
                "--prd",
                "runtime-validation",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "runtime-validation",
                "collector-rollout",
                "--title",
                "Roll out collector",
                "--issue",
                "23",
                "--labels",
                "feature,ops",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "runtime-validation",
                "quality-pass",
                "--title",
                "Inspect collected session quality",
                "--issue",
                "26",
                "--status",
                "done",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert main(["next", "--json"]) == 0
    next_task = json.loads(capsys.readouterr().out)
    assert next_task["title"] == "Roll out collector"
    assert next_task["issue"] == "23"

    assert main(["tasks", "--json"]) == 0
    tasks = json.loads(capsys.readouterr().out)
    assert len(tasks) == 2


def test_codex_pm_updates_status_and_renders_issue_and_pr_body(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "runtime-validation" / "collector-rollout.md"
    assert main(["init"]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "runtime-validation",
                "collector-rollout",
                "--title",
                "Roll out collector",
                "--issue",
                "23",
                "--labels",
                "feature,ops",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_text = task_path.read_text(encoding="utf-8")
    task_text = task_text.replace("## Context\n\n", "## Context\n\nCollector rollout still needs a real target host.\n\n")
    task_text = task_text.replace("## Deliverable\n\n", "## Deliverable\n\nRun the collector on a real schedule.\n\n")
    task_text = task_text.replace("## Scope\n\n- \n\n", "## Scope\n\n- install the scheduled collector\n- validate cursor advance\n\n")
    task_text = task_text.replace(
        "## Acceptance Criteria\n\n- \n\n",
        "## Acceptance Criteria\n\n- repeated runs do not duplicate sessions\n\n",
    )
    task_text = task_text.replace(
        "## Validation\n\n- \n\n",
        "## Validation\n\n- .venv/bin/python -m pytest tests/test_api.py tests/test_cli.py\n\n",
    )
    task_text = task_text.replace(
        "## Implementation Notes\n\n",
        "## Implementation Notes\n\nUse the systemd timer path for the first rollout.\n\n",
    )
    task_path.write_text(task_text, encoding="utf-8")

    assert main(["blocked", str(task_path), "--reason", "waiting on host access"]) == 0
    capsys.readouterr()
    assert main(["set-status", str(task_path), "in_progress"]) == 0
    capsys.readouterr()

    assert main(["issue-body", str(task_path)]) == 0
    issue_body = capsys.readouterr().out
    assert "## Context" in issue_body
    assert "Collector rollout still needs a real target host." in issue_body
    assert "## Acceptance Criteria" in issue_body

    assert (
        main(
            [
                "pr-body",
                str(task_path),
                "--issue",
                "23",
                "--tests",
                ".venv/bin/python -m pytest tests/test_api.py tests/test_cli.py",
            ]
        )
        == 0
    )
    pr_body = capsys.readouterr().out
    assert "Closes #23" in pr_body
    assert "Run the collector on a real schedule." in pr_body
    assert "Validation:" in pr_body


def test_codex_pm_lists_backfilled_tasks(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    capsys.readouterr()
    assert main(["prd-new", "mvp-runtime-validation", "--title", "MVP runtime validation and quality"]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "epic-new",
                "local-runtime-validation",
                "--title",
                "Local runtime validation",
                "--prd",
                "mvp-runtime-validation",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        main(
            [
                "epic-new",
                "real-history-quality",
                "--title",
                "Real history quality",
                "--prd",
                "mvp-runtime-validation",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "local-runtime-validation",
                "collector-rollout",
                "--title",
                "Roll out scheduled OpenClaw collector in a real target environment",
                "--issue",
                "23",
                "--labels",
                "feature,ops",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "real-history-quality",
                "anonymized-real-session-fixtures",
                "--title",
                "Add anonymized real-session fixtures to the evaluation suite",
                "--issue",
                "26",
                "--labels",
                "feature,test",
            ]
        )
        == 0
    )
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "real-history-quality",
                "precedent-ranking-quality",
                "--title",
                "Improve precedent ranking quality on larger real-case history",
                "--issue",
                "28",
                "--labels",
                "feature,test",
                "--depends-on",
                "26",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert main(["tasks", "--json"]) == 0
    tasks = json.loads(capsys.readouterr().out)
    assert len(tasks) == 3

    assert main(["next", "--json"]) == 0
    next_task = json.loads(capsys.readouterr().out)
    assert next_task["issue"] == "23"


def test_codex_pm_verify_pr_closure_sync_passes_when_matching_task_is_done(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "real-history-quality",
                "closure-sync",
                "--title",
                "Enforce task closure sync",
                "--issue",
                "90",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "closure-sync.md"
    assert main(["set-status", str(task_path), "done"]) == 0
    capsys.readouterr()

    assert (
        main(
            [
                "verify-pr-closure-sync",
                "--pr-body",
                "Closes #90",
                "--changed-file",
                str(task_path.relative_to(tmp_path)),
            ]
        )
        == 0
    )
    assert "PR task closure sync passed." in capsys.readouterr().out


def test_codex_pm_verify_pr_closure_sync_fails_when_matching_task_is_missing(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    capsys.readouterr()

    assert (
        main(
            [
                "verify-pr-closure-sync",
                "--pr-body",
                "Closes #90",
                "--changed-file",
                "README.md",
            ]
        )
        == 1
    )
    assert (
        "PR closes #90 but does not update the matching local task file"
        in capsys.readouterr().err
    )


def test_codex_pm_verify_pr_closure_sync_fails_when_matching_task_is_not_done(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "real-history-quality",
                "closure-sync",
                "--title",
                "Enforce task closure sync",
                "--issue",
                "90",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "closure-sync.md"
    assert (
        main(
            [
                "verify-pr-closure-sync",
                "--pr-body",
                "Closes #90",
                "--changed-file",
                str(task_path.relative_to(tmp_path)),
            ]
        )
        == 1
    )
    assert "matching task file is not marked done" in capsys.readouterr().err
