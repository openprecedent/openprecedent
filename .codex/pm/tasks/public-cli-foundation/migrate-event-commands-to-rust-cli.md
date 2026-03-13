---
type: task
epic: public-cli-foundation
slug: migrate-event-commands-to-rust-cli
title: Migrate event commands to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 178
---

## Context

Child issue `#178` under `#172` migrates the public `openprecedent event` command family from Python into the Rust CLI. This slice should land only the event append and structured JSONL import surfaces, preserving the raw-event timeline contract and the existing SQLite persistence layout.

## Deliverable

Implement `openprecedent event append` and `openprecedent event import-jsonl` in Rust on a dedicated child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- replace the placeholder Rust `event` handlers with real append/import implementations
- preserve event ordering, sequence assignment, timestamps, payload storage, and case status transitions
- validate imported and appended events against the current CLI contract expectations

## Acceptance Criteria

- `openprecedent event append` writes a new event through the Rust store and returns the created event
- `openprecedent event import-jsonl` ingests JSONL event records through the Rust CLI without depending on the Python CLI
- stored events remain compatible with the current persistence model and replay ordering assumptions
- Rust tests cover append and import success paths plus key error cases

## Validation

- run `cargo test -p openprecedent-cli`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh` before opening the PR

## Implementation Notes

- Keep the public interface contract-first: stable JSON output, domain-shaped errors, and no shell wrapper dependencies.
- Reuse the Rust SQLite store instead of adding Python interop or shell delegation.
- Completed on `codex/issue-178-rust-event-commands` with Rust `event append` / `event import-jsonl`, contract tests, and an event-type serialization compatibility fix in the shared Rust contracts crate.
