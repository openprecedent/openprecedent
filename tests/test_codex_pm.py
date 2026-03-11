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
    assert (tmp_path / ".codex" / "pm" / "issue-state").exists()


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
    assert next_task["task_type"] == "implementation"

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
    assert "## Task Type" in issue_body
    assert "implementation" in issue_body

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


def test_codex_pm_task_new_supports_explicit_task_type(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "real-history-quality",
                "research-framework",
                "--title",
                "Define research framework",
                "--issue",
                "100",
                "--task-type",
                "umbrella",
            ]
        )
        == 0
    )
    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "research-framework.md"
    document = task_path.read_text(encoding="utf-8")

    assert "task_type: umbrella" in document


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


def test_codex_pm_verify_pr_closure_sync_fails_for_umbrella_task_type(
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
                "research-framework",
                "--title",
                "Define research framework",
                "--issue",
                "100",
                "--task-type",
                "umbrella",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "research-framework.md"
    assert (
        main(
            [
                "verify-pr-closure-sync",
                "--pr-body",
                "Closes #100",
                "--changed-file",
                str(task_path.relative_to(tmp_path)),
            ]
        )
        == 1
    )
    assert "task_type=umbrella and must remain open" in capsys.readouterr().err


def test_codex_pm_pr_body_omits_closing_clause_for_umbrella_task(tmp_path: Path, monkeypatch, capsys) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["init"]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "task-new",
                "real-history-quality",
                "research-framework",
                "--title",
                "Define research framework",
                "--issue",
                "100",
                "--task-type",
                "umbrella",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "research-framework.md"
    assert main(["pr-body", str(task_path)]) == 0
    pr_body = capsys.readouterr().out

    assert "Closes #100" not in pr_body


def test_codex_pm_pr_create_uses_explicit_upstream_repo_and_fork_head(
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
                "pr-targeting",
                "--title",
                "Harden PR targeting",
                "--issue",
                "136",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "pr-targeting.md"

    calls: list[list[str]] = []
    captured_body: dict[str, str] = {}

    def fake_run(cmd: list[str], check: bool, capture_output: bool, text: bool):
        calls.append(cmd)
        if cmd == ["git", "branch", "--show-current"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="codex/harden-pr-targeting\n", stderr="")
        if cmd == ["git", "remote", "get-url", "origin"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="git@github.com:yaoyinnan/openprecedent.git\n", stderr="")
        if cmd == ["git", "remote", "get-url", "upstream"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="https://github.com/openprecedent/openprecedent.git\n", stderr="")
        if cmd[:3] == ["gh", "pr", "create"]:
            body_path = Path(cmd[cmd.index("--body-file") + 1])
            captured_body["value"] = body_path.read_text(encoding="utf-8")
            return subprocess.CompletedProcess(cmd, 0, stdout="https://github.com/openprecedent/openprecedent/pull/999\n", stderr="")
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert (
        main(
            [
                "pr-create",
                str(task_path),
                "--tests",
                "PYTHONPATH=src .venv/bin/pytest tests/test_codex_pm.py",
            ]
        )
        == 0
    )
    output = capsys.readouterr().out

    assert "https://github.com/openprecedent/openprecedent/pull/999" in output
    gh_call = next(cmd for cmd in calls if cmd[:3] == ["gh", "pr", "create"])
    assert "--repo" in gh_call
    assert gh_call[gh_call.index("--repo") + 1] == "openprecedent/openprecedent"
    assert gh_call[gh_call.index("--head") + 1] == "yaoyinnan:codex/harden-pr-targeting"
    assert gh_call[gh_call.index("--base") + 1] == "main"
    assert "--body-file" in gh_call
    assert "--body" not in gh_call
    assert "Closes #136" in captured_body["value"]
    assert "- `PYTHONPATH=src .venv/bin/pytest tests/test_codex_pm.py`" in captured_body["value"]
    assert "\\n" not in captured_body["value"]


def test_codex_pm_pr_create_body_file_preserves_clean_closing_reference(
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
                "closing-reference-preservation",
                "--title",
                "Preserve valid GitHub closing references in generated PR bodies",
                "--issue",
                "146",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = (
        tmp_path
        / ".codex"
        / "pm"
        / "tasks"
        / "real-history-quality"
        / "closing-reference-preservation.md"
    )

    captured_body: dict[str, str] = {}

    def fake_run(cmd: list[str], check: bool, capture_output: bool, text: bool):
        if cmd == ["git", "branch", "--show-current"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="codex/closing-reference-preservation\n", stderr="")
        if cmd == ["git", "remote", "get-url", "origin"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="git@github.com:yaoyinnan/openprecedent.git\n", stderr="")
        if cmd == ["git", "remote", "get-url", "upstream"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="https://github.com/openprecedent/openprecedent.git\n", stderr="")
        if cmd[:3] == ["gh", "pr", "create"]:
            body_path = Path(cmd[cmd.index("--body-file") + 1])
            captured_body["value"] = body_path.read_text(encoding="utf-8")
            return subprocess.CompletedProcess(cmd, 0, stdout="https://github.com/openprecedent/openprecedent/pull/1000\n", stderr="")
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert main(["pr-create", str(task_path), "--tests", "echo done"]) == 0
    body = captured_body["value"]

    assert body.splitlines()[0] == "Closes #146"
    assert body.splitlines()[-1] == "- `echo done`"
    assert "\n\nValidation:\n- `echo done`" in body
    assert "\\nCloses #146" not in body


def test_codex_pm_pr_create_fails_when_origin_owner_is_ambiguous(
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
                "pr-targeting",
                "--title",
                "Harden PR targeting",
                "--issue",
                "136",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "pr-targeting.md"

    def fake_run(cmd: list[str], check: bool, capture_output: bool, text: bool):
        if cmd == ["git", "branch", "--show-current"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="codex/harden-pr-targeting\n", stderr="")
        if cmd == ["git", "remote", "get-url", "origin"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="ssh://internal.example/openprecedent.git\n", stderr="")
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert main(["pr-create", str(task_path)]) == 1
    assert "could not derive the fork owner from the origin remote" in capsys.readouterr().err


def test_codex_pm_pr_create_fails_when_upstream_repo_does_not_match(
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
                "pr-targeting",
                "--title",
                "Harden PR targeting",
                "--issue",
                "136",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "pr-targeting.md"

    def fake_run(cmd: list[str], check: bool, capture_output: bool, text: bool):
        if cmd == ["git", "branch", "--show-current"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="codex/harden-pr-targeting\n", stderr="")
        if cmd == ["git", "remote", "get-url", "origin"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="git@github.com:yaoyinnan/openprecedent.git\n", stderr="")
        if cmd == ["git", "remote", "get-url", "upstream"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="https://github.com/someone-else/openprecedent.git\n", stderr="")
        raise AssertionError(f"unexpected command: {cmd}")

    monkeypatch.setattr(subprocess, "run", fake_run)

    assert main(["pr-create", str(task_path)]) == 1
    assert "upstream remote points to someone-else/openprecedent" in capsys.readouterr().err


def test_codex_pm_issue_state_init_creates_state_doc_and_updates_task(
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
                "issue-scoped-dev-state",
                "--title",
                "Capture issue-scoped development state",
                "--issue",
                "106",
                "--status",
                "in_progress",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "issue-scoped-dev-state.md"
    assert main(["issue-state-init", str(task_path)]) == 0
    state_path = (tmp_path / capsys.readouterr().out.strip()).resolve()

    assert state_path == (tmp_path / ".codex" / "pm" / "issue-state" / "106-issue-scoped-dev-state.md").resolve()
    assert state_path.exists()
    task_document = task_path.read_text(encoding="utf-8")
    assert "state_path: .codex/pm/issue-state/106-issue-scoped-dev-state.md" in task_document


def test_codex_pm_issue_state_check_fails_for_in_progress_issue_without_state(
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
                "issue-scoped-dev-state",
                "--title",
                "Capture issue-scoped development state",
                "--issue",
                "106",
                "--status",
                "in_progress",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert main(["issue-state-check", "--branch", "codex/issue-106-issue-scoped-dev-state"]) == 1
    assert "in-progress issue has no state document" in capsys.readouterr().err


def test_codex_pm_issue_state_check_passes_after_state_init(
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
                "issue-scoped-dev-state",
                "--title",
                "Capture issue-scoped development state",
                "--issue",
                "106",
                "--status",
                "in_progress",
            ]
        )
        == 0
    )
    capsys.readouterr()

    task_path = tmp_path / ".codex" / "pm" / "tasks" / "real-history-quality" / "issue-scoped-dev-state.md"
    assert main(["issue-state-init", str(task_path)]) == 0
    capsys.readouterr()

    assert main(["issue-state-check", "--branch", "codex/issue-106-issue-scoped-dev-state"]) == 0
    assert "Issue state check passed" in capsys.readouterr().out
