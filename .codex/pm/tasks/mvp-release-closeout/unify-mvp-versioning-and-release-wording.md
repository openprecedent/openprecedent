---
type: task
epic: mvp-release-closeout
slug: unify-mvp-versioning-and-release-wording
title: Unify MVP versioning and release wording
status: done
task_type: docs
labels: documentation
issue: 249
state_path: .codex/pm/issue-state/249-unify-mvp-versioning-and-release-wording.md
---

## Context

The current repository already uses `0.1.0`, but release-facing wording still mixes MVP status, bootstrap-era terms, and implementation-history language. The published MVP needs cleaner, more consistent version and release wording.

## Deliverable

Consistent release wording and version presentation across the MVP-facing docs and surfaces.

## Scope

- scan release-facing docs and metadata for inconsistent MVP and release wording
- normalize version and release language around the chosen MVP release baseline
- remove wording that creates unnecessary ambiguity for a first public MVP release
- avoid changing product semantics beyond release wording cleanup

## Acceptance Criteria

- release-facing docs and metadata describe the MVP release consistently
- ambiguous bootstrap-era or migration-era wording no longer dominates the release surface
- version references are aligned across the main release-facing materials

## Validation

- review the key release-facing docs and metadata after the wording pass
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

This issue is about release clarity, not introducing a new product roadmap or renaming the current version line.
