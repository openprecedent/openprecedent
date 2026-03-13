---
type: task
epic: codex-runtime-research
slug: validate-codex-real-project-decision-lineage-reuse
title: Validate Codex real-project decision-lineage reuse across HarnessHub development
status: in_progress
task_type: research
labels: research
issue: 131
state_path: .codex/pm/issue-state/131-validate-codex-real-project-decision-lineage-reuse.md
---

## Context

OpenPrecedent added Codex support so the project could test real decision-lineage reuse on the agent workflow that now produces the densest development history.
HarnessHub is the active external-project validation target for that question.
The issue remains open because the research thread still needs one tracked local twin on `main` that captures the current evidence and remaining closeout path.

## Deliverable

Track the current state of the HarnessHub real-project validation in the local PM workspace so later sessions can recover the active research context without rediscovering the study setup.

## Scope

- preserve the open GitHub issue in the local PM tree
- record that the study targets HarnessHub as the active real-project validation site
- capture the current evidence level and remaining closeout path in local issue-state
- keep the task open while the real-project validation issue remains open upstream

## Acceptance Criteria

- issue `#131` has a tracked local task twin on `main`
- the local task and issue-state preserve the current HarnessHub validation context
- future sessions can recover the study status without relying on prior chat history

## Validation

- verify that issue `#131` is represented in `.codex/pm/tasks` and `.codex/pm/issue-state`
- confirm the local task status remains aligned with the still-open remote issue
- keep the documented study context consistent with the existing HarnessHub validation artifacts

## Implementation Notes

- Earlier study records may refer to the same target project by the earlier ClawPack naming.
- This task is research tracking, not a signal that the validation conclusion is still absent.
