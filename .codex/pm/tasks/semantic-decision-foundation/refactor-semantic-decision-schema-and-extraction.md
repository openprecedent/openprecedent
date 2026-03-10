---
type: task
epic: semantic-decision-foundation
slug: refactor-semantic-decision-schema-and-extraction
title: Refactor decision schema and extraction around semantic decision lineage
status: backlog
labels: feature,test
depends_on: 68
issue: 69
---

## Context

The current decision schema and extraction logic still reflect the old operational taxonomy.
That implementation must be replaced so extracted decisions represent semantic judgment lineage instead of process operations.

## Deliverable

Refactor the decision schema and extraction pipeline around the approved semantic taxonomy, removing operational decision types entirely.

## Scope

- replace the current decision taxonomy in schema code with the approved semantic taxonomy
- remove extraction paths that derive decisions from tool calls, file writes, retries, finalize steps, or similar operational events
- extract decisions only from high-value semantic signals such as task framing, constraints, success criteria, clarifications, authority confirmation, or option rejection
- update API, CLI, and replay behavior as needed to reflect the new decision semantics

## Acceptance Criteria

- the decision schema no longer includes operational decision types
- sessions that contain only process operations do not produce precedent-worthy decisions
- sessions with semantic framing, constraints, or explicit judgment changes do produce semantic decisions with supporting evidence
- targeted API and CLI tests cover the new taxonomy and the removal of operational decision extraction

## Validation

- run focused API and CLI tests for extraction, replay, and decision presentation
- confirm that operational-only sessions no longer emit decisions while semantic cases still do

## Implementation Notes

This task depends on the taxonomy definition landing first.
