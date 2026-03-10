---
type: task
epic: real-history-quality
slug: unified-agent-preflight
title: Add a unified agent preflight script for local harness checks
status: done
labels: feature,ops,test
issue: 108
---

## Context

The repository now has multiple local guardrails, but they are still spread across separate habits and commands.
During MVP work, agents repeatedly lost time to failures that could have been caught in one earlier local pass: missing review notes, merged-branch reuse, markdownlint issues, skipped tests, and task/PR sync drift.

## Deliverable

A single local preflight entrypoint for the current harness that front-loads the most common local readiness checks before push.

## Scope

- add a repository-local preflight script for normal agent-driven development
- include review-note checks, merged-branch reuse checks, pytest, markdownlint when available, and local PR closure sync validation
- support an optional E2E pass for runtime-affecting work without forcing it for every change
- document the script in the existing tooling docs

## Acceptance Criteria

- one command gives an agent a meaningful local readiness signal before push
- the script catches common non-product failures earlier than CI where possible
- runtime-affecting work can opt into the standard E2E path through the same entrypoint
- the script is documented in repository-local tooling guidance

## Validation

- `.venv/bin/pytest tests/test_preflight_script.py`
- `.venv/bin/pytest tests/test_codex_pm.py tests/test_e2e_script.py tests/test_preflight_script.py`

## Implementation Notes

- The first version intentionally keeps markdownlint optional because local environments may not have `markdownlint-cli2` installed.
- The script treats E2E as opt-in through `OPENPRECEDENT_PREFLIGHT_RUN_E2E=1` so docs-only and small PM changes are not penalized.
