---
type: task
epic: real-history-quality
slug: normalize-github-issue-labels-across-active-and-historical-issues
title: Normalize labels across active and historical GitHub issues
status: done
task_type: implementation
labels: docs
issue: 229
state_path: .codex/pm/issue-state/229-normalize-github-issue-labels-across-active-and-historical-issues.md
---

## Context

Many historical OpenPrecedent GitHub issues were left unlabeled, including already-closed implementation and research issues. That makes the long-term issue archive harder to browse by intent and weakens repository governance around research, harness, feature, and documentation work.

## Deliverable

Backfill appropriate labels across active and historical GitHub issues, add any missing durable label categories required for classification, and record the repository-local outcome so future sessions can rely on a normalized issue archive.

## Scope

- audit open and closed GitHub issues for missing labels
- create missing reusable labels needed for durable classification
- apply appropriate labels to historical and active issues without rewriting the issue archive itself
- update the local PM task twin, issue-state, and epic references for this label-normalization work

## Acceptance Criteria

- all current GitHub issues in the repository have at least one appropriate label
- missing label categories needed for current repository work are created and documented through usage
- open and historical issues are labeled consistently enough to distinguish research, harness, feature, documentation, test, bug, and ops work
- local PM records describe what was normalized and how future sessions should interpret the result

## Validation

- run `gh issue list --state all --limit 200 --json number,labels | jq '[.[] | select((.labels|length)==0)] | length'` and confirm the result is `0`
- inspect a spot-check sample of active and historical issues to confirm expected label assignment
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

- created two new durable GitHub labels for repository classification:
  - `research`
  - `harness`
- backfilled labels across active and historical issues, including already-closed issues
- left existing labels in place and added missing labels rather than rewriting prior labeling decisions
