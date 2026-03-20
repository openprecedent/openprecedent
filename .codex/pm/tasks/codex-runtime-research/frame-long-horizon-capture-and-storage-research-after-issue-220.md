---
type: task
epic: codex-runtime-research
slug: frame-long-horizon-capture-and-storage-research-after-issue-220
title: Frame long-horizon capture and storage research after issue 220
status: done
task_type: research
labels: research
issue: 239
state_path: .codex/pm/issue-state/239-frame-long-horizon-capture-and-storage-research-after-issue-220.md
---

## Context

`#220` closed the second-phase HarnessHub reliability study positively for the current local private-entry setup, private skill, and Rust CLI combination.

That closeout also clarified two deeper base-layer questions that are worth preserving for later research, but are not justified as near-term implementation work:

- whether OpenPrecedent should eventually evolve from explicit agent-triggered semantic capture toward a hybrid model that also includes passive runtime observation
- whether OpenPrecedent should eventually evolve from the current local-first SQLite storage base toward a more graph-shaped semantic model or later storage architecture

Both ideas are strategically relevant, but they are still underspecified.
Without more research, introducing eBPF-style passive capture, graph databases, or other heavier infrastructure would primarily add technical complexity without yet solving a clearly validated bottleneck in the current product stage.

## Deliverable

Create and link two deferred long-horizon research issues and update umbrella issue `#100` with a clearer sequencing note that places them after the current higher-priority quality and explainability research.

## Scope

- define the passive-capture direction as a long-horizon research problem rather than a current implementation goal
- define the graph-shaped semantics and storage-evolution direction as a long-horizon research problem rather than a current migration goal
- state explicitly that the current repository should not adopt those technologies merely because they are available
- write the sequencing rationale back into umbrella issue `#100`

## Acceptance Criteria

- two new GitHub research issues exist for the capture and storage directions
- both issues clearly say they are deferred and should not outrank the current open research issues
- umbrella issue `#100` has a new comment that summarizes:
  - the current research priority order
  - why these two directions are long-horizon only for now
  - why architecture should evolve only in response to validated product problems

## Validation

- verify the new issues are labeled `research`
- verify the issue bodies explicitly reject premature migration or infrastructure expansion
- verify the `#100` comment mentions the existing near-term issues and places the new directions behind them

## Implementation Notes

Important framing points to preserve:

- do not position passive capture as a replacement for the current semantic CLI-triggered model
- do not position graph storage as a foregone conclusion or a short-term roadmap item
- explicitly state that technology should be introduced only when it solves an already-validated product problem
