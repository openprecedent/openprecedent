---
type: task
epic: codex-runtime-research
slug: auto-seed-shared-runtime-from-completed-harnesshub-rounds
title: Auto-seed shared runtime from completed HarnessHub rounds
status: done
task_type: implementation
labels: feature,test
depends_on: 155
issue: 161
state_path: .codex/pm/issue-state/161-auto-seed-shared-runtime-from-completed-harnesshub-rounds.md
---

## Context

OpenPrecedent can now export completed HarnessHub rounds, import them into a runtime, extract searchable decisions, validate non-empty `matched_case_ids`, and improve retrieval under wording drift.

But the live shared runtime used by current HarnessHub development still remained empty because completed rounds were not automatically imported into it.

## Deliverable

Build a minimal shared-runtime seeding loop that automatically imports newly completed HarnessHub rounds into the shared runtime and backfills a baseline set of previously completed HarnessHub rounds.

## Scope

- define the minimal trigger or command flow that treats a completed HarnessHub round as ready for shared-runtime ingestion
- backfill a small baseline set of prior completed HarnessHub rounds into the shared runtime
- verify that the shared runtime database used by live development now contains non-zero HarnessHub cases, events, and decisions

## Acceptance Criteria

- newly completed HarnessHub rounds are automatically imported into the shared runtime through the defined workflow
- previously completed HarnessHub rounds are backfilled into the shared runtime as baseline searchable history
- the shared runtime used by real HarnessHub development shows non-zero `cases`, `events`, and `decisions` after seeding
- the automatic import path is verified as successful and documented as the expected live-development workflow

## Validation

- run the automatic import workflow against at least one newly completed HarnessHub round
- backfill at least two prior completed HarnessHub rounds into the same shared runtime
- inspect the shared runtime database and confirm non-zero `cases`, `events`, and `decisions`
- record the resulting evidence in the HarnessHub validation log and sanitized archive artifacts

## Implementation Notes

- Implemented with `scripts/sync_harnesshub_shared_runtime.py` and `scripts/run-harnesshub-decision-lineage-workflow.sh`.
- Regression coverage added in `tests/test_harnesshub_shared_runtime_sync_script.py`.
- Real validation seeded `/root/.openprecedent/runtime` from completed HarnessHub issues `#53`, `#59`, `#61`, and `#62`, resulting in `cases=19`, `events=154`, and `decisions=73`.
- Real validation then used the auto-seeded wrapper workflow to retrieve non-empty matched cases from the shared runtime during a live `before_file_write` query.
