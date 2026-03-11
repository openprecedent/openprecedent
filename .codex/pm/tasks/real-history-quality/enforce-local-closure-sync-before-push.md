---
type: task
epic: real-history-quality
slug: enforce-local-closure-sync-before-push
title: Enforce local closure-sync scanning before push in the agent harness
status: done
labels: feature,test,docs
issue: 133
---

## Context

The repository already had local closure-sync verification in the optional preflight path and in CI, but not in the default pre-push hook.
That allowed contributors to push branches that would predictably fail `pr-review-gate` later.

## Deliverable

Extend the local agent harness so closure-sync scanning runs in the default pre-push path when local PR context is available.

## Scope

- add a local closure-sync check to `.githooks/pre-push`
- skip gracefully when the base ref, `gh`, or PR body is unavailable
- document the new local guardrail behavior
- add tests covering failing and passing local hook scenarios

## Acceptance Criteria

- a contributor pushing a branch with a `Closes #<issue>` mismatch and unfinished local task file is blocked locally before CI
- the hook remains usable when no local PR context is available
- tests cover the new local hook behavior
- repository docs explain the added guardrail

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_pre_push_hook.py tests/test_preflight_script.py tests/test_branch_freshness_script.py tests/test_codex_pm.py -k 'pre_push or preflight or branch_freshness or closure_sync'`
