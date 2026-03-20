---
type: issue_state
issue: 235
task: .codex/pm/tasks/codex-runtime-research/study-explicit-adoption-tracking-between-retrieved-precedent-and-final-decisions.md
title: Study explicit adoption tracking between retrieved precedent and final decisions
status: backlog
---

## Summary

Preserve the next-step research framing for explicit adoption tracking now that `#220` has shown repeated retrieval, but the system still records retrieved precedent more clearly than adopted precedent.

## Validated Facts

- issue `#220` established that precedent retrieval is now repeatedly happening across release, governance, PRD, and implementation work
- the next missing explanatory layer is explicit adoption tracking: which retrieved precedent units were adopted, ignored, or rejected later
- this issue is research framing only, not an implementation commitment

## Open Questions

- should adoption be tracked at the case level, the individual constraint/caution level, or both
- how should a later system distinguish adopted, ignored, and rejected precedent without adding excessive burden to normal development

## Next Steps

- keep the issue in backlog until post-`#220` follow-up research prioritizes adoption tracking
- use the `#106` worked example from `#220` as an initial reference point when this issue is later picked up

## Artifacts

- `.codex/pm/tasks/codex-runtime-research/study-explicit-adoption-tracking-between-retrieved-precedent-and-final-decisions.md`
- `docs/engineering/validation/harnesshub-second-phase-observation-log.md`
