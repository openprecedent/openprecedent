---
name: openclaw-live-validation
description: Use for OpenClaw runtime integration work that should be verified through the real live loop. Tells Codex when to run the live validation harness, how to seed shared history, and how to record outcomes in stable local artifacts.
---

# OpenClaw Live Validation

Use this skill when a change affects the real OpenClaw runtime path rather than only repository-local fixture flows.

Typical triggers:

- changes to `skills/openprecedent-decision-lineage/`
- changes to `scripts/run-openclaw-live-validation.sh`
- changes to shared runtime path wiring
- changes to trigger-policy wording or runtime invocation behavior
- changes to live validation docs that should be verified against reality

Do not use this skill for pure docs-only updates that do not claim a runtime behavior change.

## Goal

Make sure runtime integration work gets a real OpenClaw smoke validation at the right time instead of relying only on local tests or human memory.

This skill should reuse the existing harness entrypoint, not replace it.

## Workflow

1. Confirm that the issue actually touches the live runtime path.
   - If the change is only fixture-backed, use repository-local validation instead.
   - If the change affects runtime integration, continue with this skill.

2. Initialize issue-scoped state if the issue may span multiple sessions.
   - Run:
   - `python3 -m openprecedent.codex_pm issue-state-init <task-path>`

3. Prepare the live validation workspace.
   - Run:
   - `./scripts/run-openclaw-live-validation.sh`
   - If prior shared history is needed, pass:
   - `OPENPRECEDENT_LIVE_SEED_SESSION_FILE=...`
   - `OPENPRECEDENT_LIVE_SEED_SESSION_ID=...`
   - `OPENPRECEDENT_LIVE_SEED_CASE_ID=...`

4. Start the isolated OpenClaw gateway with the generated launcher.
   - Use the launcher written by the harness:
   - `/tmp/openprecedent-openclaw-live/launch-openclaw-gateway.sh`

5. Run one or two minimal smoke prompts.
   - Prefer one implicit prior-decision prompt if trigger behavior matters.
   - Prefer one explicit lineage prompt if runtime retrieval must be proven.

6. Re-run the live harness after the turn.
   - Refresh:
   - `output/03-invocation-summary.json`
   - Inspect:
   - `output/manifest.json`
   - `output/00-profile-workspace.txt` when skill-bundle sync matters

7. Record the result in a stable local place.
   - Update issue state or a validation doc with:
   - what prompt was used
   - whether the skill triggered
   - whether the invocation hit the intended shared runtime home
   - whether a matched case was returned

## Expected Outcomes

The live smoke result should usually be classified as one of:

- not triggered
- triggered but wrote to the wrong runtime path
- triggered with empty brief
- triggered with non-empty brief

That classification should be recorded explicitly so follow-up work can target the right gap.

## Read Next

- [`docs/engineering/openclaw-live-validation-harness.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-live-validation-harness.md)
- [`docs/engineering/openclaw-runtime-decision-lineage-trigger-rerun.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-runtime-decision-lineage-trigger-rerun.md)
- [`docs/engineering/openclaw-real-runtime-decision-lineage-validation.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-real-runtime-decision-lineage-validation.md)
