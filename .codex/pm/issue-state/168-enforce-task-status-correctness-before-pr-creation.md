---
type: issue_state
issue: 168
task: .codex/pm/tasks/real-history-quality/enforce-task-status-correctness-before-pr-creation.md
title: Enforce local task status correctness before PR creation and reconcile remote drift
status: in_progress
---

## Summary

Strengthen the local PM harness so task status drift can be reconciled explicitly and PR creation fails before CI when a closing issue's task twin is not already marked `done`.

## Validated Facts

- `openprecedent.codex_pm pr-create` now fails fast if the matching non-umbrella task twin is not marked `done` before PR creation.
- `openprecedent.codex_pm reconcile-task-statuses` can now diagnose remote-vs-local task drift and safely auto-mark local tasks `done` when the linked remote issue is already closed.
- The current `upstream/main` task twins for issues `#161`, `#164`, and `#166` already reconcile cleanly against GitHub issue state.
- Tooling and agent guidance now tell contributors to fix task status before PR creation instead of relying on push-time or CI-time closure sync failures.

## Open Questions

- Whether later harness hardening should also refuse PR body generation when the linked task twin is not yet `done`, or keep the fail-fast rule scoped to PR creation.

## Next Steps

- Open and merge the issue-scoped PR for `#168`.
- Reuse `reconcile-task-statuses` when future local-vs-remote PM drift is suspected.

## Artifacts

- `src/openprecedent/codex_pm.py`
- `tests/test_codex_pm.py`
- `docs/engineering/tooling-setup.md`
- `AGENTS.md`
