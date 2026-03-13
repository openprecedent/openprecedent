---
type: issue_state
issue: 166
task: .codex/pm/tasks/real-history-quality/add-standard-codex-session-start-workflow.md
title: Add a standard Codex session-start workflow for issue continuity and default direct-fix behavior
status: done
---

## Summary

Add a standard Codex session-start entrypoint so fresh sessions restore branch-local issue context and restate the repository's default direct-fix execution policy.

## Validated Facts

- `openprecedent.codex_pm` now exposes a `session-start` command that summarizes branch, issue, task, issue-state, PR context, and default execution policies.
- `scripts/run-codex-session-start.sh` provides the repository-local startup entrypoint for agents and humans.
- The startup output explicitly tells Codex to directly diagnose, implement, verify, and close the loop for concrete user-reported problems unless blocked or high-risk.
- Tooling and agent guidance now point new sessions at the startup command instead of relying on prior chat memory alone.

## Open Questions

- Whether the session-start command should later become an enforced pre-work checkpoint rather than a documented standard path.

## Next Steps

- Open and merge the issue-scoped PR for `#166`.
- Reuse this startup surface in future harness-gap closures where session continuity drift appears again.

## Artifacts

- `scripts/run-codex-session-start.sh`
- `src/openprecedent/codex_pm.py`
- `docs/engineering/tooling-setup.md`
- `AGENTS.md`
