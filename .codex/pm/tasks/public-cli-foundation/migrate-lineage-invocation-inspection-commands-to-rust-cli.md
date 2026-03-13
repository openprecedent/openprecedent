---
type: task
epic: public-cli-foundation
slug: migrate-lineage-invocation-inspection-commands-to-rust-cli
title: Migrate lineage invocation inspection commands to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 184
---

## Context

Child issue `#184` under `#172` migrates lineage invocation observability into Rust. This slice covers listing recorded invocation entries and inspecting one invocation together with downstream case signals.

## Deliverable

Implement the scoped GitHub issue on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- implement `lineage invocation list` in Rust
- implement `lineage invocation inspect` in Rust
- preserve invocation-log readability and downstream inspection fidelity against the current JSONL log contract

## Acceptance Criteria

- invocation history is readable through the Rust CLI
- a recorded invocation can be inspected together with downstream events and decisions when the referenced case exists
- Rust tests cover invocation listing and inspection behavior

## Validation

- run `cargo test`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh` before opening the PR

## Implementation Notes

- Reuse the lineage invocation contract introduced by `#183` instead of inventing a second log shape.
- Keep log-path resolution on the global `--invocation-log` flag and resolved runtime config so skills and harnesses can keep using one path.

## Completion Notes

- implemented `lineage invocation list` and `lineage invocation inspect` in the Rust CLI
- added a Rust inspection contract that combines one invocation with downstream events and decisions
- added Rust contract tests for invocation listing and downstream inspection behavior
