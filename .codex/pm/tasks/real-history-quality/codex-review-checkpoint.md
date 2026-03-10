---
type: task
epic: real-history-quality
slug: codex-review-checkpoint
title: Integrate Codex /review into a local harness checkpoint
status: done
task_type: implementation
labels: feature,ops,docs
issue: 116
---

## Context

Codex now has a native `/review` command, but the repository lacked a consistent local place to trigger it before pushing.
The harness already enforced the presence of `.codex-review`, but it did not guide authors toward a standard checkpoint or provide a starter note.

## Deliverable

Add a repository-local review checkpoint script, wire the hook and docs to point at it, and keep the outcome compatible with the existing `.codex-review` guardrail.

## Scope

- add a `scripts/run-codex-review-checkpoint.sh` entrypoint
- update the local pre-push hook to direct authors to the checkpoint
- document the checkpoint in tooling docs and scripts inventory
- add tests for template creation and existing-note preservation

## Acceptance Criteria

- a local script exists that creates a `.codex-review` template when missing
- the script explicitly tells the author to run native Codex `/review`
- the pre-push hook error points authors to the checkpoint script
- repository docs describe the checkpoint as the preferred `/review` trigger location

## Validation

- `.venv/bin/pytest tests/test_codex_review_checkpoint.py`

## Implementation Notes

The harness cannot invoke the native Codex slash command directly from a shell hook.
This first version therefore creates a workflow-fit checkpoint that prepares the review note and tells the author exactly when to run `/review`.
