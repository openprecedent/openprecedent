---
type: task
epic: real-history-quality
slug: enforce-review-proof-before-push
title: Make the pre-push standard review flow enforceable instead of note-only
status: done
labels: feature,test,docs
issue: 139
---

## Context

The repository currently gates pushes on `.codex-review`, but that alone does not prove the standard review checkpoint was run for the current commit set.

## Deliverable

Add a machine-generated review proof and enforce it in the local pre-push and preflight flows.

## Scope

- refresh a review proof file during the checkpoint script
- require the proof to match the current branch and `HEAD`
- require the review note to be updated after the latest checkpoint
- update docs and regression coverage

## Acceptance Criteria

- push-time review enforcement is stronger than note-only gating
- stale or missing review proof blocks push locally
- the workflow is documented in the repository tooling docs

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_codex_review_checkpoint.py tests/test_pre_push_hook.py tests/test_preflight_script.py`
