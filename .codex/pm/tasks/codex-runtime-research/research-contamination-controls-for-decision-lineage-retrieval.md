---
type: task
epic: codex-runtime-research
slug: research-contamination-controls-for-decision-lineage-retrieval
title: Research contamination controls for decision-lineage retrieval
status: backlog
task_type: research
labels: research
issue: 163
state_path: .codex/pm/issue-state/163-research-contamination-controls-for-decision-lineage-retrieval.md
---

## Context

OpenPrecedent has now validated that HarnessHub rounds can be exported, imported into the shared runtime, retrieved as matched cases, and reused in later live decision-lineage queries.

A separate research question is now visible but not yet urgent: the current matcher and brief assembly may still allow partially related cases to contribute irrelevant constraints, success criteria, or cautions into the returned context.

## Deliverable

When prioritized, produce a research plan that compares contamination-control approaches for decision-lineage retrieval and identifies the smallest next experiment worth running.

## Scope

- capture the contamination-risk question without committing to immediate optimization
- preserve candidate directions such as typed memory, provenance-aware brief assembly, scoped retrieval, and graph or relation-aware memory
- defer implementation until a concrete harmful failure or stronger product need is observed

## Acceptance Criteria

- the issue records the contamination-risk question and why it is not yet being optimized
- future work can pick this up without losing the current reasoning context
- the task does not commit the project to a graph or embedding redesign prematurely

## Validation

- verify the issue and local task twin preserve the current reasoning context
- keep the task in backlog until concrete retrieval contamination failures are observed
