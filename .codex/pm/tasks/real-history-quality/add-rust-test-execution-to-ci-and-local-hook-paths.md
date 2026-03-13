---
type: task
epic: real-history-quality
slug: add-rust-test-execution-to-ci-and-local-hook-paths
title: Add Rust test execution to CI and local hook paths
status: done
task_type: implementation
labels: ops,test
issue: 208
state_path: .codex/pm/issue-state/208-add-rust-test-execution-to-ci-and-local-hook-paths.md
---

## Context
OpenPrecedent now ships a Rust workspace and public CLI, but CI still centers on Python and markdown workflows.
That leaves `cargo test` insufficiently enforced as a first-class CI contract and allows Rust regressions to slip to later discovery.
The repository also lacks a local Rust guardrail in preflight and the pre-push hook when Rust files change.

## Deliverable
Add explicit Rust test execution to CI and to the local hook and preflight path for Rust-affecting changes.

## Scope

- add a dedicated Rust CI job that runs `cargo test`
- keep Rust failures separate from Python failures in GitHub Actions
- trigger local Rust validation from preflight and pre-push when Rust-affecting files change
- add regression coverage for the local Rust-test hook behavior

## Acceptance Criteria

- pull requests run Rust tests in CI through a dedicated check
- local preflight and pre-push run Rust tests when Rust-affecting files change
- Rust failures surface with clear messages locally and in GitHub Actions
- regression coverage protects the local Rust guardrail behavior

## Validation

- run `./scripts/run-pytest.sh -q tests/test_preflight_script.py tests/test_pre_push_hook.py tests/test_rust_cli_workspace.py`
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

- Keep Rust-change detection narrow and explicit so non-Rust branches do not pay an unnecessary local test cost.
