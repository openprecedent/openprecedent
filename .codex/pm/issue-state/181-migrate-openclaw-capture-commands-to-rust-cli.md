---
type: issue_state
issue: 181
task: .codex/pm/tasks/public-cli-foundation/migrate-openclaw-capture-commands-to-rust-cli.md
title: Migrate OpenClaw capture commands to the Rust CLI
status: done
---

## Summary

OpenClaw session discovery and import workflows now run through the Rust public CLI, including direct JSONL import, single-session import, and bulk collection with state tracking.

## Validated Facts

- issues `#177` through `#180` already moved case, event, decision, replay, and precedent into Rust and merged into the integration branch
- the Rust CLI now exposes `capture openclaw list-sessions`, `import-session`, `collect-sessions`, and `import-jsonl`
- session discovery supports both `sessions.json` indexes and fallback directory scanning of `*.jsonl` transcripts
- single-session import and bulk collection preserve duplicate-session detection through stored OpenClaw session IDs and collector state files
- Rust contract tests now cover session listing, direct trace import, sample transcript import, and duplicate-aware bulk collection

## Open Questions

- some normalization helpers still live in the CLI crate and may be moved later if capture logic needs stronger reuse across future surfaces

## Next Steps

- merge this child issue into `codex/issue-172-rust-public-cli`
- continue with `#182` for the Codex capture migration slice

## Artifacts

- `rust/openprecedent-capture-openclaw/`
- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/openclaw_capture_contract.rs`
- `.codex/pm/tasks/public-cli-foundation/migrate-openclaw-capture-commands-to-rust-cli.md`
