---
type: issue_state
issue: 236
task: .codex/pm/tasks/codex-runtime-research/study-explicit-miss-classification-for-lineage-non-invocation.md
title: Study explicit miss classification for lineage non-invocation
status: backlog
---

## Summary

Preserve the next-step research framing for explicit miss classification now that `#220` had to infer several non-invocation rounds from missing runtime evidence instead of direct miss metadata.

## Validated Facts

- `#79` and the `#81/#83/#85` sequence in `#220` were identifiable misses, but only because development happened without corresponding runtime records
- positive rounds are easier to interpret than negative rounds because the system currently lacks an explicit miss taxonomy
- this issue is research framing only, not an implementation commitment

## Open Questions

- which miss categories are the minimum set worth distinguishing
- whether explicit miss records should be captured per round, per stage, or both

## Next Steps

- keep the issue in backlog until the next research cycle prioritizes explicit miss recording
- use `#79` and `#81/#83/#85` as baseline negative examples when this issue is later elaborated

## Artifacts

- `.codex/pm/tasks/codex-runtime-research/study-explicit-miss-classification-for-lineage-non-invocation.md`
- `docs/engineering/validation/harnesshub-second-phase-observation-log.md`
