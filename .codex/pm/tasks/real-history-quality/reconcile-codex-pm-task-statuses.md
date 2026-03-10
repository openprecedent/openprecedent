---
type: task
epic: real-history-quality
slug: reconcile-codex-pm-task-statuses
title: Reconcile local Codex PM task statuses with merged GitHub issues
status: done
labels: docs,ops
issue: 89
---

## Context

Several local task files under `.codex/pm/tasks` still showed `in_progress`, `backlog`, or legacy `completed` even though their linked GitHub issues were already closed and merged.
That made the local Codex PM workspace inconsistent with the actual repository state.

## Deliverable

Update the local Codex PM task files so status values match the linked GitHub issue state for already-merged work.

## Scope

- identify task files whose linked issue is already closed
- set those task files to `done` where the work is already merged
- leave future follow-up work to new issues instead of overloading already-closed tasks

## Acceptance Criteria

- local task files linked to merged issues no longer remain in `in_progress`, `backlog`, or legacy `completed`
- the local PM workspace better reflects the current repository state

## Validation

- verify that no closed GitHub issue still maps to a non-`done` local task file

## Implementation Notes

This task is intentionally limited to local PM hygiene and does not change product behavior.
