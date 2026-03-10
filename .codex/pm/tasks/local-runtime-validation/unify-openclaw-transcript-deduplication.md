---
type: task
epic: local-runtime-validation
slug: unify-openclaw-transcript-deduplication
title: Unify OpenClaw transcript deduplication across manual import and collector
status: done
labels: bug,test
issue: 64
---

## Context

The OpenClaw full-user-journey validation found that manual transcript import and background collection do not share one deduplication contract.
If a transcript is manually imported first and later discovered by the collector, the collector can attempt to import the same transcript again under a different derived case id, hit a global event-id conflict, and leave behind an empty case shell.

## Deliverable

Unify transcript identity and deduplication across manual import and collector flows so the same OpenClaw session cannot create conflicting duplicate cases or empty partial cases.

## Scope

- reproduce the duplicate transcript path across manual import and collector workflows
- define one durable identity rule for an OpenClaw transcript or session
- prevent duplicate imports from creating conflicting event ids or empty residual cases
- add regression coverage for mixed manual-import and collector scenarios

## Acceptance Criteria

- the same transcript cannot be imported twice through different OpenClaw entry paths in a way that leaves conflicting duplicate state
- collector and manual import share a consistent transcript identity rule
- failed duplicate attempts do not leave behind empty cases
- regression tests cover the mixed-flow scenario

## Validation

- reproduce the conflict and empty-case behavior from the full-user-journey validation
- run targeted tests for manual import followed by collector import of the same transcript

## Implementation Notes

The fix should optimize for real user journey safety rather than only for collector-state bookkeeping.
