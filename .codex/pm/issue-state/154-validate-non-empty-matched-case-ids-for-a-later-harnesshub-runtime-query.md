---
type: issue_state
issue: 154
task: .codex/pm/tasks/codex-runtime-research/validate-non-empty-matched-case-ids-for-a-later-harnesshub-runtime-query.md
title: Validate non-empty matched_case_ids for a later HarnessHub runtime query
status: done
---

## Summary

Validate that imported HarnessHub searchable history produces non-empty `matched_case_ids` for a later semantically related runtime query.

## Validated Facts

- Issue `#153` now imports exported HarnessHub round bundles into a runtime and extracts searchable decisions.
- The next missing proof point is a later runtime query that actually retrieves one of those imported cases.
- `scripts/run-harnesshub-matched-case-validation.sh` now imports one prior HarnessHub round bundle, runs a later semantically related runtime query, and writes brief plus invocation artifacts.
- Regression coverage now verifies non-empty `matched_case_ids` in an isolated runtime.
- Real validation against the exported HarnessHub issue `#53` bundle produced non-empty `matched_case_ids` pointing to `case_harnesshub_issue_53_refine-verification-into-explicit-readiness-clas`.

## Open Questions

- Retrieval quality still depends on lexical overlap; follow-up issue `#155` should improve matching beyond the stable wording used here.

## Next Steps

- open the issue-scoped PR for `#154`
- continue to follow-up retrieval-quality work in `#155`

## Artifacts

- `scripts/run-harnesshub-matched-case-validation.sh`
- `tests/test_harnesshub_matched_case_validation_script.py`
