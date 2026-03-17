---
type: issue_state
issue: 220
task: .codex/pm/tasks/codex-runtime-research/run-second-phase-harnesshub-reliability-rounds-after-the-rust-cli-cutover.md
title: Run second-phase HarnessHub reliability rounds after the Rust CLI cutover
status: in_progress
---

## Summary

Run the post-plan HarnessHub research rounds that determine whether decision-lineage invocation and precedent reuse remain reliable after the Rust CLI cutover.

## Validated Facts

- issue `#131` closed the first-phase feasibility question
- issue `#217` defined the second-phase reliability plan and preserved `2026-03-13T082811Z` as additional positive evidence
- the next unanswered question is empirical: whether later repeated rounds keep triggering lineage and returning useful precedent
- HarnessHub issue `#79` completed and merged on `2026-03-15` without any newly recorded OpenPrecedent invocation, making it a clear invocation-adherence miss under the post-cutover workflow
- HarnessHub issues `#81`, `#83`, and `#85` all completed and merged on `2026-03-17` without any new OpenPrecedent invocation records, strengthening the evidence that later rounds can bypass lineage entirely
- HarnessHub issue `#89` and follow-up issue `#93` on `2026-03-17` reintroduced `initial_planning` and `before_file_write` invocation records with non-empty `matched_case_ids`
- The user reported that those successful `#89/#93` rounds also relied on an additional locally maintained hidden file referenced from HarnessHub's `AGENTS.md` to bring the private OpenPrecedent skill into the session, so the positive result cannot yet be attributed solely to the `#233` repository-side skill refinement

## Open Questions

- do later HarnessHub rounds reliably invoke lineage at the intended stages
- when lineage is invoked, does it still return useful precedent often enough to support a reliability claim
- do observed failures point primarily to invocation adherence, retrieval quality, or contamination
- whether the refreshed Rust-CLI-based private skill is actually being composed into current HarnessHub sessions or is still routinely skipped by the main workflow
- whether the decisive factor for the new `#89/#93` positive evidence was the single-skill `#233` refinement, the user-maintained hidden local AGENTS indirection, or the combination of both

## Next Steps

- execute the next HarnessHub rounds under the current Rust CLI and private-skill surface
- archive and interpret each round separately
- update the phase-two study record without reopening issue `#131`
- determine whether the `#79` and `2026-03-17` misses came from workflow-composition drift, task-type-based skipping, or another local session-path gap
- separate repository-side skill changes from user-local hidden-entry changes when interpreting later positive rounds so the study does not over-credit `#233`

## Artifacts

- `docs/engineering/validation/harnesshub-second-phase-reliability-plan.md`
- `docs/engineering/validation/harnesshub-second-phase-observation-log.md`
- `research-artifacts/harnesshub/`
