---
type: task
epic: public-cli-foundation
slug: migrate-decision-commands-to-rust-cli
title: Migrate decision commands to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 179
---

## Context

Child issue `#179` under `#172` migrates the public derived-decision workflow into Rust. This slice should implement Rust-native decision extraction and listing while preserving the separation between raw events and derived decision records.

## Deliverable

Implement `openprecedent decision extract` and `openprecedent decision list` in Rust on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- replace the placeholder Rust `decision` handlers with real extraction and listing implementations
- preserve the current decision heuristics for task framing, constraints, success criteria, clarification, option rejection, and authority confirmation
- persist extracted decisions through the Rust SQLite store

## Acceptance Criteria

- `openprecedent decision extract <case-id>` derives and stores decisions through the Rust path
- `openprecedent decision list <case-id>` returns stable JSON and readable text output from the Rust path
- extracted decisions remain compatible with the current persistence model and downstream replay/precedent assumptions
- Rust tests cover representative extraction scenarios and key failure cases

## Validation

- run `cargo test`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh` before opening the PR

## Implementation Notes

- Keep the extraction logic Rust-native; do not shell out to the Python CLI or Python service layer.
- Favor a direct behavior port from the current Python heuristics before attempting any semantic redesign.
- Completed on `codex/issue-179-rust-decision-commands` with Rust-native decision extraction/listing, contract tests, and persisted decision records through the Rust SQLite store.
