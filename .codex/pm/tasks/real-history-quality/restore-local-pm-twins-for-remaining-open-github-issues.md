---
type: task
epic: real-history-quality
slug: restore-local-pm-twins-for-remaining-open-github-issues
title: Restore local PM twins for remaining open GitHub issues
status: done
task_type: implementation
labels: ops,docs
issue: 204
state_path: .codex/pm/issue-state/204-restore-local-pm-twins-for-remaining-open-github-issues.md
---

## Context

`reconcile-task-statuses` currently reports no local-vs-remote status drift for tracked task twins, but the repository still has a narrower PM consistency gap.
Some still-open GitHub issues either lack tracked local task twins on `main`, lack tracked issue-state files, or both.
That weakens session-start restoration and makes the local PM view less trustworthy than the actual GitHub issue list.

## Deliverable

Restore the missing local task twin and issue-state coverage for the remaining open GitHub issues and confirm the resulting local PM state matches remote issue status.

## Scope

- create a tracked local task twin for issue `#204`
- restore the missing tracked local task twin for issue `#131`
- track the existing issue `#163` task twin on `main`
- add issue-state files for open issues `#100`, `#131`, `#163`, and `#204`
- keep the long-lived umbrella semantics for `#100` intact
- update epic metadata where needed so the restored tasks are visible in the local PM structure

## Acceptance Criteria

- every intended open GitHub issue tracked by the local PM workflow has a tracked task twin on `main`
- the remaining open issues that should participate in session restore have tracked issue-state files
- local task status values for those issues match their intended local workflow stage
- `reconcile-task-statuses --json` still reports no remote-vs-local status drift after the restoration

## Validation

- verify tracked local PM coverage for open issues `#100`, `#131`, `#163`, and `#204`
- run `PYTHONPATH=src python3 -m openprecedent.codex_pm reconcile-task-statuses --json`
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

- This issue is about restoring missing local PM assets, not about changing the underlying product roadmap.
- If an issue is intentionally long-lived, preserve that semantics in local status and issue-state rather than forcing artificial closure.
