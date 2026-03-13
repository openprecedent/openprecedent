---
type: task
epic: public-cli-foundation
slug: design-and-adopt-rust-cli-as-stable-public-interface
title: Design and adopt a Rust CLI as the stable public interface for OpenPrecedent
status: done
task_type: umbrella
labels: cli,rust,interface
issue: 172
state_path: .codex/pm/issue-state/172-design-and-adopt-rust-cli-as-stable-public-interface.md
---

## Context

OpenPrecedent needs a durable public executable surface.
This issue started as the design baseline for the Rust-based `openprecedent` CLI and is now the long-lived parent issue for the full public CLI migration train.
The design baseline landed through PR `#173`, but the issue remains open as the integration parent for all later Rust CLI child issues that merge into the dedicated branch `codex/issue-172-rust-public-cli` before the final cutover back to `main`.

## Deliverable

Keep the Rust public CLI design baseline authoritative, define the branch integration policy for the migration train, and carry the full Rust CLI child-issue chain through integration until the completed train is ready for one final merge from `codex/issue-172-rust-public-cli` back to `main`.

## Scope

- keep the long-term public command tree and interface rules fixed as the parent contract
- require child implementation PRs under this workstream to merge into `codex/issue-172-rust-public-cli` instead of `main`
- maintain the child-issue breakdown for the Rust workspace, store layer, domain commands, capture surfaces, lineage surfaces, skill migration, and final cutover
- hold the integration branch open until the Rust CLI chain is fully integrated and ready for one final merge back to `main`

## Acceptance Criteria

- the repository contains a decision-complete CLI design doc for Rust public interface evolution
- the design makes Rust CLI the sole intended public interface after cutover
- local PM and GitHub issue artifacts make `#172` the explicit parent of the Rust CLI implementation chain
- the parent issue states that child issue PRs merge into `codex/issue-172-rust-public-cli` before the final cutover PR back to `main`
- the child issue breakdown is fine-grained enough for independent review and implementation slices

## Validation

- review the design against the current Python CLI surface, public docs, and script-based runtime workflows
- verify the child issue chain covers all currently shipped public capabilities that are exposed through `openprecedent` or through public shell wrappers
- confirm the parent issue and integration-branch policy are explicit in both local PM state and the GitHub issue body
- run the integrated Rust CLI branch through `cargo test`, targeted Python regression tests, and `./scripts/run-agent-preflight.sh` before opening the final merge-back PR

## Implementation Notes

- PR `#173` merged the design baseline into `main`.
- Issue `#172` was reopened as the parent umbrella for the dedicated Rust CLI integration branch.
- Child issues `#174` through `#187` implemented the migration in independently reviewable slices and merged into `codex/issue-172-rust-public-cli`.
- The integration branch now contains the full Rust workspace, Rust command families, skill migration, and public cutover away from the Python CLI and public shell-script entrypoints.
