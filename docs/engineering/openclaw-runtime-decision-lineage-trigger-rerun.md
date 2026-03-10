# OpenClaw Runtime Decision-Lineage Trigger Rerun

## Goal

Record follow-up live runtime checks after the shared OpenPrecedent DB wiring landed, focusing on whether the real OpenClaw loop can retrieve non-empty lineage from shared history and whether the skill now triggers for implicit prior-decision prompts.

## Validation Baseline

- validation date: `2026-03-10`
- repository baseline: `upstream/main` at `f2a23ae`
- OpenClaw profile: `opv80`
- runtime mode: live local agent execution through the OpenClaw gateway
- shared runtime home: `/tmp/openprecedent-opv80-shared`

## Setup

One earlier OpenClaw recommendation session from the same `opv80` profile was imported into the shared OpenPrecedent runtime home:

- source session: `opv80-test-3.jsonl`
- imported case id: `case_opv80_prior_readme`

That prior case produced three semantic decisions:

- `constraint_adopted`
- `success_criteria_set`
- `option_rejected`

The `opv80` gateway was then restarted with:

```bash
OPENPRECEDENT_HOME=/tmp/openprecedent-opv80-shared openclaw --profile opv80 gateway
```

## Prompt Under Test: Explicit Lineage Request

The live agent turn used this constrained recommendation prompt:

`Do not edit code. Before answering, use any relevant prior decision-lineage from OpenPrecedent if available, then provide a short written recommendation only for improving repository navigation.`

## Observed Result: Explicit Lineage Request

In the live session, OpenClaw:

- read the installed `openprecedent-decision-lineage` skill
- executed `openprecedent runtime decision-lineage-brief`
- received a non-empty brief with one matched case from shared history

Observed brief result:

- `matched_cases[0].case_id = case_opv80_prior_readme`
- `similarity_score = 44`
- `accepted_constraints` was non-empty
- `success_criteria` was non-empty

The runtime invocation log was written to:

- `/tmp/openprecedent-opv80-shared/openprecedent-runtime-invocations.jsonl`

The newest invocation record showed:

- `matched_case_ids = ["case_opv80_prior_readme"]`

Meanwhile, the old workspace-local log under `/root/.openclaw-opv80/workspace/openprecedent-runtime-invocations.jsonl` still only contained the earlier empty-brief record from the pre-wiring validation.

## Prompt Under Test: Implicit Prior-Decision Consistency

After updating the installed skill wording to make prior-decision consistency an explicit `initial_planning` trigger, the live agent turn was rerun with:

`Do not edit code. Provide a short written recommendation only for improving repository navigation, and keep it consistent with earlier repository decisions if relevant.`

## Observed Result: Implicit Prior-Decision Consistency

In the same live profile, OpenClaw:

- read the updated installed `openprecedent-decision-lineage` skill
- executed `openprecedent runtime decision-lineage-brief`
- received a non-empty brief with the same shared-history match

Observed brief result:

- `matched_cases[0].case_id = case_opv80_prior_readme`
- `similarity_score = 44`
- `accepted_constraints` was non-empty
- `success_criteria` was non-empty

The shared runtime invocation log gained a new record:

- `recorded_at = 2026-03-10T15:05:59.836511Z`
- `matched_case_ids = ["case_opv80_prior_readme"]`

The corresponding live session still returned a constrained no-code answer rather than drifting into code edits, which means the lineage call happened inside the intended task framing path rather than by forcing an unrelated workflow.

## What This Establishes

These reruns close both gaps that were visible after issue `#80`:

- OpenClaw can now call the lineage skill in a real loop
- the call can read shared prior history instead of an accidental workspace-local empty database
- the invocation log can be captured at the intended shared runtime path
- prompts that ask for consistency with earlier repository decisions can now trigger lineage retrieval without an explicit "use OpenPrecedent" instruction

This validation closes the trigger-policy change tracked in `#94`.
