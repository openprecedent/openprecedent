---
type: task
epic: codex-runtime-research
slug: validate-codex-real-project-decision-lineage-reuse
title: Validate Codex real-project decision-lineage reuse across HarnessHub development
status: done
task_type: research
labels: docs,test
depends_on: 130
issue: 131
state_path: .codex/pm/issue-state/131-validate-codex-real-project-decision-lineage-reuse.md
---

## Context

OpenPrecedent completed the first external-project validation loop for Codex decision-lineage reuse in HarnessHub.
The study started during the target repository's earlier ClawPack phase, survived a repository rename, diagnosed why live matching initially failed, and then closed the missing searchable-history chain until live HarnessHub development finally returned non-empty precedent matches.

## Deliverable

Produce a durable closeout archive for issue `#131` that explains:

- what the study was trying to prove
- what failed during the early rounds
- how the missing retrieval chain was diagnosed
- what follow-up refactors and issue chain closed the gap
- what concrete live-reuse evidence ultimately validated the hypothesis
- what questions remain for future research after this issue is closed

## Scope

- preserve the existing validation plan, observation log, sanitized archives, and final report
- add an explicit archive-style closeout document for the first-phase HarnessHub study
- update local PM state so issue `#131` is represented as archived completed research rather than active work
- close this issue without collapsing future contamination-control or post-cutover reliability work into the same thread

## Acceptance Criteria

- OpenPrecedent contains a closeout document that narrates the first-phase HarnessHub validation from initial failures through final success
- the archive clearly explains the pipeline gap, retrieval-quality gap, rename-trigger gap, and follow-up issue chain that resolved them
- issue `#131` local state is marked done and points future work to separate follow-up issues instead of leaving the issue open as an ambiguous active thread
- the branch is ready to merge as the final archive closeout for `#131`

## Validation

- verify that the closeout archive is consistent with the validation plan, observation log, validation report, and archived research artifacts
- verify that local task and issue-state status are aligned with closing issue `#131`
- run repository preflight after the archive closeout edits

## Implementation Notes

- Historical evidence files may still refer to the target repository's earlier ClawPack naming when describing the earlier phase of the same study.
- Post-Rust-CLI reliability validation should be handled by a new research issue rather than reopening `#131`.
