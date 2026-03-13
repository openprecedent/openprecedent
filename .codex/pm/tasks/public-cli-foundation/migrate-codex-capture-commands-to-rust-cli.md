---
type: task
epic: public-cli-foundation
slug: migrate-codex-capture-commands-to-rust-cli
title: Migrate Codex capture commands to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 182
---

## Context

Child issue `#182` under `#172` migrates the public Codex rollout import workflow into Rust. This slice covers the stable `capture codex import-rollout` surface and the normalization behavior that downstream replay, decision extraction, and precedent retrieval depend on.

## Deliverable

Implement the scoped GitHub issue on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- implement `capture codex import-rollout` in Rust
- preserve current rollout normalization semantics, including unsupported-record counting and tool-output noise stripping
- keep imported events compatible with existing replay, decision extraction, and precedent ranking behavior
- add Rust contract tests that exercise the current Codex rollout fixtures

## Acceptance Criteria

- Codex rollout capture runs through the Rust CLI without falling back to Python or shell wrappers
- imported data remains compatible with the shared SQLite schema and downstream Rust replay, decision, and precedent commands
- Rust tests cover the normal rollout path and noisy rollout normalization path

## Validation

- run `cargo test`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh` before opening the PR

## Implementation Notes

- Prefer moving Codex rollout normalization helpers into the dedicated `openprecedent-capture-codex` crate instead of embedding more runtime-specific parsing directly into the CLI binary.
- Preserve the JSON output contract because later lineage and skill migrations will invoke this command directly.

## Completion Notes

- implemented `capture codex import-rollout` in the Rust CLI
- moved Codex rollout normalization and unsupported-record classification into the dedicated `openprecedent-capture-codex` crate
- added Rust contract tests for the standard rollout path, noisy rollout normalization, and precedent ranking with Codex fixtures
