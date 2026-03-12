---
type: task
epic: codex-runtime-research
slug: improve-harnesshub-decision-lineage-matching-beyond-lexical-overlap
title: Improve HarnessHub decision-lineage matching beyond lexical overlap
status: done
task_type: implementation
labels: feature,test
depends_on: 154
issue: 155
state_path: .codex/pm/issue-state/155-improve-harnesshub-decision-lineage-matching-beyond-lexical-overlap.md
---

## Context

Issue `#154` proves that imported HarnessHub history can be retrieved, but the current matcher still depends mostly on direct token overlap. Two semantically related HarnessHub rounds can tie or rank poorly when later wording drifts away from the earlier issue title and task summary.

## Deliverable

Add the smallest retrieval improvement that makes semantically related HarnessHub wording drift rank the intended prior case more robustly.

## Scope

- diagnose one real HarnessHub wording-drift query against multiple imported prior rounds
- add a minimal matcher improvement beyond raw lexical overlap
- cover the improved ranking with regression tests

## Acceptance Criteria

- a later HarnessHub wording-drift query ranks the semantically related prior case above a nearby distractor round
- regression coverage demonstrates the improved behavior
- the change stays within the existing local-first matcher architecture

## Validation

- run the targeted retrieval regression tests
- reproduce the real HarnessHub two-round query scenario locally
- confirm the semantically related readiness-classes round ranks above the structural-vs-runtime-ready round

## Implementation Notes

- Do not introduce embeddings or broad search infrastructure here.
- Implemented as lightweight semantic alias expansion inside the existing keyword tokenizer.
- Regression coverage added in `tests/test_api.py` for the real HarnessHub issue `#45` versus issue `#53` wording-drift ranking scenario.
- Real local validation against imported issue `#45` and issue `#53` bundles now ranks the issue `#53` readiness-classes round above the issue `#45` structural-vs-runtime-ready round for a wording-drift query.
