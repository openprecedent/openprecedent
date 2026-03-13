---
type: task
epic: public-cli-foundation
slug: migrate-case-commands-to-rust-cli
title: Migrate case commands to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 177
state_path: .codex/pm/issue-state/177-migrate-case-commands-to-rust-cli.md
---

## Context

The Rust CLI now has global config handling and a reusable SQLite store layer.
This slice migrates the first public domain command family, `openprecedent case`, off the Python CLI and onto the Rust binary using the new store.

## Deliverable

Implement `case create`, `case list`, and `case show` directly in the Rust CLI, preserving the expected JSON behavior and key error semantics.

## Scope

- replace the placeholder Rust `case` command tree with real create/list/show handling
- connect the Rust `case` command family to the Rust SQLite store
- preserve expected machine-readable JSON output for create, list, and show
- preserve user-facing error cases for duplicate case ids and missing case ids
- add Rust integration tests that exercise the `case` surface through the compiled binary

## Acceptance Criteria

- the public `case` command family runs through the Rust binary
- machine-readable output is stable enough for automation and test fixtures
- case operations do not call the Python CLI or shell wrappers
- Rust integration tests cover create, list, show, generated ids, and duplicate or missing-case failures

## Validation

- run `. \"$HOME/.cargo/env\" && cargo test -p openprecedent-cli`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`

## Implementation Notes

- The Rust CLI now generates `case_<12 hex chars>` ids when `--case-id` is omitted, matching the current Python behavior.
- Text rendering remains human-focused, but JSON output is the contract surface for automation.
