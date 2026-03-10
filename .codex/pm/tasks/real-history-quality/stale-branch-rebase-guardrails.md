---
type: task
epic: real-history-quality
slug: stale-branch-rebase-guardrails
title: Add harness guardrails for stale branches and missed rebases
status: done
task_type: implementation
labels: feature,ops,test
issue: 114
---

## Context

Even after adding stronger workflow guardrails, branch freshness still depends too much on memory.
In practice, stale branches and missed rebases are often caught late, after review has started or after CI has already run. This creates avoidable churn and repeatedly requires manual reminders.

## Deliverable

A harness-level branch freshness check that detects when the current branch no longer contains the latest `upstream/main` and surfaces that problem earlier through the local pre-push and preflight flows.

## Scope

- add one repository-local branch freshness checker that can be called from shell guardrails and tested independently
- integrate it into the existing pre-push hook
- integrate it into the unified agent preflight script
- document the new freshness expectation in repository governance and tooling docs

## Acceptance Criteria

- the harness can detect when a branch is behind the configured base ref
- the local pre-push path blocks stale branches before push unless explicitly bypassed
- the preflight path fails early on stale branches before later checks run
- the guidance tells the user to rebase onto the latest `upstream/main`

## Validation

- `.venv/bin/pytest tests/test_branch_freshness_script.py`
- `.venv/bin/pytest tests/test_preflight_script.py tests/test_branch_freshness_script.py`

## Implementation Notes

- The first version focuses on detection and messaging, not automatic rebasing.
- The freshness check should remain bypassable for exceptional cases, but the default path should strongly prefer an up-to-date branch before push.
