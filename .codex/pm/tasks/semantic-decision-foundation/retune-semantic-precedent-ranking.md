---
type: task
epic: semantic-decision-foundation
slug: retune-semantic-precedent-ranking
title: Retune precedent ranking toward semantic decision similarity
status: backlog
labels: feature,test
depends_on: 69
issue: 71
---

## Context

Current precedent behavior still leans on operational signals such as shared tools, file targets, or similar process patterns.
After the decision model is corrected, precedent retrieval should prioritize semantic judgment similarity instead.

## Deliverable

Retune precedent ranking so semantic decision-lineage signals dominate operational pattern matching.

## Scope

- review the current precedent fingerprint and scoring inputs
- reduce or remove operational signals as primary precedent drivers
- promote semantic decision signals such as task framing, constraints, success criteria, rejected options, and authority patterns
- add evaluation coverage that demonstrates semantic similarity ranking behavior

## Acceptance Criteria

- precedent retrieval no longer relies primarily on shared operational patterns
- semantic decision signals materially affect ranking order
- new evaluation coverage proves that cases with shared judgment lineage outrank cases that only share tool or file behavior
- documentation reflects the shift from operational precedent to semantic precedent

## Validation

- run precedent-related tests and any targeted ranking evaluation fixtures
- review ranked results on representative cases to confirm semantic similarity dominates operational overlap

## Implementation Notes

This task depends on the semantic decision extraction baseline being in place first.
