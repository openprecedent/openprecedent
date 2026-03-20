---
type: task
epic: codex-runtime-research
slug: study-explicit-miss-classification-for-lineage-non-invocation
title: Study explicit miss classification for lineage non-invocation
status: backlog
task_type: research
labels: research
issue: 236
state_path: .codex/pm/issue-state/236-study-explicit-miss-classification-for-lineage-non-invocation.md
---

## Context

During `#220`, several misses had to be inferred from the absence of runtime records rather than from an explicit explanation of why lineage was not invoked.

That was enough for the reliability study, but it leaves a weaker research trail than positive rounds.
The next iteration should study how to classify non-invocation directly instead of reconstructing it from missing records.

## Deliverable

Produce a research framing document that defines an explicit miss-classification model for lineage non-invocation and skipped invocation.

## Scope

- define a small miss taxonomy for lineage not appearing in a round
- include at least: not applicable, local setup unavailable, workflow path skipped, failure before invocation, and unknown/ambiguous
- clarify when a round should be considered a true miss versus an intentional non-use
- preserve the distinction between invocation-adherence problems and retrieval-quality problems

## Acceptance Criteria

- the issue records why missing runtime evidence is currently insufficiently expressive
- the issue defines a compact explicit classification model for future research or implementation
- the issue explains how a miss taxonomy would strengthen future reliability studies beyond `#220`

## Validation

- verify the issue links back to the `#79` and `#81/#83/#85` negative evidence from `#220`
- verify the local task twin and issue-state preserve the same miss-classification framing
- keep this issue in backlog until later research prioritizes explicit miss capture

## Implementation Notes

Potential questions to answer later:

- where should miss classification be recorded: runtime log, issue closeout, or both
- whether explicit non-invocation should be represented per round or per stage
- how to avoid turning every intentional skip into noisy bookkeeping
