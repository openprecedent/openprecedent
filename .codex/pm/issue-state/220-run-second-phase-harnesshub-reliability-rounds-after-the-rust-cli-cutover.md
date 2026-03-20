---
type: issue_state
issue: 220
task: .codex/pm/tasks/codex-runtime-research/run-second-phase-harnesshub-reliability-rounds-after-the-rust-cli-cutover.md
title: Run second-phase HarnessHub reliability rounds after the Rust CLI cutover
status: in_progress
---

## Summary

Run the post-plan HarnessHub research rounds that determine whether decision-lineage invocation and precedent reuse remain reliable after the Rust CLI cutover, then close the study once the evidence spans more than release-only work.

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

## Open Questions

- whether a later follow-up study should isolate the causal contribution of the single-skill `#233` refinement, the user-maintained hidden local AGENTS indirection, the refreshed Rust CLI command entry, or the combination of those factors
- whether contamination and retrieval hygiene become the next primary research risk now that invocation reliability has been re-established under the current local setup
- how the system should explicitly record which retrieved precedent was adopted, ignored, or rejected in the final decision path
- how non-invocation or skipped-invocation rounds should be classified explicitly instead of inferred from missing runtime records
- whether a lightweight closeout-stage capture should summarize validated precedent and noisy retrieval after each completed round

## Next Steps

- prepare the `#220` closeout update and archive the final second-phase conclusion without reopening issue `#131`
- keep the causal-boundary caveat explicit in the closeout: the study validates the current local private-entry setup, not the repository-side skill text in isolation
- treat any follow-up work on causal isolation or contamination as separate research issues rather than blockers to closing `#220`
- link the next-step follow-up issues for adoption tracking, miss classification, closeout capture, and contamination control into the closeout narrative so they carry the remaining research load after `#220` closes
- use `#235`, `#236`, `#237`, and `#163` as the explicit post-`#220` issue set so the closeout can say the main reliability question is answered while the next research questions remain tracked

## Artifacts

- `docs/engineering/validation/harnesshub-second-phase-reliability-plan.md`
- `docs/engineering/validation/harnesshub-second-phase-observation-log.md`
- `research-artifacts/harnesshub/`
