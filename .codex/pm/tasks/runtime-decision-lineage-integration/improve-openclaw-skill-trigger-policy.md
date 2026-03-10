---
type: task
epic: runtime-decision-lineage-integration
slug: improve-openclaw-skill-trigger-policy
title: Improve OpenClaw trigger policy for decision-lineage skill usage
status: done
labels: feature,docs,test
issue: 94
---

## Context

A fresh rerun of the issue #80 live validation on March 10, 2026 showed that shared-path wiring now works and OpenClaw can retrieve a non-empty decision-lineage brief in a real runtime loop.
The remaining product gap is trigger behavior: OpenClaw still tends to call the lineage skill only when the prompt explicitly says to use OpenPrecedent, rather than for implicit but eligible constrained-task moments.

## Deliverable

Strengthen the OpenClaw-facing decision-lineage skill and its invocation guidance so lineage retrieval is more likely to trigger for the right constrained tasks without requiring an explicit user instruction.

## Scope

- refine skill wording and trigger guidance for initial planning and prior-decision consistency requests
- preserve the current semantic-decision focus and avoid operational imitation
- validate at least one implicit-but-eligible prompt where OpenClaw should now trigger lineage retrieval
- keep impact measurement out of scope for this issue

## Acceptance Criteria

- skill guidance is clearer about when OpenClaw should call decision-lineage retrieval without explicit prompting
- validation covers at least one constrained prompt where lineage retrieval now triggers implicitly
- the trigger-policy change is documented or otherwise inspectable in-repo

## Validation

- rerun the relevant no-code OpenClaw recommendation prompts from the issue #80 validation pattern
- confirm whether OpenClaw invokes the lineage skill for at least one implicit-but-eligible prompt

## Implementation Notes

- Updated the OpenClaw-facing skill wording to treat prior-decision consistency requests as valid `initial_planning` triggers without requiring the user to explicitly say "use OpenPrecedent".
- Documented the trigger-policy guidance in the runtime validation docs and the operator-facing usage guide.
- Live rerun on `2026-03-10` with the prompt `Do not edit code. Provide a short written recommendation only for improving repository navigation, and keep it consistent with earlier repository decisions if relevant.` triggered `openprecedent runtime decision-lineage-brief` and matched `case_opv80_prior_readme` in the shared runtime log.
