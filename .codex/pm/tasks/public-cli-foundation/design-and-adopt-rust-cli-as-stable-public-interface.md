---
type: task
epic: public-cli-foundation
slug: design-and-adopt-rust-cli-as-stable-public-interface
title: Design and adopt a Rust CLI as the stable public interface for OpenPrecedent
status: done
task_type: implementation
labels: cli,rust,interface
issue: 172
state_path: .codex/pm/issue-state/172-design-and-adopt-rust-cli-as-stable-public-interface.md
---

## Context

OpenPrecedent needs a durable public executable surface.
This issue defines the contract and system design for a Rust-based `openprecedent` CLI that replaces public Python CLI usage and public shell-wrapper exposure rather than merely mirroring the current MVP command tree.

## Deliverable

Write the system design for the Rust public CLI, create the local PM framing for the new public-interface workstream, and anchor the repository docs to that design baseline.

## Scope

- define the long-term public command tree
- define global flags, output contracts, config precedence, and error semantics
- define the Rust workspace architecture and migration stages
- define how skills and automation move from shell wrappers to direct CLI invocation
- define the cutover policy that removes public Python CLI and public shell-wrapper exposure

## Acceptance Criteria

- the repository contains a decision-complete CLI design doc for Rust public interface evolution
- the design makes Rust CLI the sole intended public interface after cutover
- the design distinguishes public product CLI from repository-internal PM and harness tooling
- local PM artifacts explain how this issue fits into a dedicated public-interface epic
- key product and architecture docs point to the new CLI design baseline

## Validation

- review the design against the current Python CLI surface, public docs, and script-based runtime workflows
- verify the design covers all currently shipped public capabilities that are exposed through `openprecedent` or through public shell wrappers

## Implementation Notes
