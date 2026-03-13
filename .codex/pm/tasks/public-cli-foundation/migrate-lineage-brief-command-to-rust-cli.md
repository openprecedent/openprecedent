---
type: task
epic: public-cli-foundation
slug: migrate-lineage-brief-command-to-rust-cli
title: Migrate the lineage brief command to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 183
---

## Context

Child issue `#183` under `#172` migrates the runtime decision-lineage brief into Rust. This slice defines the first stable machine-facing lineage retrieval surface that skills will call directly.

## Deliverable

Implement the scoped GitHub issue on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- implement `lineage brief` in Rust
- preserve the current semantic retrieval and brief-shaping behavior closely enough for existing research fixtures
- append runtime invocation records to the resolved invocation log path
- define stable Rust JSON contracts for the lineage brief and recorded invocation shape

## Acceptance Criteria

- skills can call `openprecedent lineage brief --format json` without shell wrapper indirection
- successful brief requests append runtime invocation records compatible with the existing log file contract
- Rust tests cover brief generation and invocation-log recording

## Validation

- run `cargo test`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh` before opening the PR

## Implementation Notes

- Treat the lineage brief JSON shape as a long-lived skill contract, not as an internal debug payload.
- Keep invocation logging explicit in the Rust CLI so later `lineage invocation` commands can build on the same stored contract.

## Completion Notes

- implemented `lineage brief` in the Rust CLI with stable JSON and text rendering
- added lineage contract types to `openprecedent-contracts`, including the runtime invocation record shape
- preserved invocation-log recording for successful brief requests and added Rust contract tests for brief generation and log recording
