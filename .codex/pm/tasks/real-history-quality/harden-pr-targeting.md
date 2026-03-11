---
type: task
epic: real-history-quality
slug: harden-pr-targeting
title: Harden the agent harness against fork-targeted PR creation drift
status: done
labels: feature,test,docs
issue: 136
---

## Context

Repeated PR creation attempts can still drift toward the fork or inferred default repository instead of the intended upstream target.

## Deliverable

Add a repository-local PR creation path that pins the upstream repository and explicit fork head owner.

## Scope

- add a local PR creation command to `openprecedent.codex_pm`
- fail fast when fork owner or upstream targeting is ambiguous
- update workflow documentation and the local skill command map

## Acceptance Criteria

- default local PR creation targets `openprecedent/openprecedent`
- the local command does not rely on `gh` repository inference
- ambiguous remote targeting fails locally with a clear error

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_codex_pm.py -k 'pr_create or pr_body'`
