---
type: task
epic: local-runtime-validation
slug: standard-e2e-validation
title: Add a standard end-to-end validation script and merge checklist
status: done
labels: feature,docs,test
issue: 88
---

## Context

The repository already documents the OpenClaw full user journey validation flow, but today it is spread across manual commands in docs.
That makes merge-time validation inconsistent for changes that touch the runtime path, collector, replay, extraction, or precedent behavior.

## Deliverable

Add a repository-local script that runs the standard E2E validation flow and document a short merge checklist describing when contributors should use it.

## Scope

- add a script that prepares a clean fixture-backed runtime workspace and runs the standard local E2E CLI flow
- save the step outputs in a predictable location for later inspection
- document when the script should be part of pre-merge validation
- keep the scope focused on local validation rather than CI orchestration or live OpenClaw setup

## Acceptance Criteria

- a contributor can run one script to execute the standard local E2E validation path
- the script uses the existing full-user-journey baseline rather than inventing a different path
- docs explain when to run the script before merge and what outputs it produces

## Validation

- run the new E2E script against a temporary local workspace
- run automated tests covering the script entrypoint and expected outputs

## Implementation Notes
