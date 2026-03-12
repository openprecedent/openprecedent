---
type: issue_state
issue: 155
task: .codex/pm/tasks/codex-runtime-research/improve-harnesshub-decision-lineage-matching-beyond-lexical-overlap.md
title: Improve HarnessHub decision-lineage matching beyond lexical overlap
status: done
---

## Summary

Improve the local matcher so semantically related HarnessHub wording drift ranks the intended prior case more robustly than pure token overlap.

## Validated Facts

- Issue `#154` proved that imported HarnessHub history can produce non-empty `matched_case_ids`.
- With both issue `#45` and issue `#53` imported, wording-drift queries can currently tie or lean toward the structurally similar but less semantically precise prior round.
- The matcher now applies lightweight semantic alias expansion for wording drift such as `states -> classes`, `setup -> required`, and `restored -> imported`.
- Regression coverage now verifies that a wording-drift HarnessHub query ranks issue `#53` above issue `#45`.
- Real local validation against imported issue `#45` and issue `#53` bundles now ranks `case_harnesshub_issue_53_refine-verification-into-explicit-readiness-clas` above `case_harnesshub_issue_45_separate-structural-restore-from-runtime-ready-v`.

## Open Questions

- Follow-up research can measure whether this alias set creates any false-positive inflation outside HarnessHub verification terminology.

## Next Steps

- open the issue-scoped PR for `#155`
- fold the retrieval-quality finding back into the ongoing HarnessHub validation research thread

## Artifacts

- `src/openprecedent/services.py`
- `tests/test_api.py`
