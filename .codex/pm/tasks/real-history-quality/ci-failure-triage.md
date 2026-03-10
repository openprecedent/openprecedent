---
type: task
epic: real-history-quality
slug: ci-failure-triage
title: Add CI failure triage tooling for the agent development harness
status: done
task_type: implementation
labels: feature,ops,test
issue: 107
---

## Context

The repository already has useful checks, but agents still spend too much time re-reading routine CI failures by hand.
During MVP work, many failures fell into a small number of predictable categories such as markdownlint, python-ci regressions, and PR gate / PM drift checks. The harness should classify those failures quickly and point to the right next step.

## Deliverable

A repository-local CI triage entrypoint that summarizes current PR checks, classifies known failures, and surfaces the most likely next action for an agent developer.

## Scope

- add a local script that inspects GitHub PR check status through `gh`
- classify the repository's current known checks into higher-level categories
- render actionable summaries for failing checks without trying to auto-fix them
- document the triage entrypoint in the local tooling docs

## Acceptance Criteria

- one command can summarize the current PR checks for this repository
- known failures such as `python-ci`, `markdownlint`, and `pr-review-gate` are classified into useful categories
- the output gives an agent enough context to choose the next repair step faster than raw log hunting

## Validation

- `.venv/bin/pytest tests/test_ci_triage_script.py`

## Implementation Notes

- The first version uses `gh pr view --json statusCheckRollup` because the installed `gh pr checks` command does not support JSON output in this environment.
- Focus on classification and concise guidance, not automatic remediation.
