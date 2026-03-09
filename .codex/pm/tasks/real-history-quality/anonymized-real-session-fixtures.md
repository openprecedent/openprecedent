---
type: task
epic: real-history-quality
slug: anonymized-real-session-fixtures
title: Add anonymized real-session fixtures to the evaluation suite
status: backlog
labels: feature,test
issue: 26
---

## Context

Current evaluation coverage is still dominated by curated fixtures. The roadmap explicitly calls for expanding evaluation with real collected trajectories once enough collection volume exists.

## Deliverable

Add an anonymized real-session fixture pack and wire it into the existing evaluation suite so replay, extraction, and precedent behavior are exercised against real trajectories.

## Scope

- select a small set of representative collected sessions
- anonymize them for repository inclusion
- define expected decision and precedent assertions where feasible
- connect the fixture pack to the evaluation flow already used by the repository

## Acceptance Criteria

- the repository contains a small anonymized real-session fixture set
- the fixture suite exercises replay, extraction, and precedent behavior on real trajectories
- CI or local test coverage includes the new fixture pack
- the fixture format remains consistent with the existing OpenClaw session import path

## Validation

- add or extend tests that import and evaluate the anonymized real-session fixtures
- run the relevant evaluation and regression test suite after the fixtures are added

## Implementation Notes

This task likely depends on collector rollout and access to real sessions, but the result should still land as repository-safe anonymized fixtures rather than raw collected data.
