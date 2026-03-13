---
type: task
epic: public-cli-foundation
slug: migrate-skills-and-validation-workflows-from-scripts-to-rust-cli
title: Migrate skills and validation workflows from scripts to the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 186
state_path: .codex/pm/issue-state/186-migrate-skills-and-validation-workflows-from-scripts-to-rust-cli.md
---

## Context

Rust CLI command surfaces for capture, lineage, and evaluation are already implemented under the `#172` integration train, but the skill and validation layers still expose repository-local workflow scripts and older Python-era command names. This issue migrates those entrypoints onto the Rust CLI without waiting for the final public cutover.

## Deliverable

Implement the scoped GitHub issue on a child branch that merges into `codex/issue-172-rust-public-cli`.

## Scope

- migrate private and local skill guidance from script-path invocation to direct Rust CLI usage
- update Codex and HarnessHub validation harness scripts so their runtime queries and inspection steps call the Rust CLI directly
- refresh the key Codex/OpenClaw/HarnessHub validation docs and tests to reference the Rust CLI lineage and capture surfaces

## Acceptance Criteria

- satisfy the acceptance criteria in the linked GitHub issue before opening a child PR

## Validation

- `. "$HOME/.cargo/env" && cargo test`
- `./scripts/run-pytest.sh -q tests/test_codex_runtime_workflow_script.py tests/test_codex_live_validation_script.py tests/test_harnesshub_shared_runtime_sync_script.py tests/test_harnesshub_matched_case_validation_script.py tests/test_harnesshub_skill_install_script.py tests/test_cli.py`
- `./scripts/run-agent-preflight.sh`

## Implementation Notes

- add a repository-local helper for resolving the Rust `openprecedent` binary so internal harness scripts do not fall back to Python CLI entrypoints
- keep repository-local harness scripts only as internal orchestration wrappers; public skill and docs surfaces should show direct `openprecedent ...` usage
