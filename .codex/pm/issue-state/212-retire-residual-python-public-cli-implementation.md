---
type: issue_state
issue: 212
task: .codex/pm/tasks/real-history-quality/retire-residual-python-public-cli-implementation.md
title: Retire residual Python public CLI implementation
status: in_progress
---

## Summary

Issue #212 removes the retired Python public CLI implementation now that Rust `openprecedent` is the only supported public CLI surface, and updates the remaining collateral references so the repository no longer treats that code as a live contract.

## Validated Facts

- `pyproject.toml` no longer exposes `openprecedent = "openprecedent.cli:run"`.
- The remaining direct code-level dependency on `openprecedent.cli` was `tests/test_cli.py`.
- Collateral references to `tests/test_cli.py` still existed in `tests/test_codex_pm.py` and `tests/test_api.py`.
- `src/openprecedent/cli.py` and `tests/test_cli.py` can be removed without affecting `openprecedent-pm` or the Rust CLI surface.
- Targeted Python regressions, `cargo test`, and repo preflight all pass after the cleanup.

## Open Questions

- No unresolved product-surface questions remain; only PR review and merge are left.

## Next Steps

- Mark the task twin `done`.
- Commit the cleanup on the issue branch and open the PR that closes `#212`.

## Artifacts

- `src/openprecedent/cli.py`
- `tests/test_cli.py`
- `docs/engineering/rust-public-cli-implementation.md`
- `tests/test_rust_cli_workspace.py`
