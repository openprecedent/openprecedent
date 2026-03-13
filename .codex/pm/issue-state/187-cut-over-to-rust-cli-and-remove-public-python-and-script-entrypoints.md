---
type: issue_state
issue: 187
task: .codex/pm/tasks/public-cli-foundation/cut-over-to-rust-cli-and-remove-public-python-and-script-entrypoints.md
title: Cut over to the Rust CLI and remove public Python and script entrypoints
status: done
---

## Summary

This issue is executing the final public cutover: the packaged Python `openprecedent` console entrypoint is being removed, remaining operational wrappers now call the Rust binary directly, and the remaining public architecture and operations docs are being rewritten around the Rust CLI command tree.

## Validated Facts

- `pyproject.toml` no longer exposes `openprecedent = "openprecedent.cli:run"`; only the internal PM tool remains under `project.scripts`
- `run-e2e.sh`, `run-collector.sh`, `run-openclaw-live-validation.sh`, and the HarnessHub round import/sync path now execute the Rust `openprecedent` binary and current `capture` / `decision` / `eval` commands directly
- public-facing docs in `docs/engineering/using-openprecedent.md`, `docs/engineering/openclaw-collector-operations.md`, `docs/architecture/mvp-design.md`, and related architecture docs have been updated away from the Python/runtime command surface
- targeted regressions for the cutover surfaces passed locally

## Open Questions

- whether any additional non-public historical validation docs should be normalized now or left for later doc maintenance

## Next Steps

- open the child PR against `codex/issue-172-rust-public-cli`
- merge the completed cutover slice into the integration branch
- merge the fully integrated Rust CLI train back to `main`

## Artifacts

- `pyproject.toml`
- `scripts/run-e2e.sh`
- `scripts/run-collector.sh`
- `scripts/run-openclaw-live-validation.sh`
- `scripts/import_harnesshub_codex_round.py`
- `scripts/sync_harnesshub_shared_runtime.py`
- `docs/engineering/using-openprecedent.md`
- `docs/architecture/mvp-design.md`
