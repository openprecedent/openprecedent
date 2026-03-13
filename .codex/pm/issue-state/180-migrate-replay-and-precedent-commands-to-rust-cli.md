---
type: issue_state
issue: 180
task: .codex/pm/tasks/public-cli-foundation/migrate-replay-and-precedent-commands-to-rust-cli.md
title: Migrate replay and precedent commands to the Rust CLI
status: in_progress
---

## Summary

Migrate replay and precedent lookup from the Python CLI into the Rust public CLI on top of the Rust case, event, and decision layers.

## Validated Facts

- the Rust CLI now implements `replay case` and `precedent find`
- the Rust contracts crate now exposes dedicated `ReplayResponse` and `Precedent` types for stable machine-readable output
- replay derives artifacts from events, persists them through the Rust SQLite store, and returns summary/data compatible with the existing Python output shape
- precedent lookup now computes Rust-native case fingerprints, similarity explanations, and ranked reusable prior cases
- `cargo test` passes with the new replay/precedent contract tests

## Open Questions

- whether the next capture/runtime slices should reuse the current in-binary helper approach or start moving replay/precedent helpers into shared Rust core modules

## Next Steps

- run local preflight, commit the `#180` slice, open a child PR against `codex/issue-172-rust-public-cli`, and merge it
- start `#181` after replay/precedent land in the integration branch

## Artifacts

- `rust/openprecedent-contracts/src/`
- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/replay_precedent_contract.rs`
- `.codex/pm/issue-state/180-migrate-replay-and-precedent-commands-to-rust-cli.md`
