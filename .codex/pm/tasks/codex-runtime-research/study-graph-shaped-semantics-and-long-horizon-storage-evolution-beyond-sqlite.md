---
type: task
epic: codex-runtime-research
slug: study-graph-shaped-semantics-and-long-horizon-storage-evolution-beyond-sqlite
title: Study graph-shaped semantics and long-horizon storage evolution beyond SQLite
status: backlog
task_type: research
labels: research
issue: 241
state_path: .codex/pm/issue-state/241-study-graph-shaped-semantics-and-long-horizon-storage-evolution-beyond-sqlite.md
---

## Context

OpenPrecedent currently stores cases, events, decisions, invocation evidence, and precedent data in a local-first SQLite runtime.

That base is still aligned with the current product stage:

- it is simple
- local-first
- auditable
- compatible with the Rust public CLI

At the same time, several later research directions imply more graph-shaped semantics:

- reusable knowledge units above cases
- fact-versus-prescription modeling
- smaller retrieval units
- richer adopted-versus-retrieved relationship tracking

This makes it reasonable to preserve a long-horizon research question about graph-shaped semantics and future storage evolution.
It does not yet justify migrating from SQLite to a graph database or any heavier storage platform.

The current evidence does not show that SQLite is the main bottleneck.
The near-term problems are still retrieval quality, contamination, adoption explainability, miss classification, and lightweight closeout capture.

## Deliverable

Produce a research framing issue for a future study of graph-shaped semantics and possible long-horizon storage evolution beyond SQLite.

## Scope

- study whether the logical model should become more graph-shaped before any decision about physical storage is made
- keep the issue focused on future research framing rather than a storage migration plan
- explain why graph databases, knowledge graphs, or similar systems are not currently justified
- place the issue behind the current higher-priority research problems that still concern quality and explainability

## Acceptance Criteria

- the issue clearly distinguishes logical semantic modeling from physical storage migration
- the issue clearly states why SQLite should remain the current base until stronger evidence appears
- the issue lists the future research questions that would need answers before graph storage could become a justified roadmap choice
- the issue preserves the principle that architecture should evolve only when it addresses a validated product need

## Validation

- verify the issue is labeled `research`
- verify the issue text explicitly says it is a deferred long-horizon direction
- verify the issue text states that graph storage is not a current roadmap commitment

## Implementation Notes

Potential questions to answer later:

- which future queries actually require graph-shaped semantics rather than relational joins and derived indices
- whether the project needs a graph logical model without needing a graph database
- when reusable knowledge layers or smaller retrieval units would become hard to express or maintain on the current base
- what compatibility, distribution, and local-first costs a later storage migration would impose
