---
type: task
epic: public-cli-foundation
slug: migrate-replay-and-precedent-commands-to-rust-cli
title: Migrate replay and precedent commands to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 180
---

## Context

Child issue `#180` under `#172` migrates replay and precedent lookup into the Rust public CLI. This slice should expose the first full read path across stored cases, events, decisions, and derived artifacts.

## Deliverable

Implement Rust `replay case` and `precedent find` on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- replace the placeholder Rust `replay` and `precedent` handlers with real implementations
- add any missing Rust contract types needed for replay and precedent output
- preserve current summary, artifact derivation, and precedent ranking behavior closely enough for downstream automation

## Acceptance Criteria

- `openprecedent replay case <case-id>` returns stable Rust-native replay output
- `openprecedent precedent find <case-id>` returns stable Rust-native precedent output
- replay and precedent lookup do not depend on Python CLI execution
- Rust tests cover representative replay and precedent scenarios plus missing-case handling

## Validation

- run `cargo test`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh` before opening the PR

## Implementation Notes

- Reuse the Rust SQLite store and Rust decision extraction now available from earlier child issues.
- Keep machine-readable JSON shapes stable; text rendering can stay close to the current Python human output.
- Completed on `codex/issue-180-rust-replay-precedent` with Rust-native replay and precedent read paths, dedicated contract types, artifact derivation, and replay/precedent contract tests.
