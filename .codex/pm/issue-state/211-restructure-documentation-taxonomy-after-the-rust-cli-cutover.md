---
type: issue_state
issue: 211
task: .codex/pm/tasks/real-history-quality/restructure-documentation-taxonomy-after-the-rust-cli-cutover.md
title: Restructure documentation taxonomy after the Rust CLI cutover
status: done
---

## Summary
The English engineering docs were regrouped into `cli`, `runtime`, `validation`, and `governance` subdirectories after the Rust CLI cutover, and README entrypoints were updated to explain the new taxonomy.

## Validated Facts

- the moved engineering docs now live under category-specific subfolders instead of a flat `docs/engineering/`
- README entrypoints were updated in `README.md`, `docs/README.md`, and `docs/zh/README.md`
- moved-path references in docs and local skill files were updated to the new locations
- the only non-doc test changes kept on this branch are the minimal path assertion updates in `tests/test_e2e_script.py` and `tests/test_live_validation_script.py`

## Open Questions

- none for this issue-scoped move; follow-up cleanup can decide whether to mirror the English taxonomy more fully under `docs/zh/`

## Next Steps

- keep the task twin and issue state marked `done`
- open the issue-scoped PR that closes `#211`

## Artifacts

- `docs/engineering/README.md`
- `docs/engineering/cli/`
- `docs/engineering/runtime/`
- `docs/engineering/validation/`
- `docs/engineering/governance/`
