---
type: issue_state
issue: 261
task: .codex/pm/tasks/codex-runtime-research/study-openprecedent-assisted-agentharnesskit-development-as-a-new-external-validation-track.md
title: Study OpenPrecedent-assisted AgentHarnessKit development as a new external validation track
status: done
---

## Summary

Close out the initial AgentHarnessKit external-validation round as a limited but positive evidence set for OpenPrecedent in a harness-scaffold repository.

## Validated Facts

- issue `#261` exists as a `research` issue
- AgentHarnessKit is a different external repository category than HarnessHub because it focuses on harness infrastructure rather than product delivery
- OpenPrecedent has already been privately activated in the current AgentHarnessKit clone through a local hidden overlay rather than a public repository dependency
- future evidence from that repository should be analyzed separately from the completed HarnessHub studies
- the first AgentHarnessKit wave produced four recorded invocations with non-empty `matched_case_ids`
- the observed query reasons were `initial_planning` and `after_failure`; `before_file_write` did not appear in this sample
- the missing `before_file_write` evidence is best explained by the way the work was later split into issues and PRs after most implementation had already happened
- AgentHarnessKit therefore validates precedent transfer into a new repository category, but not stable reliability in the stronger HarnessHub sense

## Open Questions

- whether future AgentHarnessKit rounds will ever justify a larger follow-on study
- whether a later issue-scoped implementation wave from day one would produce `before_file_write` evidence in this repository category

## Next Steps

- close the initial issue with a limited positive conclusion
- treat any later AgentHarnessKit evidence as a separate future follow-on study rather than leaving this issue open indefinitely

## Artifacts

- `docs/engineering/validation/agentharnesskit-external-validation-observation-log.md`
- `docs/engineering/validation/agentharnesskit-external-validation-closeout.md`
- `research-artifacts/agentharnesskit/README.md`
- `research-artifacts/agentharnesskit/2026-03-20T150227Z/`
