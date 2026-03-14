---
type: issue_state
issue: 210
task: .codex/pm/tasks/real-history-quality/reclassify-repository-local-shell-wrappers-as-internal-only-tooling.md
title: Reclassify repository-local shell wrappers as internal-only tooling
status: in_progress
---

## Summary

Reclassified retained shell wrappers as internal-only repository helpers and tightened wrapper-facing docs so the Rust CLI remains the only supported public interface.

## Validated Facts

- Rust `openprecedent` is already the supported public CLI.
- Multiple wrapper scripts under `scripts/` still provide justified repo-local harness value.
- Current docs still mention some wrappers without always making the internal-only boundary explicit.

## Open Questions

- No wrapper was removed in this issue because each reviewed script still had a justified repo-local harness role.

## Next Steps

- open and merge the issue-scoped PR for #210
- reassess wrapper removal only if a later issue can prove one of these helpers has become redundant

## Artifacts

- `scripts/README.md`
- `docs/engineering/tooling-setup.md`
- `docs/engineering/openclaw-live-validation-harness.md`
- `docs/engineering/openclaw-collector-operations.md`
- `tests/test_codex_runtime_workflow_script.py`
- `tests/test_live_validation_script.py`
