---
type: task
epic: mvp-release-closeout
slug: add-mvp-quickstart-and-new-project-installation-guide
title: Add MVP quickstart and new-project installation guide
status: done
task_type: docs
labels: documentation
issue: 248
state_path: .codex/pm/issue-state/248-add-mvp-quickstart-and-new-project-installation-guide.md
---

## Context

The current usage guide is useful, but publishing the MVP for new-project use needs a shorter and more direct quickstart path that a new user can follow without reading the whole repository.

## Deliverable

A concise quickstart and installation guide for using the MVP in a new project.

## Scope

- document the recommended installation or build path for the Rust CLI
- provide a minimal end-to-end example that proves the MVP loop works
- optimize the docs for first-use clarity rather than exhaustive engineering detail
- keep the guide aligned with the actual supported MVP surface

## Acceptance Criteria

- a new user can find a short install/build path
- a new user can run a minimal example without repository archaeology
- the quickstart points to deeper usage docs only after the shortest successful path

## Validation

- follow the documented quickstart from a clean local path
- confirm the commands and file references are correct
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

If binary artifacts are not yet available, the quickstart should still make the source-build path short and explicit.
