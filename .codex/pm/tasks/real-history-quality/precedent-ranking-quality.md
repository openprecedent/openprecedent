---
type: task
epic: real-history-quality
slug: precedent-ranking-quality
title: Improve precedent ranking quality on larger real-case history
status: done
labels: feature,test
depends_on: 26
issue: 28
---

## Context

Precedent retrieval works for MVP v1, but the roadmap still calls out ranking quality as a gap once real-case history grows. This should be improved against a stronger real-session corpus, not only against the current curated examples.

## Deliverable

Improve precedent ranking quality on larger real-case history and lock the improvement in with regression coverage.

## Scope

- inspect weak matches and false positives from real-session evaluation
- refine ranking or fingerprint comparison logic for the observed failures
- add regression coverage for the targeted ranking improvements
- preserve existing precedent response structure and contracts

## Acceptance Criteria

- at least one concrete ranking failure from real or anonymized session history is corrected
- the targeted ranking cases improve without regressing existing fixture expectations
- the ranking change is backed by automated regression coverage
- the work remains tied to real-history evidence, not abstract refactoring alone

## Validation

- add or extend tests that exercise the corrected ranking cases
- run precedent-related regression coverage after the ranking logic changes

## Implementation Notes

This task depends on `#26` in the local PM workspace because a stronger real-session fixture set should exist before ranking quality is tuned.
