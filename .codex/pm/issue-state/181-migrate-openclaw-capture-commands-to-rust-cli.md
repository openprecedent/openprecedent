---
type: issue_state
issue: 181
task: .codex/pm/tasks/public-cli-foundation/migrate-openclaw-capture-commands-to-rust-cli.md
title: Migrate OpenClaw capture commands to the Rust CLI
status: in_progress
---

## Summary

Migrate OpenClaw session discovery and import workflows from the Python CLI into the Rust public CLI.

## Validated Facts

- issues `#177` through `#180` already moved case, event, decision, replay, and precedent into Rust and merged into the integration branch
- Python currently exposes four OpenClaw-facing workflows: session listing, single-session import, bulk collection, and direct JSONL import
- the OpenClaw import path is larger than earlier slices because it includes transcript normalization, collector state, and duplicate-session detection
- later Rust CLI cutover work depends on OpenClaw capture no longer going through Python or shell wrappers

## Open Questions

- how much of the current normalization logic should move into the dedicated `openprecedent-capture-openclaw` crate versus staying in CLI-level orchestration

## Next Steps

- model the Rust output contracts for OpenClaw session references and collection results
- implement Rust session listing
- port single-session import and direct JSONL import
- port bulk collection and state-file behavior
- add contract tests and open a child PR against `codex/issue-172-rust-public-cli`

## Artifacts

- `rust/openprecedent-capture-openclaw/`
- `rust/openprecedent-cli/src/main.rs`
- `.codex/pm/tasks/public-cli-foundation/migrate-openclaw-capture-commands-to-rust-cli.md`
