---
type: issue_state
issue: 153
task: .codex/pm/tasks/codex-runtime-research/import-exported-harnesshub-rounds-into-the-shared-runtime-and-extract-decisions.md
title: Import exported HarnessHub rounds into the shared runtime and extract decisions
status: completed
---

## Summary

Import exported HarnessHub round bundles into the shared runtime and extract searchable decision records.

## Validated Facts

- Issue `#152` now exports completed HarnessHub rounds as round bundles with `round-manifest.json` and importable `events.jsonl`.
- The next missing link is to turn those bundles into actual runtime cases and decisions inside the shared database.
- `scripts/import_harnesshub_codex_round.py` now imports one exported round bundle, creates the case, imports the event JSONL, and runs decision extraction.
- Regression coverage now verifies bundle import and decision extraction in an isolated runtime.
- A real HarnessHub issue `#53` round bundle now imports successfully into an isolated runtime with `1 case / 16 events / 5 decisions`.

## Open Questions

- The importer currently supports an explicit `--skip-if-case-exists` mode; later work can decide whether shared-runtime replay should prefer idempotent defaults.

## Next Steps

- open the issue-scoped PR for `#153`
- continue to `#154` to validate non-empty `matched_case_ids` against the newly populated runtime history

## Artifacts

- `scripts/import_harnesshub_codex_round.py`
- `tests/test_harnesshub_round_import_script.py`
- `research-artifacts/harnesshub-rounds/issue-53-refine-verification-into-explicit-readiness-clas-2026-03-12T082148Z`
