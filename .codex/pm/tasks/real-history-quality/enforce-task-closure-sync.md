---
type: task
epic: real-history-quality
slug: enforce-task-closure-sync
title: Enforce task closure sync in issue-linked PRs
status: done
labels: feature,test,ops
issue: 90
---

## Context

The repository expects one issue-scoped task file per implementation branch, but that rule is not enforced automatically.
When a PR closes an issue without marking the matching local task file as `done`, the local Codex PM workspace drifts and later requires cleanup work.

## Deliverable

Add an in-repo validation command and PR gate that require issue-linked PRs to update the matching local task file to `status: done` before merge.

## Scope

- add Codex PM validation logic for `Closes #<issue>` style PR bodies
- fail PR checks when the matching task file is absent from the diff or not marked `done`
- cover the validation behavior with automated tests
- keep the scope focused on task-closure consistency rather than broader PM automation

## Acceptance Criteria

- a PR that closes an issue fails if the matching `.codex/pm/tasks/...` file is not changed
- a PR that closes an issue fails if the matching task file is changed but not marked `done`
- a PR that closes an issue passes when the matching task file is present and marked `done`
- the rule is enforced through repository CI rather than human memory alone

## Validation

- run Codex PM unit tests covering passing and failing closure-sync cases
- verify the PR review gate workflow executes the new validation command

## Implementation Notes
