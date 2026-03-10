---
type: task
epic: real-history-quality
slug: issue-scoped-development-state
title: Capture issue-scoped development state for long-running agent work
status: done
task_type: implementation
labels: feature,ops,docs
issue: 106
state_path: .codex/pm/issue-state/106-issue-scoped-development-state.md
---

## Context

Longer issue threads repeatedly lost high-value working memory: what had already been validated, which runtime session proved what, and what remained unresolved.
The harness needed a lightweight local mechanism that fits existing task twins instead of a separate heavyweight PM system.

## Deliverable

Add an issue-scoped state document workflow to `codex_pm`, connect it to local preflight, and document how authors should use it for in-progress issue branches.

## Scope

- add `issue-state-init`, `issue-state-show`, and `issue-state-check` commands to `openprecedent.codex_pm`
- store issue state under `.codex/pm/issue-state/` and link it from the matching task metadata
- have local preflight surface missing state for in-progress issue branches and support an optional enforcement mode
- document the workflow in engineering tooling docs

## Acceptance Criteria

- an in-progress issue task can initialize a stable local state document
- the task metadata records the linked state document path
- local preflight surfaces missing state for in-progress issue branches
- the workflow stays lightweight enough for routine use

## Validation

- `.venv/bin/pytest tests/test_codex_pm.py`

## Implementation Notes

The default preflight behavior only warns on missing issue state so adoption stays lightweight.
Teams that want stricter continuity can opt into enforcement with `OPENPRECEDENT_PREFLIGHT_ENFORCE_ISSUE_STATE=1`.
