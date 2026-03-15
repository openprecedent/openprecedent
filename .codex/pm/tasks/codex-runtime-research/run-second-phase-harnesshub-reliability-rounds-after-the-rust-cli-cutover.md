---
type: task
epic: codex-runtime-research
slug: run-second-phase-harnesshub-reliability-rounds-after-the-rust-cli-cutover
title: Run second-phase HarnessHub reliability rounds after the Rust CLI cutover
status: in_progress
task_type: research
labels: docs,test
issue: 220
state_path: .codex/pm/issue-state/220-run-second-phase-harnesshub-reliability-rounds-after-the-rust-cli-cutover.md
---

## Context

Issue `#217` defined the second-phase HarnessHub reliability plan after the first validation closeout.
The next step is no longer planning.
OpenPrecedent now needs actual repeated HarnessHub development rounds that test whether the Rust CLI and updated private-skill path reliably trigger lineage retrieval and whether retrieved precedent remains materially useful.

## Deliverable

Execute the first phase-two HarnessHub research rounds, archive their sanitized evidence, and record whether the post-cutover reliability claim is strengthened, weakened, or still ambiguous.

## Scope

- run new HarnessHub development rounds under the Rust CLI and private-skill surface
- record whether `initial_planning` and `before_file_write` invocations happen as intended
- archive sanitized post-round evidence under `research-artifacts/harnesshub/`
- update the phase-two validation docs with success, failure, or ambiguity judgments
- distinguish invocation-adherence failures from retrieval-quality failures

## Acceptance Criteria

- the repository records at least the first new phase-two execution rounds and their interpretations
- each completed round has both observation evidence and a sanitized archive milestone
- the issue explicitly states whether the current evidence increases, weakens, or leaves ambiguous the post-cutover reliability claim
- contamination-control follow-up is only escalated if it becomes the dominant failure mode

## Validation

- verify the new round evidence is consistent with the phase-two plan in `docs/engineering/validation/harnesshub-second-phase-reliability-plan.md`
- verify each archived round contains sanitized files and a clear interpretation entry
- run repository preflight after the documentation and archive updates

## Artifacts

- `docs/engineering/validation/harnesshub-second-phase-reliability-plan.md`
- `docs/engineering/validation/harnesshub-second-phase-observation-log.md`
- `research-artifacts/harnesshub/`
