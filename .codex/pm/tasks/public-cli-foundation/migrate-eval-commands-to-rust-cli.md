---
type: task
epic: public-cli-foundation
slug: migrate-eval-commands-to-rust-cli
title: Migrate eval commands to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 185
---

## Context

Child issue `#185` under `#172` migrates the public evaluation command family into Rust. This slice covers fixture-suite evaluation and collected OpenClaw session evaluation.

## Deliverable

Implement the scoped GitHub issue on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- implement `eval fixtures` in Rust
- implement `eval captured-openclaw-sessions` in Rust
- preserve expected evaluation report formats where they are part of the public contract

## Acceptance Criteria

- evaluation flows run through the Rust CLI
- evaluation outputs are stable enough for automated validation
- the public eval surface no longer depends on Python CLI execution

## Validation

- run `cargo test`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh` before opening the PR

## Implementation Notes

- Reuse the Rust capture, decision extraction, and precedent helpers instead of routing eval through the Python service.
- Keep the JSON report shapes stable because validation harnesses can depend on them directly once the Rust CLI becomes the public surface.

## Completion Notes

- implemented `eval fixtures` and `eval captured-openclaw-sessions` in the Rust CLI
- added Rust evaluation report contracts under `openprecedent-contracts`
- added Rust contract tests for fixture-suite evaluation and collected OpenClaw session evaluation
