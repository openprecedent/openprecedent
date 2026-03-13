---
type: issue_state
issue: 179
task: .codex/pm/tasks/public-cli-foundation/migrate-decision-commands-to-rust-cli.md
title: Migrate decision commands to the Rust CLI
status: in_progress
---

## Summary

Migrate derived decision extraction and listing from the Python CLI into the Rust public CLI on top of the Rust config and SQLite store layers.

## Validated Facts

- the Rust CLI now implements `decision extract` and `decision list`
- the Rust decision commands derive decisions from Rust-managed event timelines and persist them through the Rust SQLite store
- the initial Rust extraction preserves the current six decision types: task frame, constraint adopted, success criteria set, clarification resolved, option rejected, and authority confirmed
- text rendering for `decision list` now mirrors the existing Python-readable fields: question, chosen action, confidence, goal, why, evidence, constraints, and result
- `cargo test` and `cargo test -p openprecedent-cli` pass with the new decision contract tests

## Open Questions

- whether the next replay/precedent slices should keep extending the CLI binary directly or start moving domain logic into a dedicated Rust core module

## Next Steps

- run local preflight, commit the `#179` slice, open a child PR against `codex/issue-172-rust-public-cli`, and merge it
- start `#180` after the Rust decision commands land in the integration branch

## Artifacts

- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/decision_contract.rs`
- `.codex/pm/issue-state/179-migrate-decision-commands-to-rust-cli.md`
- `.codex/pm/tasks/public-cli-foundation/migrate-decision-commands-to-rust-cli.md`
