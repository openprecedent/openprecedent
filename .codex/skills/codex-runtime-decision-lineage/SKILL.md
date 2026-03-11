---
name: codex-runtime-decision-lineage
description: Use for Codex-driven development work that should retrieve semantic decision-lineage context from OpenPrecedent during execution. Reuses the repository-local runtime workflow instead of introducing a generic multi-runtime abstraction.
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
   If not already set, the workflow script defaults to:
   - `OPENPRECEDENT_HOME=$HOME/.openprecedent/runtime`

3. Run the repository-local workflow script:

```bash
./scripts/run-codex-decision-lineage-workflow.sh \
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

2. If later inspection matters, use:

```bash
./scripts/run-codex-decision-lineage-workflow.sh \
  --inspect-latest \
  --query-reason initial_planning \
  --task-summary "..."
```

This prints the brief first, then inspects the newest recorded invocation from the runtime log.

## Decision Rules

- Prefer `initial_planning` when a task first needs earlier judgment context.
- Prefer `before_file_write` when a semantic constraint or approval should shape a risky change.
- Prefer `after_failure` only when the failure is semantic or directional, not just a transient command problem.
- If the brief is empty, continue normally rather than forcing precedent use.
- If the brief returns constraints, approvals, or rejected options, let those shape the task framing.

## Read Next

- [`docs/engineering/codex-precedent-retrieval-validation.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/codex-precedent-retrieval-validation.md)
- [`docs/engineering/using-openprecedent.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/using-openprecedent.md)
- [`docs/engineering/codex-runtime-decision-lineage-workflow.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/codex-runtime-decision-lineage-workflow.md)
