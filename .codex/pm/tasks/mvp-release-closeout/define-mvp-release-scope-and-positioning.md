---
type: task
epic: mvp-release-closeout
slug: define-mvp-release-scope-and-positioning
title: Define the MVP release scope and positioning
status: done
task_type: docs
labels: documentation
issue: 245
state_path: .codex/pm/issue-state/245-define-mvp-release-scope-and-positioning.md
---

## Context

The repository states that MVP v1 is complete, but the release still needs a concise public-facing statement of what is included, what is intentionally excluded, and what kind of release this is.

## Deliverable

Release-scope and release-positioning documentation for the MVP publication.

## Scope

- define the MVP release as local-first, research-oriented, and developer-facing
- clearly separate release scope from post-MVP research backlog
- clarify supported usage boundaries and what this release does not promise
- avoid changing product behavior

## Acceptance Criteria

- release-facing documentation clearly states what the MVP release is
- release-facing documentation clearly states what the MVP release is not
- post-release research issues are not described as MVP blockers

## Validation

- review the release-facing docs for consistent positioning
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

This issue should set the narrative baseline that later release notes and closeout docs can reuse.
