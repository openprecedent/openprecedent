---
type: issue_state
issue: 185
task: .codex/pm/tasks/public-cli-foundation/migrate-eval-commands-to-rust-cli.md
title: Migrate eval commands to the Rust CLI
status: done
---

## Summary

The public evaluation command family now runs through the Rust CLI, including fixture-suite evaluation and collected OpenClaw session evaluation.

## Validated Facts

- issues `#177` through `#184` already moved the CRUD, replay, precedent, capture, and lineage observability surfaces into Rust on the integration branch
- the Rust CLI now exposes `eval fixtures` and `eval captured-openclaw-sessions`
- fixture evaluation preserves isolated-database enforcement, decision-type checks, and precedent expectations from the current evaluation suites
- collected OpenClaw session evaluation preserves aggregated counters, unsupported-record summaries, and optional report-file emission

## Open Questions

- later validation flows may still want additional filtering or benchmark-specific summaries on top of these raw evaluation reports

## Next Steps

- merge this child issue into `codex/issue-172-rust-public-cli`
- continue with `#186` for skill and validation workflow migration away from scripts

## Artifacts

- `rust/openprecedent-contracts/src/eval.rs`
- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/eval_contract.rs`
- `.codex/pm/tasks/public-cli-foundation/migrate-eval-commands-to-rust-cli.md`
