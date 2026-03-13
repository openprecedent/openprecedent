---
type: task
epic: public-cli-foundation
slug: cut-over-to-rust-cli-and-remove-public-python-and-script-entrypoints
title: Cut over to the Rust CLI and remove public Python and script entrypoints
status: done
task_type: implementation
labels: cli,rust,interface
issue: 187
state_path: .codex/pm/issue-state/187-cut-over-to-rust-cli-and-remove-public-python-and-script-entrypoints.md
---

## Context

The Rust CLI child issue chain now covers capture, replay, precedent, lineage, evaluation, and skill-facing integration. This final cutover removes the remaining public Python CLI exposure and updates the remaining public docs and internal wrappers so they no longer present the older Python/runtime command surface as supported.

## Deliverable

Implement the scoped GitHub issue on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- remove the public `openprecedent` Python console-script exposure from packaging
- migrate the remaining repository-local operational wrappers to call the Rust binary and Rust command tree directly
- update the remaining public architecture and operations docs to describe the Rust CLI as the supported external interface

## Acceptance Criteria

- satisfy the acceptance criteria in the linked GitHub issue before opening a child PR

## Validation

- `. "$HOME/.cargo/env" && cargo test`
- `./scripts/run-pytest.sh -q tests/test_e2e_script.py tests/test_live_validation_script.py tests/test_harnesshub_round_import_script.py tests/test_harnesshub_shared_runtime_sync_script.py tests/test_cli.py tests/test_rust_cli_workspace.py`
- `./scripts/run-agent-preflight.sh`

## Implementation Notes

- public shell wrappers may remain as repository-local harness helpers, but they must not be documented as the supported product interface
- historical research fixtures that mention the older command surface can remain unchanged because they are evidence artifacts, not current product guidance
