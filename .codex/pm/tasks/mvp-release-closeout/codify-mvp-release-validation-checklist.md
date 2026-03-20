---
type: task
epic: mvp-release-closeout
slug: codify-mvp-release-validation-checklist
title: Codify the MVP release validation checklist
status: backlog
task_type: docs
labels: documentation,test
issue: 251
state_path: .codex/pm/issue-state/251-codify-mvp-release-validation-checklist.md
---

## Context

The repository already has tests, preflight, and validation docs, but it does not yet have a single release-ready checklist that defines what must pass before the MVP can be published.

## Deliverable

A standard release validation checklist for the MVP baseline.

## Scope

- define the commands and checks required before publication
- include test, preflight, CLI smoke, and minimal end-to-end validation expectations
- explicitly include the coverage threshold as a blocker once the threshold issue is complete
- keep the checklist release-facing and auditable

## Acceptance Criteria

- the repository has one clear MVP release validation checklist
- the checklist identifies which failures block release
- the checklist aligns with the shipped Rust CLI and current local-first MVP scope

## Validation

- review the checklist against current CI and runtime validation paths
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

This issue should consolidate existing validation paths rather than inventing unrelated new validation work.
