---
type: task
epic: real-history-quality
slug: reclassify-repository-local-shell-wrappers-as-internal-only-tooling
title: Reclassify repository-local shell wrappers as internal-only tooling
status: done
task_type: implementation
labels: cleanup,tooling
issue: 210
state_path: .codex/pm/issue-state/210-reclassify-repository-local-shell-wrappers-as-internal-only-tooling.md
---

## Context

Rust `openprecedent` is now the supported public CLI, but repository-local shell wrappers still exist for validation, collection, and harness workflows.
Those wrappers remain useful for repo-local automation, yet some script headers and docs still make them look closer to product-facing entrypoints than they should.

## Deliverable

Reclassify the retained shell wrappers as internal-only repository helpers without removing wrappers that still provide justified repo-local value.

## Scope

- audit retained wrapper scripts under `scripts/`
- add explicit internal-only classification where the wrappers are still valid
- update docs and script inventory text so wrappers are described as repo-local harness helpers around the Rust CLI
- add regression coverage that locks in the new classification language

## Acceptance Criteria

- retained wrappers are clearly marked as internal-only helpers
- product-facing docs continue to point to the Rust CLI as the supported interface
- wrapper docs no longer imply that repository-local shell scripts are public product entrypoints
- targeted regression tests and repository preflight pass

## Validation

- run `./scripts/run-pytest.sh -q tests/test_codex_runtime_workflow_script.py tests/test_live_validation_script.py`
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

- Keep wrappers that still support repo-local harness workflows such as live validation and scheduled collection.
- Prefer reclassification and simplification over removal unless a wrapper is clearly unused and redundant.
