---
type: task
epic: public-cli-foundation
slug: design-and-adopt-rust-cli-as-stable-public-interface
title: Design and adopt a Rust CLI as the stable public interface for OpenPrecedent
status: done
task_type: docs
labels: cli,rust,interface
issue: 172
state_path: .codex/pm/issue-state/172-design-and-adopt-rust-cli-as-stable-public-interface.md
---

## Context

OpenPrecedent needs a durable public executable surface.
This issue started as the design baseline for the Rust-based `openprecedent` CLI and later served as the long-lived parent issue for the full public CLI migration train.
The design baseline landed through PR `#173`, the implementation train landed through PR `#202`, and the remaining closeout work is to leave one durable in-repo implementation summary that explains what the Rust CLI actually ships on `main`.

## Deliverable

Document the shipped Rust CLI implementation in one systematic engineering overview and close out issue `#172` now that the design baseline and implementation train have both landed on `main`.

## Scope

- add one comprehensive implementation summary for the shipped Rust CLI
- explain the actual public command surface, workspace layout, compatibility model, workflow cutover, and verification layers
- link the implementation summary from the existing usage and design docs
- close issue `#172` after the in-repo closeout documentation lands

## Acceptance Criteria

- the repository contains a durable engineering document describing the shipped Rust CLI implementation
- the closeout doc distinguishes design intent from implemented behavior
- the implementation doc explains the command surface, crate layout, data compatibility model, and cutover away from the Python CLI and public shell wrappers
- the usage and design docs link to the implementation summary
- the resulting PR can close issue `#172`

## Validation

- review the implementation summary against the Rust workspace, current public docs, and shipped command surface on `main`
- verify the closeout doc matches the actual cutover state for Python CLI removal and public script deprecation
- run `./scripts/run-agent-preflight.sh` before opening the closing PR

## Implementation Notes

- PR `#173` merged the design baseline into `main`.
- PR `#202` merged the dedicated Rust CLI integration branch back into `main`.
- Child issues `#174` through `#187` implemented the migration in independently reviewable slices before the final integration merge.
- This closeout PR leaves one stable implementation summary in the repository and closes issue `#172`.
