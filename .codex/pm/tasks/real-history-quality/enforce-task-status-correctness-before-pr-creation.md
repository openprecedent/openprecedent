---
type: task
epic: real-history-quality
slug: enforce-task-status-correctness-before-pr-creation
title: Enforce local task status correctness before PR creation and reconcile remote drift
status: done
task_type: implementation
labels: ops,test
issue: 168
state_path: .codex/pm/issue-state/168-enforce-task-status-correctness-before-pr-creation.md
---

## Context

Local `.codex/pm` task statuses have drifted from remote GitHub issue reality in a few cases, including tasks left in `backlog` after the linked issue was already completed and merged.
The repository currently catches some closure mismatches at push or CI time, but that is later than the harness should allow.

## Deliverable

Add a repository-local guardrail so PR creation verifies task status correctness early and provide a standard path for reconciling already-drifted local task metadata against remote issue state.

## Scope

- identify and reconcile existing local task status drift against remote issue state where practical
- enforce that a PR which closes an issue can only be created when the matching task twin is already in the expected status
- strengthen local workflow guidance so status correction happens before push and before CI
- add regression coverage for the chosen enforcement path

## Acceptance Criteria

- existing local task/issue status drift is diagnosed and corrected through a standard repository-local path
- PR creation fails fast when the matching task twin is not in the expected status for the linked issue
- the harness catches this before CI or post-hoc review
- automated coverage exists for the new guardrail

## Validation

- run targeted regression coverage for the PR-creation and closure-sync path
- verify that already-drifted local task metadata can be reconciled through the documented local workflow
- confirm the harness now blocks incorrect task status before PR creation instead of only in CI

## Implementation Notes

- Prefer strengthening the existing `codex_pm pr-create` and closure-sync workflow instead of inventing a parallel PM path.
- Keep the fix focused on local task/issue status correctness rather than broad GitHub project synchronization.
