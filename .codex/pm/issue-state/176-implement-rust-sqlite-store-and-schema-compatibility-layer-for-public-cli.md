---
type: issue_state
issue: 176
task: .codex/pm/tasks/public-cli-foundation/implement-rust-sqlite-store-and-schema-compatibility-layer-for-public-cli.md
title: Implement the Rust SQLite store and schema compatibility layer for the public CLI
status: in_progress
---

## Summary

Port SQLite schema ownership and the reusable persistence layer into Rust so later command migrations can read and write the runtime database without depending on Python.

## Validated Facts

- the Rust contracts crate now includes case, event, decision, and artifact domain types
- the Rust SQLite store crate now owns schema initialization for cases, events, decisions, and artifacts
- the Rust SQLite store crate also applies the decisions-table compatibility migration for missing `confidence` and `explanation_json` columns
- the Rust store exposes reusable methods for creating and listing cases, appending and listing events, replacing and listing decisions, finding a case by OpenClaw session id, and upserting artifacts
- `cargo test` passes across the full Rust workspace, including store roundtrip and legacy migration tests

## Open Questions

- whether the next command-family slices should move the shared row-mapping helpers into smaller modules as the Rust store grows

## Next Steps

- commit the `#176` implementation, open a child PR against `codex/issue-172-rust-public-cli`, and merge it
- start `#177` from the refreshed integration branch after the Rust store layer lands

## Artifacts

- `rust/openprecedent-contracts/src/`
- `rust/openprecedent-store-sqlite/src/lib.rs`
