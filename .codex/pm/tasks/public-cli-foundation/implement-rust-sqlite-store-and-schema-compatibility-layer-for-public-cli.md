---
type: task
epic: public-cli-foundation
slug: implement-rust-sqlite-store-and-schema-compatibility-layer-for-public-cli
title: Implement the Rust SQLite store and schema compatibility layer for the public CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 176
state_path: .codex/pm/issue-state/176-implement-rust-sqlite-store-and-schema-compatibility-layer-for-public-cli.md
---

## Context

The Rust CLI already has a stable config and doctor surface from `#175`, but later command families still need a Rust-native persistence layer.
This slice ports SQLite schema ownership, initialization, migration, and row-mapping into Rust so later command issues can use one shared store crate instead of reaching back into Python.

## Deliverable

Implement the Rust SQLite store crate with schema bootstrap, legacy migration handling, and reusable CRUD-style methods for the core case, event, decision, and artifact records.

## Scope

- add Rust domain structs for case, event, decision, and artifact records to the shared contracts crate
- implement SQLite schema initialization and migration in `openprecedent-store-sqlite`
- implement reusable store methods for the core persisted objects used by later CLI slices
- add Rust tests for roundtripping current schema data and upgrading a legacy decisions table missing newer columns

## Acceptance Criteria

- the Rust implementation can open and validate the existing SQLite runtime schema shape
- schema and migration ownership for the public CLI no longer depend on Python at runtime
- later CLI command slices can reuse the Rust store layer instead of re-implementing DB access
- store tests cover both current-schema roundtrips and legacy-column migration behavior

## Validation

- run `. \"$HOME/.cargo/env\" && cargo test`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`

## Implementation Notes

- The store crate now owns the SQLite DDL for cases, events, decisions, and artifacts.
- The Rust contracts crate now includes the core persisted object types, which later command slices can use directly.
