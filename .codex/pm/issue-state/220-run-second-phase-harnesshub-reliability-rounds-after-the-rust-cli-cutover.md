---
type: issue_state
issue: 220
task: .codex/pm/tasks/codex-runtime-research/run-second-phase-harnesshub-reliability-rounds-after-the-rust-cli-cutover.md
title: Run second-phase HarnessHub reliability rounds after the Rust CLI cutover
status: done
---

## Summary

The second-phase HarnessHub reliability study is complete.
It determined that the current local private-entry setup repeatedly supports useful decision-lineage invocation across release, governance, PRD, and implementation work after the Rust CLI cutover.

## Validated Facts

- issue `#131` closed the first-phase feasibility question
- issue `#217` defined the second-phase reliability plan and preserved `2026-03-13T082811Z` as additional positive evidence
- the next unanswered question is empirical: whether later repeated rounds keep triggering lineage and returning useful precedent
- HarnessHub issue `#79` completed and merged on `2026-03-15` without any newly recorded OpenPrecedent invocation, making it a clear invocation-adherence miss under the post-cutover workflow
- HarnessHub issues `#81`, `#83`, and `#85` all completed and merged on `2026-03-17` without any new OpenPrecedent invocation records, strengthening the evidence that later rounds can bypass lineage entirely
- HarnessHub issue `#89` and follow-up issue `#93` on `2026-03-17` reintroduced `initial_planning` and `before_file_write` invocation records with non-empty `matched_case_ids`
- The user reported that those successful `#89/#93` rounds also relied on an additional locally maintained hidden file referenced from HarnessHub's `AGENTS.md` to bring the private OpenPrecedent skill into the session, so the positive result cannot yet be attributed solely to the `#233` repository-side skill refinement
- HarnessHub issue `#95` on `2026-03-18` produced a stronger three-stage positive sample with `initial_planning`, `before_file_write`, and `after_failure` invocation records, all with non-empty `matched_case_ids`, during the merged release-candidate round in PR `#96`
- The `#95` positive sample strengthens confidence in the current local private-entry setup, but it still does not isolate whether the decisive factor is the hidden local AGENTS indirection, the repository-side single-skill refinement, the refreshed Rust CLI entrypoint, or their combination
- HarnessHub's subsequent `2026-03-18` release sequence around issues `#98`, `#99`, `#97`, and `#102` produced a dense run of additional planning, write-time, and failure-recovery invocation records with non-empty `matched_case_ids`, extending the positive evidence well beyond a single round
- The current evidence now supports a stronger intermediate claim: the combined local private-entry setup is repeatedly supporting real HarnessHub release work across multiple consecutive rounds, even though the study still does not isolate which individual intervention is necessary or sufficient by itself
- HarnessHub's first `0.2.0`-line tasks on `2026-03-19` also produced new positive evidence: issue `#110` left both planning and write-time invocation records with non-empty `matched_case_ids`, and issue `#104` left a planning-stage invocation record with non-empty `matched_case_ids`
- Those `0.2.0` records show early generalization beyond release-only work, but they are not yet enough to close the study because implementation-heavy `0.2.0` issues have not yet demonstrated the same end-to-end planning/write/failure pattern
- HarnessHub's first implementation-heavy `v0.2.0` wave on `2026-03-19` to `2026-03-20` then produced the missing evidence: issues `#106`, `#107`, `#105`, `#109`, and `#108` all left new planning and/or write-time invocation records with non-empty `matched_case_ids` while the corresponding PRs `#113` to `#117` merged successfully
- With that implementation-wave evidence in place, the main `#220` question has been answered positively: the current local private-entry setup now shows repeated useful invocation across release, governance, PRD, and implementation work rather than only a narrow release corridor
- The `#106` worked example now demonstrates the full decision-influence chain in concrete terms: original task framing, retrieved historical cases, and a narrowing effect on later implementation and validation choices
- The current three-stage evaluation is now stable enough to summarize: `initial_planning` is effective for task framing, `before_file_write` is currently the strongest stage for implementation narrowing, and `after_failure` is less frequent but already validated on real recovery loops
- A final sanitized second-phase archive snapshot now exists at `research-artifacts/harnesshub/2026-03-20T043601Z/`, containing 41 HarnessHub invocation records through the current closeout boundary and covering all three query reasons: `initial_planning`, `before_file_write`, and `after_failure`

## Open Questions

- whether a later follow-up study should isolate the causal contribution of the single-skill `#233` refinement, the user-maintained hidden local AGENTS indirection, the refreshed Rust CLI command entry, or the combination of those factors
- how contamination and retrieval hygiene should be researched now that invocation reliability has been re-established under the current local setup

## Next Steps

- close issue `#220` with the second-phase closeout document rather than reopen `#131`
- keep the causal-boundary caveat explicit: the study validates the current local private-entry setup, not the repository-side skill text in isolation
- continue later research under `#235`, `#236`, `#237`, and `#163`

## Artifacts

- `docs/engineering/validation/harnesshub-second-phase-reliability-plan.md`
- `docs/engineering/validation/harnesshub-second-phase-observation-log.md`
- `docs/engineering/validation/harnesshub-second-phase-reliability-closeout.md`
- `research-artifacts/harnesshub/2026-03-20T043601Z/`
- `research-artifacts/harnesshub/`
