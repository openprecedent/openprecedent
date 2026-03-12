from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from openprecedent.config import get_db_path
from openprecedent.services import CreateCaseInput, OpenPrecedentService


def _git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_export_harnesshub_round_bundle_can_be_imported_and_extracted(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    harnesshub_root = tmp_path / "HarnessHub"
    harnesshub_root.mkdir()

    _git(harnesshub_root, "init")
    _git(harnesshub_root, "config", "user.name", "Test User")
    _git(harnesshub_root, "config", "user.email", "test@example.com")

    task_path = harnesshub_root / ".codex" / "pm" / "tasks" / "product-direction" / "refine-verification-into-explicit-readiness-classes.md"
    task_path.parent.mkdir(parents=True)
    task_path.write_text(
        """---
type: task
title: Refine verification into explicit readiness classes
status: done
---

## Deliverable

Refine verification semantics beyond a boolean runtime-ready signal into explicit readiness classes.

## Scope

- define explicit readiness classes for imported images
- update verification output and tests

## Acceptance Criteria

- verify output can express more than a simple ready/not-ready distinction
""",
        encoding="utf-8",
    )

    state_path = harnesshub_root / ".codex" / "pm" / "issue-state" / "53-refine-verification-into-explicit-readiness-classes.md"
    state_path.parent.mkdir(parents=True)
    state_path.write_text(
        """---
type: issue_state
title: Refine verification into explicit readiness classes
status: done
---

## Summary

Keep the change within current MVP scope and make readiness output more actionable.
""",
        encoding="utf-8",
    )

    changed_file = harnesshub_root / "src" / "core" / "verifier.ts"
    changed_file.parent.mkdir(parents=True)
    changed_file.write_text("export const readiness = true;\n", encoding="utf-8")

    _git(harnesshub_root, "add", ".")
    _git(harnesshub_root, "commit", "-m", "Add explicit verification readiness classes")
    commit_sha = _git(harnesshub_root, "rev-parse", "HEAD")

    runtime_home = tmp_path / "runtime-home"
    runtime_home.mkdir()
    (runtime_home / "openprecedent-runtime-invocations.jsonl").write_text(
        json.dumps(
            {
                "invocation_id": "rtinv_issue53",
                "recorded_at": "2026-03-12T07:43:18.333010Z",
                "query_reason": "before_file_write",
                "task_summary": "HarnessHub issue #53: refine verify output from a binary runtimeReady signal into explicit readiness classes while preserving the current MVP verification scope",
                "current_plan": None,
                "candidate_action": "Add readinessClass to verify results, map structural failure vs manual steps vs runtime ready, and update CLI/e2e output accordingly",
                "known_files": ["src/core/verifier.ts", "test/e2e.test.ts"],
                "matched_case_ids": [],
            }
        )
        + "\n",
        encoding="utf-8",
    )

    output_root = tmp_path / "exports"
    subprocess.run(
        [
            "python3",
            str(repo_root / "scripts" / "export_harnesshub_codex_round.py"),
            "--repo-root",
            str(harnesshub_root),
            "--issue",
            "53",
            "--task-path",
            str(task_path),
            "--state-path",
            str(state_path),
            "--commit",
            commit_sha,
            "--runtime-home",
            str(runtime_home),
            "--output-root",
            str(output_root),
        ],
        check=True,
        cwd=repo_root,
    )

    export_dirs = sorted(output_root.iterdir())
    assert export_dirs
    bundle_dir = export_dirs[-1]
    manifest = json.loads((bundle_dir / "round-manifest.json").read_text(encoding="utf-8"))
    assert manifest["issue"] == 53
    assert manifest["runtime_invocation_count"] == 1

    events_path = bundle_dir / "events.jsonl"
    lines = [json.loads(line) for line in events_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert any(item["event_type"] == "message.user" for item in lines)
    assert any(item["event_type"] == "file.write" for item in lines)

    old_home = os.environ.get("OPENPRECEDENT_HOME")
    isolated_runtime = tmp_path / "op-runtime"
    isolated_runtime.mkdir()
    os.environ["OPENPRECEDENT_HOME"] = str(isolated_runtime)
    try:
        service = OpenPrecedentService.from_path(get_db_path())
        service.create_case(
            CreateCaseInput(
                case_id=manifest["case_id"],
                title=manifest["case_title"],
                agent_id="codex",
            )
        )
        service.import_events_jsonl(events_path)
        decisions = service.extract_decisions(manifest["case_id"])
    finally:
        if old_home is None:
            os.environ.pop("OPENPRECEDENT_HOME", None)
        else:
            os.environ["OPENPRECEDENT_HOME"] = old_home

    assert decisions
    assert any(decision.decision_type.value == "task_frame_defined" for decision in decisions)
