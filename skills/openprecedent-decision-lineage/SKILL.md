---
name: openprecedent-decision-lineage
description: Retrieve semantic decision-lineage briefs from OpenPrecedent for task framing, constraints, approvals, and rejected paths.
user-invocable: false
metadata: {"openclaw":{"homepage":"https://github.com/openprecedent/openprecedent","requires":{"bins":["openprecedent"]}}}
---

# OpenPrecedent Decision Lineage

Use this skill when the current task would benefit from prior semantic judgment context rather than raw operational history.

This skill is for:

- initial task framing before execution starts
- high-risk moments before changing repository state
- recovery moments after a failure or ambiguous turn
- user requests that carry strong constraints, approvals, or success criteria

Do not use this skill to look up tool preferences or file-write habits.
Its value is semantic decision lineage, not operational imitation.

## When To Call It

Prefer calling this skill only when at least one of these is true:

- the user introduced a meaningful constraint
- the user clarified or narrowed the task
- a human approval or authority boundary matters
- you are about to commit a high-risk write
- the task resembles a previously solved problem and you need the prior judgment, not just the prior mechanics

Avoid calling it for every turn.
If the task is already straightforward and no semantic ambiguity exists, continue normally.

## How To Call It

Run the OpenPrecedent CLI and ask for a decision-lineage brief.

### Initial planning

```bash
openprecedent runtime decision-lineage-brief \
  --query-reason initial_planning \
  --task-summary "<current task summary>"
```

### Before a risky write

```bash
openprecedent runtime decision-lineage-brief \
  --query-reason before_file_write \
  --task-summary "<current task summary>" \
  --candidate-action "<planned write or change>" \
  --known-file "<candidate file path>"
```

### After failure or ambiguity

```bash
openprecedent runtime decision-lineage-brief \
  --query-reason after_failure \
  --task-summary "<current task summary>" \
  --current-plan "<current plan or attempted path>" \
  --candidate-action "<next recovery idea>"
```

Add multiple `--known-file` flags if specific files are already in scope.

## How To Use The Result

The brief returns:

- `matched_cases`
- `task_frame`
- `accepted_constraints`
- `success_criteria`
- `rejected_options`
- `authority_signals`
- `cautions`
- `suggested_focus`

Use the brief to:

- inherit the right task framing
- carry forward constraints and approvals
- avoid historically rejected paths
- align your next step with prior success criteria

Do not treat the brief as a command dispatcher.
It should influence judgment, not replace local reasoning.

## Decision Rules

- If `matched_cases` is empty, continue without forcing precedent use.
- If `accepted_constraints` or `authority_signals` are present, prefer honoring them over convenient operational habits.
- If `rejected_options` is present, avoid repeating that path unless the current user explicitly overrode the older decision.
- If `suggested_focus` conflicts with the current user instruction, the current user instruction wins.

## Example

Task:

`Do not edit code. Provide a short written recommendation only.`

Useful call:

```bash
openprecedent runtime decision-lineage-brief \
  --query-reason initial_planning \
  --task-summary "Do not edit code. Provide a short written recommendation only."
```

Expected use:

- carry forward docs-only scope
- recognize that code edits are out of bounds
- preserve any approval or authority signals
- avoid drifting into operational behavior that violates the current instruction
