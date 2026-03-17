# HarnessHub Second-Phase Observation Log

Use this file during issue `#220` to record post-cutover HarnessHub observations after the second-phase reliability plan from issue `#217` was defined.

The goal is not to reopen the first-phase study from issue `#131`.
The goal is to classify later rounds as positive, negative, or ambiguous evidence for post-Rust-CLI invocation reliability and retrieval usefulness.

## Observation Entries

### Entry Template

- Timestamp:
- HarnessHub issue:
- Development step:
- Query reasons observed:
- Runtime evidence:
- Interpretation:
- Reliability effect:

## Entries

- Timestamp: 2026-03-17, observed from merged issues `#81`, `#83`, and `#85`
- HarnessHub issue: `#81` Document how to interpret harness CLI artifact outputs; `#83` Raise coverage on CLI entrypoints and command/output surfaces; `#85` Raise overall branch coverage to 80 percent
- Development step: complete three consecutive issue rounds through PRs `#82`, `#84`, and `#86`, with a fourth follow-up issue `#87` already opened afterward
- Query reasons observed: none on `2026-03-17`; the shared runtime still contains no records newer than the `2026-03-14` issue `#77` round
- Runtime evidence: HarnessHub completed issue `#81` at `2026-03-17T11:50:04Z`, issue `#83` at `2026-03-17T12:21:40Z`, and issue `#85` at `2026-03-17T12:48:06Z`, with matching merged PRs `#82`, `#84`, and `#86`; a new issue `#87` was opened at `2026-03-17T12:54:54Z`; however, `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` still ends its HarnessHub evidence at `2026-03-14T16:58:22.426163810Z`
- Interpretation: this is stronger negative evidence than the single `#79` miss because it shows multiple later HarnessHub rounds and a new follow-up planning wave all proceeded without entering the lineage path at all; the current post-cutover weakness is still best classified as invocation-adherence or workflow-composition failure, not retrieval degradation
- Reliability effect: materially weakens the current reliability claim for stage-based invocation after the Rust CLI cutover; the evidence now suggests that later HarnessHub work can continue successfully across multiple rounds without triggering the private OpenPrecedent skill

- Timestamp: 2026-03-15, observed from merged issue `#79`
- HarnessHub issue: `#79` Stabilize coverage workflow dependency installation
- Development step: complete issue execution through PR `#80` merge without any newly recorded OpenPrecedent invocation during the same day
- Query reasons observed: none on `2026-03-15`; the shared runtime contains no new `initial_planning`, `before_file_write`, or `after_failure` records for this round
- Runtime evidence: HarnessHub development clearly occurred on `2026-03-15` with commits `19c5c10`, `fb37b74`, `1af6de1`, `bc0190d`, `2205916`, and `086d7c9`, and PR `#80` merged at `2026-03-15T05:45:39Z`; however, `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` contains no `2026-03-15` records even though the Rust-CLI-based private skill had already been installed into HarnessHub on `2026-03-14`
- Interpretation: this round is best classified as an invocation-adherence miss rather than a retrieval-quality regression or a Rust CLI execution failure; the development loop ran and closed successfully, but it did not enter the lineage path at all
- Reliability effect: negative evidence for reliable stage-triggered invocation after the Rust CLI cutover; it suggests the current main HarnessHub workflow still does not consistently compose or execute the private OpenPrecedent skill during every issue round
