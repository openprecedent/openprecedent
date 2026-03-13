---
type: issue_state
issue: 184
task: .codex/pm/tasks/public-cli-foundation/migrate-lineage-invocation-inspection-commands-to-rust-cli.md
title: Migrate lineage invocation inspection commands to the Rust CLI
status: done
---

## Summary

Lineage invocation history can now be listed and inspected through the Rust public CLI without falling back to the Python CLI.

## Validated Facts

- issue `#183` already writes runtime lineage invocation records from the Rust CLI
- the Rust CLI now exposes `lineage invocation list` and `lineage invocation inspect`
- Rust inspection preserves the current behavior of returning downstream events and decisions that occurred after the recorded invocation time for the referenced case
- Rust contract tests cover invocation list readability and inspection fidelity against the current JSONL log contract

## Open Questions

- later research tooling may still want higher-level filtering or summary commands beyond the raw list and inspect surfaces

## Next Steps

- merge this child issue into `codex/issue-172-rust-public-cli`
- continue with `#185` for eval command migration

## Artifacts

- `rust/openprecedent-contracts/`
- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/lineage_invocation_contract.rs`
- `.codex/pm/tasks/public-cli-foundation/migrate-lineage-invocation-inspection-commands-to-rust-cli.md`
