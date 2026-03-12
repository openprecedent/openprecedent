---
type: task
epic: codex-runtime-research
slug: validate-non-empty-matched-case-ids-for-a-later-harnesshub-runtime-query
title: Validate non-empty matched_case_ids for a later HarnessHub runtime query
status: done
task_type: implementation
labels: feature,test
depends_on: 153
issue: 154
state_path: .codex/pm/issue-state/154-validate-non-empty-matched-case-ids-for-a-later-harnesshub-runtime-query.md
---

## Context

Issue `#153` populates the shared runtime with searchable HarnessHub history, but the research loop is still incomplete until a later runtime query actually retrieves that prior history as non-empty `matched_case_ids`.

## Deliverable

Add a minimal HarnessHub validation flow that seeds one imported prior round, runs a later semantically related runtime query, and records non-empty `matched_case_ids` as durable output.

## Scope

- import one exported HarnessHub round bundle into an isolated runtime
- run one later semantically related runtime decision-lineage query
- capture invocation summary and inspection artifacts showing non-empty matched case ids

## Acceptance Criteria

- at least one later HarnessHub runtime invocation records non-empty `matched_case_ids`
- the matched case is traceable to the imported prior HarnessHub round bundle
- the validation flow is covered by a regression test

## Validation

- run the new HarnessHub matched-case validation harness
- verify the summary artifact contains non-empty `latest_matched_case_ids`
- verify the inspection artifact points back to the imported HarnessHub case id

## Implementation Notes

- Keep this issue focused on validation and evidence production, not retrieval-quality tuning.
- Implemented via `scripts/run-harnesshub-matched-case-validation.sh`.
- Regression coverage added in `tests/test_harnesshub_matched_case_validation_script.py`.
- Real validation against the exported HarnessHub issue `#53` bundle produced non-empty `matched_case_ids` pointing back to the imported prior round.
