---
name: codex-runtime-decision-lineage
description: Use for Codex-driven development work that should retrieve semantic decision-lineage context from OpenPrecedent during execution through the Rust public CLI.
---

# Codex Runtime Decision Lineage

Use this skill when Codex is working inside a real development task and should consult prior semantic judgment from OpenPrecedent.

Typical triggers:

- the task asks to stay consistent with earlier repository decisions
- the user adds meaningful constraints, approvals, or success criteria
- the task is about to drift into a broader path and prior narrowing decisions may matter
- the current work resembles a previously solved Codex development problem

Do not use this skill to retrieve tool preferences or mechanical file-write habits.
Its purpose is semantic judgment reuse, not operational imitation.

## Goal

Give Codex a narrow, inspectable runtime workflow for:

1. requesting a semantic decision-lineage brief
2. keeping runtime persistence on a stable shared OpenPrecedent home
3. inspecting the resulting invocation when later validation needs to understand what happened

## Workflow

1. Make sure the task has enough semantic context.
   At minimum, provide:
   - `--task-summary`
   - the appropriate `--query-reason`

2. Prefer a stable runtime home.
   If not already set, use:
   - `OPENPRECEDENT_HOME=$HOME/.openprecedent/runtime`

3. Resolve the Rust CLI binary once per session:

```bash
if [[ -x ./target/release/openprecedent ]]; then
  OPENPRECEDENT_BIN=./target/release/openprecedent
elif [[ -x ./target/debug/openprecedent ]]; then
  OPENPRECEDENT_BIN=./target/debug/openprecedent
else
  cargo build -q -p openprecedent-cli
  OPENPRECEDENT_BIN=./target/debug/openprecedent
fi
```

1. Run the Rust CLI directly:

```bash
"$OPENPRECEDENT_BIN" \
  --home "$HOME/.openprecedent/runtime" \
  --format json \
  lineage brief \
  --query-reason initial_planning \
  --task-summary "Do not edit code. Provide a short written recommendation only and keep it consistent with earlier Codex runtime decisions."
```

1. Add context when needed.
   Useful optional flags:
   - `--current-plan`
   - `--candidate-action`
   - `--known-file`
   - `--case-id`
   - `--session-id`

1. If later inspection matters, inspect the recorded invocation explicitly:

```bash
"$OPENPRECEDENT_BIN" --home "$HOME/.openprecedent/runtime" --format json lineage invocation list
"$OPENPRECEDENT_BIN" --home "$HOME/.openprecedent/runtime" --format json lineage invocation inspect --invocation-id <id>
```

## Decision Rules

- Prefer `initial_planning` when a task first needs earlier judgment context.
- Prefer `before_file_write` when a semantic constraint or approval should shape a risky change.
- Prefer `after_failure` only when the failure is semantic or directional, not just a transient command problem.
- If the brief is empty, continue normally rather than forcing precedent use.
- If the brief returns constraints, approvals, or rejected options, let those shape the task framing.

## Read Next

- [`docs/engineering/validation/codex-precedent-retrieval-validation.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/codex-precedent-retrieval-validation.md)
- [`docs/engineering/cli/using-openprecedent.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/using-openprecedent.md)
- [`docs/engineering/runtime/codex-runtime-decision-lineage-workflow.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-decision-lineage-workflow.md)
