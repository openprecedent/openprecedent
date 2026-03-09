---
type: epic
slug: local-runtime-validation
title: Local runtime validation
status: backlog
prd: mvp-runtime-validation
---

# Local runtime validation

## Outcome

Operationalize the existing collector path in a real target environment so the MVP loop is validated on scheduled collection rather than only on curated or manually imported sessions.

## Scope

- real target-environment rollout of the collector
- schedule validation and cursor/state validation
- operational notes needed to keep the collector running
- linkage from runtime rollout to later real-session quality work

## Acceptance Criteria

- the epic has a task file linked to the real collector rollout issue
- the task file captures runtime-specific acceptance criteria instead of only generic roadmap text
- future agents can identify this epic as the operational prerequisite for the remaining validation work

## Child Issues

- `#23` Roll out scheduled OpenClaw collector in a real target environment

## Notes

This epic is intentionally narrow. It is about proving the collector runs on a real schedule, not about improving extraction quality or ranking quality directly.
