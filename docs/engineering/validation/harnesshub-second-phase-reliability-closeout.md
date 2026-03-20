# HarnessHub Second-Phase Reliability Closeout

Date: 2026-03-20

Issue `#220` closes the second-phase reliability study that followed the first-phase HarnessHub feasibility closeout in `#131`.

## Outcome

The main second-phase question is now answered positively:
under the current local private-entry setup, OpenPrecedent repeatedly supports useful decision-lineage retrieval across multiple HarnessHub task classes after the Rust CLI cutover.

This study no longer depends on a narrow release-only corridor.
By the end of the study, positive evidence spans:

- release execution and release recovery
- governance and repository-policy documentation
- PRD and product-direction planning
- implementation-heavy `v0.2.0` feature work

## What Was Validated

The study validated that the current setup repeatedly leaves useful runtime evidence at the intended stages:

- `initial_planning`
- `before_file_write`
- `after_failure`

It also validated that returned precedent remained materially useful rather than empty or obviously unrelated:

- the recorded rounds repeatedly returned non-empty `matched_case_ids`
- the matched cases remained semantically aligned with the later HarnessHub work
- the `#106` worked example shows a full chain from recorded task input, to retrieved historical cases, to later implementation narrowing

## Evidence Progression

The study moved through three phases of evidence:

1. negative evidence
   - `#79` and the `#81/#83/#85` sequence showed that post-cutover HarnessHub work could still bypass lineage entirely
2. restored positive evidence
   - `#89/#93` reintroduced planning and write-time invocation
   - `#95`, `#98`, and `#102` extended that into a denser release sequence with real `after_failure` recovery samples
3. generalized positive evidence
   - `#110` and `#104` showed the pattern extending beyond release work
   - `#106/#107/#105/#109/#108` supplied the missing implementation-heavy `v0.2.0` wave

That progression is enough to close the reliability question without claiming that every possible future task type has already been sampled.

## Boundary of the Conclusion

This closeout is intentionally narrower than a claim about any one repository-side change in isolation.

The study validates the current combined local setup:

- the user-maintained hidden local AGENTS indirection
- the private OpenPrecedent skill
- the refreshed Rust CLI entrypoint

The study does **not** isolate which one of those factors is individually necessary or sufficient.

## Follow-Up Research

The remaining questions are no longer blockers to `#220`.
They are tracked as follow-up research:

- `#235` explicit adoption tracking between retrieved precedent and final decisions
- `#236` explicit miss classification for lineage non-invocation
- `#237` lightweight closeout capture for precedent validation and retention
- `#163` contamination and retrieval-hygiene follow-up

## Artifacts

- `docs/engineering/validation/harnesshub-second-phase-reliability-plan.md`
- `docs/engineering/validation/harnesshub-second-phase-observation-log.md`
- `docs/engineering/validation/harnesshub-second-phase-reliability-closeout.md`
- `research-artifacts/harnesshub/2026-03-20T043601Z/`
