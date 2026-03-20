---
type: issue_state
issue: 241
task: .codex/pm/tasks/codex-runtime-research/study-graph-shaped-semantics-and-long-horizon-storage-evolution-beyond-sqlite.md
title: Study graph-shaped semantics and long-horizon storage evolution beyond SQLite
status: backlog
---

## Summary

Preserve a future research direction for graph-shaped semantics and possible long-horizon storage evolution without treating graph databases or storage migration as current roadmap work.

## Validated Facts

- SQLite remains aligned with the current local-first product stage
- several later research threads imply more graph-shaped relationships, but that does not yet prove the need for a graph database
- the current higher-priority bottlenecks remain quality, contamination, adoption explainability, miss classification, and closeout capture

## Open Questions

- which future queries truly require graph-shaped semantics rather than richer relational modeling
- whether the logical model should evolve before any physical storage decision is made
- when a later storage migration would become justified by product need rather than architecture curiosity

## Next Steps

- keep this issue behind the current open research stack
- revisit it only after the nearer-term research produces stronger evidence about future semantic and query requirements

## Artifacts

- `.codex/pm/tasks/codex-runtime-research/study-graph-shaped-semantics-and-long-horizon-storage-evolution-beyond-sqlite.md`
- `.codex/pm/tasks/codex-runtime-research/frame-long-horizon-capture-and-storage-research-after-issue-220.md`
