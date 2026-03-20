---
type: issue_state
issue: 163
task: .codex/pm/tasks/codex-runtime-research/research-contamination-controls-for-decision-lineage-retrieval.md
title: Research contamination controls for decision-lineage retrieval
status: backlog
---

## Summary

Preserve the backlog research context for decision-lineage contamination control now that `#220` has re-established invocation reliability and the next unanswered question is retrieval hygiene rather than basic feasibility.

## Validated Facts

- HarnessHub validation has already produced evidence that matched cases can be retrieved and reused in later live decision-lineage work.
- issue `#163` exists to capture the next research question: preventing partially related cases from contributing irrelevant constraints or cautions.
- `#220` now shifts the center of gravity toward contamination and retrieval hygiene because the system is no longer primarily blocked on invocation reliability.
- this work is not yet urgent enough to move out of backlog.
- the local PM workspace should still track the issue so the reasoning context is not lost when it becomes relevant again.

## Open Questions

- which contamination-control direction should be tested first once the issue is prioritized
- whether contamination should be evaluated at the level of retrieved units, whole cases, or assembled briefs
- how to distinguish helpful recall from noisy context-cost inflation in later experiments
- how adopted-versus-retrieved tracking should interact with contamination analysis

## Next Steps

- keep the task and issue-state in backlog until a concrete contamination failure or stronger product need appears
- use the post-`#220` closeout as the point where contamination becomes a primary follow-up quality question rather than a speculative future topic
- pick up the preserved reasoning context when the research issue is reprioritized

## Artifacts

- `.codex/pm/tasks/codex-runtime-research/research-contamination-controls-for-decision-lineage-retrieval.md`
- `docs/engineering/validation/harnesshub-real-project-observation-log.md`
