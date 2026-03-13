---
type: issue_state
issue: 182
task: .codex/pm/tasks/public-cli-foundation/migrate-codex-capture-commands-to-rust-cli.md
title: Migrate Codex capture commands to the Rust CLI
status: done
---

## Summary

The Codex rollout import surface now runs through the Rust public CLI, including unsupported-record counting, tool-argument cleanup, and tool-output noise stripping.

## Validated Facts

- issues `#177` through `#181` already moved case, event, decision, replay, precedent, and OpenClaw capture into Rust on the integration branch
- the Rust CLI now exposes `capture codex import-rollout`
- Codex rollout normalization now lives in the dedicated `openprecedent-capture-codex` crate instead of the Python CLI
- Rust import preserves unsupported-record counting, tool-argument cleanup, and tool-output noise stripping semantics from the existing Codex rollout fixtures
- new Rust contract tests cover normal rollout import, noisy rollout normalization, and downstream precedent ranking using Codex fixtures

## Open Questions

- future lineage-specific capture work may still decide whether any of these Codex normalization helpers should be shared more broadly across runtime ingestion surfaces

## Next Steps

- merge this child issue into `codex/issue-172-rust-public-cli`
- continue with `#183` for the Rust lineage brief command

## Artifacts

- `rust/openprecedent-capture-codex/`
- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/codex_capture_contract.rs`
- `.codex/pm/tasks/public-cli-foundation/migrate-codex-capture-commands-to-rust-cli.md`
