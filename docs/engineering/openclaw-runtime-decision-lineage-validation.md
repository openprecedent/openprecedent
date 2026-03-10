# OpenClaw Runtime Decision-Lineage Validation

## Goal

Record the first repository-local validation baseline for when OpenClaw should call the OpenPrecedent decision-lineage skill and what kind of benefit that brief can realistically provide.

This document is intentionally narrow.
It does not claim that OpenClaw is already runtime-integrated with OpenPrecedent inside a live execution loop.
It defines the current best trigger policy and the expected effect of the brief when the skill is invoked at those moments.

## Validation Baseline

- validation date: `2026-03-10`
- repository baseline: `upstream/main` at `8e62389`
- runtime surface under test:
  - `openprecedent runtime decision-lineage-brief`
  - `skills/openprecedent-decision-lineage/SKILL.md`
- validation mode: repository-local fixture-backed simulation

## What Was Evaluated

The validation focused on three candidate trigger points:

1. `initial_planning`
2. `before_file_write`
3. `after_failure`

The question was not whether the brief can tell OpenClaw which tool to use.
The question was whether the brief can improve semantic task judgment:

- task framing
- accepted constraints
- success criteria
- rejected options
- authority handling

## Recommended Trigger Policy

### Keep: `initial_planning`

Use when:

- the user request contains meaningful constraints
- the task has likely been seen before
- the agent needs to inherit task framing or success criteria before acting

Why it is worth keeping:

- this is the cleanest point to inherit prior judgment without already being committed to a local path
- the brief is most useful here when prior cases encode docs-only scope, output shape, or approval boundaries

Expected benefit:

- better starting task frame
- earlier visibility into accepted constraints
- earlier visibility into rejected options

### Keep: `before_file_write`

Use when:

- the agent is about to modify repository state
- the current task has explicit scope or approval boundaries
- a mistaken write would violate prior or current constraints

Why it is worth keeping:

- this is the highest-value safety checkpoint for semantic lineage reuse
- it helps prevent drift from a recommendation or docs-only task into code modification

Expected benefit:

- stronger constraint adherence
- better recognition of approval boundaries
- fewer writes that violate the intended task frame

### Keep Narrow: `after_failure`

Use only when:

- the failure reveals ambiguity in task direction
- recovery requires re-evaluating constraints or rejected paths
- the failure is semantic, not merely operational

Why it should stay narrow:

- many failures are local tool or command failures and do not justify precedent lookup
- the brief is useful only when the failure changes how the task should be interpreted

Expected benefit:

- better recovery framing
- better avoidance of previously rejected paths
- more explicit re-alignment with success criteria

## Trigger Points Not Recommended As Default

Do not make these default automatic triggers:

- every turn
- every tool call
- every search
- every command failure

Reason:

- these moments add noise faster than they add semantic value
- the current brief is optimized for judgment inheritance, not operational steering

## Observed Value Of The Current Brief

In the current implementation, the decision-lineage brief is best understood as:

- a semantic memory lookup
- a task-framing reminder
- a constraint and authority checkpoint

It is not yet:

- a live planner replacement
- a command recommender
- a tool selector

## Expected Positive Effects

When used at the recommended trigger points, the brief can improve:

- alignment with docs-only or no-code constraints
- retention of explicit human approvals
- awareness of previously rejected directions
- consistency of task framing across similar tasks

## Current Limits

- this validation is fixture-backed and repository-local, not a live OpenClaw runtime A/B experiment
- the brief depends on previously captured semantic decisions; sparse history limits usefulness
- no automatic trigger policy is implemented yet inside OpenClaw
- no quantitative quality delta is claimed yet

## Practical Conclusion

The current best policy is:

1. call the skill at `initial_planning` when semantic ambiguity or strong constraints exist
2. call the skill again at `before_file_write` for high-risk state changes
3. use `after_failure` only for failures that require semantic re-interpretation, not routine operational retries

This is enough to support the next stage of runtime experimentation without pretending that the product has already proven online accuracy gains.

## Next Questions

- which real OpenClaw tasks produce the clearest before/after difference from the brief
- whether `before_file_write` should become mandatory for high-risk task classes
- whether approval-sensitive tasks need a stronger authority-specific brief section
- how to measure semantic-quality improvement beyond anecdotal observation
