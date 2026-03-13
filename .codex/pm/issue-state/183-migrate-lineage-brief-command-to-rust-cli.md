---
type: issue_state
issue: 183
task: .codex/pm/tasks/public-cli-foundation/migrate-lineage-brief-command-to-rust-cli.md
title: Migrate the lineage brief command to the Rust CLI
status: done
---

## Summary

The runtime decision-lineage brief now runs through the Rust public CLI and records stable runtime invocation entries for successful brief requests.

## Validated Facts

- issues `#177` through `#182` already moved the core CRUD, replay, precedent, and capture surfaces into Rust on the integration branch
- the Rust CLI now exposes `lineage brief`
- lineage brief now returns stable Rust contract types and appends runtime invocation records to the resolved invocation-log path
- Rust contract tests cover brief generation from extracted decisions and invocation-log recording with `case_id`, `session_id`, `current_plan`, `candidate_action`, and `known_files`

## Open Questions

- the ranking and brief-shaping helpers currently live in the CLI crate and may still move into shared core helpers if more lineage surfaces converge on the same logic

## Next Steps

- merge this child issue into `codex/issue-172-rust-public-cli`
- continue with `#184` for lineage invocation list and inspect commands

## Artifacts

- `rust/openprecedent-contracts/`
- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/lineage_brief_contract.rs`
- `.codex/pm/tasks/public-cli-foundation/migrate-lineage-brief-command-to-rust-cli.md`
