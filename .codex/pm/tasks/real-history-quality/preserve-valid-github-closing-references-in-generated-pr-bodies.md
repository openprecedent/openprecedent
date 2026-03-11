---
type: task
epic: real-history-quality
slug: preserve-valid-github-closing-references-in-generated-pr-bodies
title: Preserve valid GitHub closing references in generated PR bodies
status: done
labels: feature,test
issue: 146
---

## Context

The repository PR-creation harness generated a malformed PR body in PR #145, so GitHub did not auto-close issue #130 after merge.

## Deliverable

Make the PR-creation flow preserve clean multiline PR bodies and valid standalone closing references.

## Scope

- pass generated PR bodies to `gh pr create` through a temporary body file instead of an inline `--body` argument
- filter placeholder-only validation bullets out of generated PR bodies
- add regression coverage for clean closing references and preserved body formatting

## Acceptance Criteria

- generated PR bodies preserve normal multiline formatting
- a trailing closing reference such as `Closes #123` is emitted as a clean standalone line
- regression coverage would have caught the malformed PR body seen in PR #145

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_codex_pm.py -k 'pr_create or pr_body'`
