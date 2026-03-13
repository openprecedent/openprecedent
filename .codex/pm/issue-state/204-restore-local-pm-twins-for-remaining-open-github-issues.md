---
type: issue_state
issue: 204
task: .codex/pm/tasks/real-history-quality/restore-local-pm-twins-for-remaining-open-github-issues.md
title: Restore local PM twins for remaining open GitHub issues
status: done
---

## Summary

Restore tracked local PM coverage for the remaining open GitHub issues so session-start and local issue/task reasoning match the actual upstream issue set.

## Validated Facts

- `reconcile-task-statuses` only checks tracked task twins; it cannot report on open issues whose local twin is missing.
- the current open GitHub issue set is `#100`, `#131`, `#163`, and `#204`
- issue `#100` already has a tracked local task twin but did not have a tracked issue-state file on `main`
- issue `#131` lacked both a tracked task twin and a tracked issue-state file on `main`
- issue `#163` had a local task twin in the working tree but it was not tracked on `main`, and it also lacked a tracked issue-state file
- issue `#204` itself needs a tracked task twin and issue-state file because the work is now active on a dedicated branch

## Open Questions

- whether any additional open issues later need to be intentionally excluded from local PM tracking rather than restored

## Next Steps

- open and merge the issue-scoped PR for `#204`
- reuse the restored local PM coverage in future session-start and reconciliation workflows

## Artifacts

- `.codex/pm/tasks/`
- `.codex/pm/issue-state/`
- `src/openprecedent/codex_pm.py`
