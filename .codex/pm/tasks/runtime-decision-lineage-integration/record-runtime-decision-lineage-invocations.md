---
type: task
epic: runtime-decision-lineage-integration
slug: record-runtime-decision-lineage-invocations
title: Record runtime decision-lineage skill invocations
status: done
labels: feature,observability
depends_on: 72
issue: 81
---

## Context

OpenPrecedent can build a decision-lineage brief, but it does not yet record that a runtime skill invocation happened as a structured, inspectable event.
Without that record, later validation cannot reliably answer when OpenClaw called the skill or what task context triggered the lookup.

## Deliverable

Add a minimal runtime observability mechanism that records each decision-lineage skill invocation as structured evidence.

## Scope

- record when the runtime decision-lineage skill is invoked
- record the semantic query context, including `query_reason`, task summary, current plan, candidate action, and known files when available
- make the invocation record visible through stored events, replay, or another inspectable repository-local surface
- keep the scope focused on observability, not evaluation logic

## Acceptance Criteria

- a runtime invocation can be inspected after the fact without relying on terminal scrollback
- the stored record includes enough context to explain why the lookup happened
- the record can be associated with the surrounding case or session history

## Validation

- trigger at least one runtime decision-lineage lookup and verify that the invocation record is visible through a stable local interface

## Implementation Notes

This task is a prerequisite for meaningful real-task runtime validation.
