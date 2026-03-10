---
type: task
epic: local-runtime-validation
slug: isolate-fixture-eval-from-used-db
title: Isolate fixture evaluation from reused working databases
status: done
labels: bug,test
issue: 63
---

## Context

The OpenClaw full-user-journey validation found that `openprecedent eval fixtures` is not safe to rerun against a database that already contains the evaluation case ids.
Instead of behaving like an isolated evaluation pass, the command attempts to import the same fixture cases again and fails with event or sequence conflicts.

## Deliverable

Make fixture evaluation safe and predictable when run from a normal working environment, either by isolating evaluation imports from the active database or by failing early with a clear non-partial behavior.

## Scope

- reproduce the current conflict behavior on a reused database
- decide whether fixture evaluation should use an isolated store, namespaced cases, or stricter preflight checks
- prevent partial writes or confusing reuse behavior during evaluation
- document the expected evaluation semantics if they change

## Acceptance Criteria

- rerunning `eval fixtures` against a previously used environment does not leave the user with partial or confusing state
- the command either succeeds safely or fails early with a clear message before partial imports
- the behavior is covered by regression tests

## Validation

- reproduce the current `event conflict` behavior from the full-user-journey validation
- run targeted tests for the chosen isolated or fail-fast behavior

## Implementation Notes

This is a workflow and reliability issue, not just a test harness issue. Human operators and agent workflows should be able to reason about whether evaluation is safe to rerun.
