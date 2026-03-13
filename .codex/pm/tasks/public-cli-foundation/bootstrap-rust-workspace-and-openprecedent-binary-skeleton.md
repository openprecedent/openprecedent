---
type: task
epic: public-cli-foundation
slug: bootstrap-rust-workspace-and-openprecedent-binary-skeleton
title: Bootstrap the Rust workspace and openprecedent binary skeleton
status: done
task_type: implementation
labels: cli,rust,interface
issue: 174
state_path: .codex/pm/issue-state/174-bootstrap-rust-workspace-and-openprecedent-binary-skeleton.md
---

## Context

The Rust public CLI design is already merged and issue `#172` now acts as the parent integration issue for the migration train.
The first implementation slice needs to create the Rust workspace and the top-level `openprecedent` binary skeleton so later command families can land without revisiting crate layout or binary identity.

## Deliverable

Create the Rust workspace, add the binary crate and supporting library crates named in the design baseline, and add regression coverage that keeps the workspace topology and top-level command roots from drifting.

## Scope

- add a root `Cargo.toml` workspace for the Rust public CLI workstream
- create the `openprecedent` binary crate and the initial contract and core crate skeletons
- create placeholder crates for the planned store and capture modules so later issues can land without reworking the workspace
- define the top-level command roots in the Rust binary even if command execution remains placeholder-only in this slice
- add lightweight regression tests that verify the workspace layout and command-root skeleton

## Acceptance Criteria

- the repository contains a Rust workspace rooted at `Cargo.toml`
- the Rust workspace includes the crates named in the public CLI design baseline
- the `openprecedent` binary name is established in Rust
- the Rust CLI skeleton exposes the long-term top-level command roots needed by later child issues
- regression tests protect the workspace topology and command-root skeleton

## Validation

- run the repository-local Python test path for the Rust workspace regression tests
- run `cargo test` for the new Rust workspace
- confirm the workspace files are consistent with `docs/engineering/rust-public-cli-design.md`

## Implementation Notes

- This slice intentionally does not migrate live command behavior away from Python yet.
- The Rust skeleton should be stable enough for later child branches to build on without reworking crate or binary identity.
- The initial workspace includes the command roots from the design doc, but subcommands still return explicit not-implemented errors except for `version`.
