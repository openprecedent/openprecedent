---
type: task
epic: codex-runtime-research
slug: import-exported-harnesshub-rounds-into-the-shared-runtime-and-extract-decisions
title: Import exported HarnessHub rounds into the shared runtime and extract decisions
status: completed
task_type: implementation
labels: feature,test
depends_on: 152
issue: 153
state_path: .codex/pm/issue-state/153-import-exported-harnesshub-rounds-into-the-shared-runtime-and-extract-decisions.md
---

## Context

Exported HarnessHub round artifacts are only useful if they can be imported into the shared runtime as searchable cases with extracted decisions.
Issue `#131` showed that the shared runtime database currently contains no cases, events, or decisions for the HarnessHub study.

## Deliverable

Import one or more exported HarnessHub round artifacts into the shared runtime database and extract searchable decision records from them.

## Scope

- add the minimal import procedure for exported HarnessHub round artifacts
- extract decisions after import using the existing semantic flow
- verify the shared runtime database is no longer empty for the HarnessHub study

## Acceptance Criteria

- at least one exported HarnessHub round imports successfully into the shared runtime database
- decision extraction produces non-empty decisions for that imported round
- the resulting case can be listed and inspected through existing OpenPrecedent surfaces

## Validation

- import one real exported HarnessHub round
- run decision extraction
- verify the shared runtime database shows non-zero cases, events, and decisions for the study

## Implementation Notes

- This task depends on `#152` and should stop at searchable-history population, not later retrieval tuning.
- Implemented via `scripts/import_harnesshub_codex_round.py`.
- Regression coverage added in `tests/test_harnesshub_round_import_script.py`.
- Real validation imported the exported HarnessHub issue `#53` bundle into an isolated runtime and produced `1 case / 16 events / 5 decisions`.
