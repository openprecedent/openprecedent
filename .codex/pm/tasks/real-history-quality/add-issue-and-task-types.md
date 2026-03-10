---
type: task
epic: real-history-quality
slug: add-issue-and-task-types
title: Add issue and task types to the Codex PM workflow
status: done
labels: feature,test,ops
issue: 103
---

## Context

The current Codex PM workflow tracks status and issue linkage, but it does not explicitly represent what kind of issue a task actually is.
That gap caused confusion during harness work around whether a PR should close an issue, whether a task should remain open long-term, and how umbrella research issues should be handled differently from normal delivery work.

## Deliverable

A first-pass issue/task type model in Codex PM that can distinguish normal delivery work from long-lived umbrella issues and enforce the most important closure behavior difference.

## Scope

- add explicit task type metadata to Codex PM task creation and task serialization
- support task types for at least `implementation`, `docs`, `research`, and `umbrella`
- make PR-body rendering and PR closure validation respect `umbrella` semantics
- update the existing `#100` task twin to use the new `umbrella` type

## Acceptance Criteria

- Codex PM task documents can represent task type directly in frontmatter and JSON output
- issue body rendering exposes the task type in an inspectable way
- PR body generation does not emit `Closes #...` for `umbrella` tasks
- PR closure sync fails if a PR attempts to close an `umbrella` task issue

## Validation

- `.venv/bin/pytest tests/test_codex_pm.py`

## Implementation Notes

- Added `--task-type` to `task-new` with `implementation`, `docs`, `research`, and `umbrella`.
- Updated PR closure validation so `task_type=umbrella` must remain open.
- Marked the existing `#100` local task twin as `task_type: umbrella`.
