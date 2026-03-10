---
type: task
epic: semantic-decision-foundation
slug: rebuild-semantic-decision-fixtures-and-tests
title: Rebuild evaluation fixtures and tests for semantic decision lineage
status: in_progress
labels: test,docs
depends_on: 69
issue: 70
---

## Context

The current fixture and test baseline was built around operationally flavored decision expectations.
Once the taxonomy changes, the evaluation layer must be rebuilt so it validates semantic judgment extraction rather than process activity.

## Deliverable

Replace the current decision fixtures and evaluation assertions with semantic decision-lineage fixtures and tests.

## Scope

- add or rewrite fixtures that express task framing, adopted constraints, success criteria, authority confirmation, clarification resolution, and rejected options
- remove or rewrite assertions that treat operational choices as correct decisions
- update API, CLI, and evaluation-suite expectations to reflect the semantic taxonomy
- add negative coverage proving that operational-only sessions do not create decision records

## Acceptance Criteria

- the evaluation suite can distinguish semantic decisions from raw event activity
- tests no longer validate tool selection, file writes, retries, or finalize steps as decision outputs
- new fixtures cover both positive semantic-decision cases and negative operational-only cases
- the semantic taxonomy is consistently reflected across API, CLI, and evaluation tests

## Validation

- run the relevant API and CLI evaluation tests against the new fixtures
- confirm the regression baseline covers both semantic-positive and operational-negative cases

## Implementation Notes

This task should follow the schema and extractor refactor closely so the repository regains a stable regression baseline quickly.
