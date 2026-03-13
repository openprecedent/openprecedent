---
type: task
epic: public-cli-foundation
slug: migrate-openclaw-capture-commands-to-rust-cli
title: Migrate OpenClaw capture commands to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 181
---

## Context

Child issue `#181` under `#172` migrates the public OpenClaw capture workflows into Rust. This slice covers session discovery, single-session import, bulk collection, and direct JSONL import for OpenClaw traces.

## Deliverable

Implement the `capture openclaw` command family in Rust on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- implement `capture openclaw list-sessions`
- implement `capture openclaw import-session`
- implement `capture openclaw collect-sessions`
- implement `capture openclaw import-jsonl`
- preserve session-state compatibility and current OpenClaw normalization behavior closely enough for existing fixtures

## Acceptance Criteria

- OpenClaw capture workflows run through the Rust CLI without Python or shell wrappers
- existing session index and transcript fixtures remain usable
- imported data remains compatible with the shared SQLite schema and downstream replay/precedent commands
- Rust tests cover session listing, import, and collection behavior

## Validation

- run `cargo test`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh` before opening the PR

## Implementation Notes

- Prefer reusing or expanding the dedicated `openprecedent-capture-openclaw` crate instead of further bloating the CLI binary.
- Keep the JSON output contract stable because later live-validation and skill migrations will depend on it.

## Completion Notes

- implemented `capture openclaw list-sessions`, `import-session`, `collect-sessions`, and `import-jsonl` in the Rust CLI
- expanded the dedicated `openprecedent-capture-openclaw` crate with session discovery and collector-state helpers
- added Rust contract tests for session listing, direct trace import, single-session import, and duplicate-aware collection
