---
type: issue_state
issue: 178
task: .codex/pm/tasks/public-cli-foundation/migrate-event-commands-to-rust-cli.md
title: Migrate event commands to the Rust CLI
status: done
---

## Summary

Migrate the public `openprecedent event` command family from the Python CLI into the Rust CLI on top of the Rust config and SQLite store layers.

## Validated Facts

- the Rust CLI now implements `event append` and `event import-jsonl`
- the Rust event commands persist and read data through the Rust SQLite store crate, not the Python service layer
- event append covers generated event ids, case existence checks, payload parsing, and sequence allocation
- event import ingests canonical event JSONL records, supports `--case-id` fallback, preserves case completion summary/status transitions, and errors when `case_id` is missing
- the shared Rust event contract now serializes `EventType` with the existing dotted public values such as `message.agent` and `case.completed`
- `cargo test` and `cargo test -p openprecedent-cli -p openprecedent-contracts` pass with the new event contract tests

## Open Questions

- whether the next replay/decision slices should keep extending `main.rs` directly or extract command handlers into smaller modules as the Rust surface grows

## Next Steps

- keep this slice as merged history on `codex/issue-172-rust-public-cli`
- include the event command family in the final integration PR that closes `#172`

## Artifacts

- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/event_contract.rs`
- `rust/openprecedent-contracts/src/event.rs`
- `.codex/pm/tasks/public-cli-foundation/migrate-event-commands-to-rust-cli.md`
