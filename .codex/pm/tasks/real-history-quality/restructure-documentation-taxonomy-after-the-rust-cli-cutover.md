---
type: task
epic: real-history-quality
slug: restructure-documentation-taxonomy-after-the-rust-cli-cutover
title: Restructure documentation taxonomy after the Rust CLI cutover
status: done
task_type: implementation
labels: docs,cleanup
issue: 211
state_path: .codex/pm/issue-state/211-restructure-documentation-taxonomy-after-the-rust-cli-cutover.md
---

## Context

The Rust CLI cutover left engineering documentation spread across a large flat `docs/engineering/` directory.
That made CLI usage, runtime operations, validation evidence, and governance guidance harder to navigate and increased the cost of maintaining cross-links after public-interface changes.

## Deliverable

Reorganize the engineering documentation into a clearer taxonomy, update README entrypoints, and repair the moved-path references needed to keep the repository documentation and doc-path tests coherent.

## Scope

- move English engineering docs into `cli/`, `runtime/`, `validation/`, and `governance/`
- add a local `docs/engineering/README.md` entrypoint for the new taxonomy
- update README entrypoints and moved-path links in docs and skill references
- update only the minimal surviving doc-path assertions outside `docs/`
- avoid product-code, fixture, and unrelated test churn

## Acceptance Criteria

- the oversized flat engineering docs folder is replaced by clear subcategories
- moved documents remain reachable from README entrypoints
- moved-path links in docs and skill references resolve to the new taxonomy
- only minimal surviving test updates are made outside docs to preserve doc-path assertions
- repo-local validation for the moved docs and updated path assertions passes

## Validation

- run `OPENPRECEDENT_PYTHON_BIN=/workspace/02-projects/incubation/openprecedent/.venv/bin/python ./scripts/run-pytest.sh -q tests/test_e2e_script.py tests/test_live_validation_script.py`
- run `source "$HOME/.cargo/env" && cargo test -p openprecedent-cli`
- run `OPENPRECEDENT_PYTHON_BIN=/workspace/02-projects/incubation/openprecedent/.venv/bin/python ./scripts/run-agent-preflight.sh`

## Implementation Notes

- Keep this branch docs-only aside from the minimal surviving doc-path assertions in `tests/test_e2e_script.py` and `tests/test_live_validation_script.py`.
- Revert any accidental fixture or non-doc path rewrites caused by broad replacement passes.
