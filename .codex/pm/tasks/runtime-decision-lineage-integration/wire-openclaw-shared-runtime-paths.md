---
type: task
epic: runtime-decision-lineage-integration
slug: wire-openclaw-shared-runtime-paths
title: Wire the OpenClaw decision-lineage skill to a stable shared OpenPrecedent DB and invocation log
status: done
labels: feature,docs,test
issue: 85
---

## Context

Live validation in issue #80 proved that OpenClaw can discover and invoke the OpenPrecedent decision-lineage skill, but the runtime command defaulted to workspace-local persistence.
That split prior decision lineage across accidental current-working-directory databases and made invocation logs land in ad hoc workspace paths.

## Deliverable

Define and implement a stable runtime configuration path that lets OpenClaw point the decision-lineage skill at an intended shared OpenPrecedent database and invocation log.

## Scope

- add a supported shared runtime home configuration for live OpenClaw use
- keep explicit DB and invocation-log overrides working
- document the supported wiring for operators and skill installers
- add tests that prove runtime brief calls honor the configured shared paths outside the current working directory

## Acceptance Criteria

- a runtime decision-lineage brief can read prior lineage from a configured shared database instead of a workspace-local default
- invocation logging can write to the configured shared path during runtime use
- human-facing and skill-facing docs explain the supported configuration clearly
- tests lock the chosen path resolution behavior so future changes do not regress live runtime integration

## Validation

- run the runtime CLI tests that cover shared home and explicit override path resolution
- verify the runtime brief and invocation list commands read and write the configured shared paths

## Implementation Notes

Issue #85 is the direct follow-up to the live isolated-profile findings recorded in `docs/engineering/openclaw-real-runtime-decision-lineage-validation.md`.
