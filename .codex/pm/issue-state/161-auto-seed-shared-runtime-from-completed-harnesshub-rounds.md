---
type: issue_state
issue: 161
task: .codex/pm/tasks/codex-runtime-research/auto-seed-shared-runtime-from-completed-harnesshub-rounds.md
title: Auto-seed shared runtime from completed HarnessHub rounds
status: done
---

## Summary

Auto-seed the live shared runtime from completed HarnessHub rounds and backfill a baseline searchable history set.

## Validated Facts

- `scripts/sync_harnesshub_shared_runtime.py` now scans completed HarnessHub task twins, resolves a commit from repository history, exports round bundles, and imports missing cases into the chosen runtime.
- `scripts/run-harnesshub-decision-lineage-workflow.sh` now auto-runs shared-runtime sync before the standard decision-lineage brief workflow.
- Regression coverage now verifies both baseline backfill and incremental import of a newly completed round, plus automatic sync before a live brief query.
- Real validation seeded `/root/.openprecedent/runtime` from completed HarnessHub issues `#53`, `#59`, `#61`, and `#62`, producing `cases=19`, `events=154`, and `decisions=73`.
- Real validation then ran the auto-seeded wrapper workflow and retrieved non-empty matched cases from the shared runtime for a live wording-drift query.

## Open Questions

- Some older completed HarnessHub rounds still need stronger commit-resolution heuristics; the sync summary records these as non-fatal unresolved items rather than blocking live workflow.

## Next Steps

- open the issue-scoped PR for `#161`
- fold the shared-runtime seeding result back into the ongoing HarnessHub validation research thread

## Artifacts

- `scripts/sync_harnesshub_shared_runtime.py`
- `scripts/run-harnesshub-decision-lineage-workflow.sh`
- `tests/test_harnesshub_shared_runtime_sync_script.py`
