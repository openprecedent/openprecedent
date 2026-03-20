---
type: task
epic: codex-runtime-research
slug: study-explicit-adoption-tracking-between-retrieved-precedent-and-final-decisions
title: Study explicit adoption tracking between retrieved precedent and final decisions
status: backlog
task_type: research
labels: research
issue: 235
state_path: .codex/pm/issue-state/235-study-explicit-adoption-tracking-between-retrieved-precedent-and-final-decisions.md
---

## Context

Issue `#220` now shows that the current local private-entry setup can repeatedly retrieve useful precedent across release, governance, PRD, and implementation work.

The next missing piece is not whether retrieval happened, but whether the repository can later explain which retrieved precedent actually changed the final decision path.
Today, the runtime records retrieved context more clearly than adopted context.
That makes the research legible, but still leaves a gap between "retrieved" and "used".

## Deliverable

Produce a research framing document that defines how OpenPrecedent should explicitly record which retrieved precedent units were adopted, ignored, or rejected in later decision-making.

## Scope

- define the distinction between retrieved context and adopted context
- compare candidate recording units such as case-level, constraint-level, caution-level, or brief-level adoption
- identify how later research should represent adopted, ignored, and rejected precedent without overfitting to one current workflow
- preserve compatibility with the existing lineage stages instead of redesigning the whole runtime first

## Acceptance Criteria

- the issue clearly states why adoption tracking is now the next missing explanatory layer after `#220`
- the issue defines concrete research questions for adopted versus ignored versus rejected precedent
- the issue leaves a later implementation team with a decision-complete research target rather than a vague desire for "more explainability"

## Validation

- verify the issue links back to `#220` and preserves the worked-example reasoning from the second-phase study
- verify the local task twin and issue-state capture the same adoption-tracking framing
- keep this issue in backlog until the post-`#220` research queue prioritizes it

## Implementation Notes

Potential questions to answer later:
- should adoption be recorded at the level of retrieved cases or individual constraints/cautions
- should the runtime store explicit "adopted / ignored / rejected" markers or infer them from closeout summaries
- how should adoption tracking interact with future contamination-control work
