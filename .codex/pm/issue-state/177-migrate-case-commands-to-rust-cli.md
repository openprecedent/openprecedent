---
type: issue_state
issue: 177
task: .codex/pm/tasks/public-cli-foundation/migrate-case-commands-to-rust-cli.md
title: Migrate case commands to the Rust CLI
status: in_progress
---

## Summary

Migrate the public `openprecedent case` command family from the Python CLI into the Rust CLI on top of the Rust config and store layers.

## Validated Facts

- the Rust CLI now implements `case create`, `case list`, and `case show`
- the Rust case commands persist and read data through the Rust SQLite store crate, not the Python service layer
- create, list, show, generated case ids, duplicate-case errors, and missing-case errors are covered by Rust integration tests
- `cargo test -p openprecedent-cli` passes with both the doctor/version tests and the new case contract tests

## Open Questions

- whether the next event-command slice should reuse the same one-file CLI shape or split the command handlers into smaller modules first

## Next Steps

- run repository preflight, commit the `#177` implementation, open a child PR against `codex/issue-172-rust-public-cli`, and merge it
- start `#178` after the Rust case commands land in the integration branch

## Artifacts

- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/case_contract.rs`
