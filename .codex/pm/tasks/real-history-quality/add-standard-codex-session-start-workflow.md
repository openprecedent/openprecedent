---
type: task
epic: real-history-quality
slug: add-standard-codex-session-start-workflow
title: Add a standard Codex session-start workflow for issue continuity and default direct-fix behavior
status: done
task_type: implementation
labels: ops,test
issue: 166
state_path: .codex/pm/issue-state/166-add-standard-codex-session-start-workflow.md
---

## Context

Codex sessions can restart without reliably recovering repository-specific execution behavior, especially around issue continuity, closure state, and the default expectation to directly fix concrete problems through implementation and verification.

## Deliverable

Add a standard session-start harness entrypoint that surfaces the active issue/task/PR context and the repository's default direct-fix behavior so later Codex sessions start from the same durable workflow state.

## Scope

- add one repository-local startup entrypoint for Codex sessions
- surface branch, issue, task status, issue-state availability, and PR context
- restate the default execution rule for concrete user-reported problems: diagnose, implement, verify, and close the loop unless blocked or high-risk
- document the startup workflow in contributor-facing harness docs
- add regression coverage for the startup surface

## Acceptance Criteria

- a new Codex session has one standard local command to restore active issue context
- the startup output includes enough issue/task/state information to reduce branch-local workflow drift
- the startup output explicitly states the repository's default direct-fix behavior for concrete problems
- automated coverage exists for the startup surface

## Validation

- run targeted pytest coverage for `codex_pm` and the docs guardrails
- verify the startup output includes the direct-fix policy and state warnings where appropriate

## Implementation Notes

- Prefer building on the existing `codex_pm`, task twin, and issue-state mechanisms instead of inventing a second state system.
