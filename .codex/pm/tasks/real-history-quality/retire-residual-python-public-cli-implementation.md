---
type: task
epic: real-history-quality
slug: retire-residual-python-public-cli-implementation
title: Retire residual Python public CLI implementation
status: done
task_type: implementation
labels: cleanup,python
issue: 212
state_path: .codex/pm/issue-state/212-retire-residual-python-public-cli-implementation.md
---

## Context

Rust `openprecedent` is now the supported public CLI, but the repository still carries the retired Python CLI module and its direct test surface.
That leaves a dead public-interface implementation in `src/openprecedent/cli.py` and `tests/test_cli.py` even though packaging and runtime workflows have already cut over to Rust.

## Deliverable

Remove the retired Python public CLI implementation and update remaining references so the repository no longer treats it as an active contract surface.

## Scope

- remove `src/openprecedent/cli.py`
- retire `tests/test_cli.py`
- update collateral tests and documentation that still point at the deleted Python CLI module or legacy test file
- keep Python PM tooling and internal service logic intact

## Acceptance Criteria

- the retired Python CLI module is removed from `src/openprecedent/`
- no repository tests import or execute the old Python CLI surface
- docs describe Rust `openprecedent` as the supported CLI without implying the old Python implementation is still present
- targeted Python regressions, `cargo test`, and repo preflight pass after the cleanup

## Validation

- run `OPENPRECEDENT_PYTHON_BIN=/workspace/02-projects/incubation/openprecedent/.venv/bin/python ./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py tests/test_codex_pm.py tests/test_api.py`
- run `. "$HOME/.cargo/env" && cargo test`
- run `touch .codex-review && OPENPRECEDENT_PYTHON_BIN=/workspace/02-projects/incubation/openprecedent/.venv/bin/python ./scripts/run-agent-preflight.sh`

## Implementation Notes

- Keep historical design-doc comparisons that mention the retired Python CLI when they are explicitly describing what is disallowed after the Rust cutover.
