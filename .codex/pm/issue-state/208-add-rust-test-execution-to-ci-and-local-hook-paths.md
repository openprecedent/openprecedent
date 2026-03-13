---
type: issue_state
issue: 208
task: .codex/pm/tasks/real-history-quality/add-rust-test-execution-to-ci-and-local-hook-paths.md
title: Add Rust test execution to CI and local hook paths
status: done
---

## Summary

Add a dedicated Rust CI path and a local Rust-test guardrail for preflight and pre-push so Rust regressions surface earlier and more clearly.

## Validated Facts

- the repository now contains a Rust workspace and public CLI
- `python-ci` currently installs Rust but does not expose a dedicated `rust-ci` check
- local preflight and pre-push currently do not run `cargo test` based on Rust-affecting changes
- this is a harness gap because Rust regressions should be caught before or alongside Python CI, not only by manual local discipline

## Open Questions

- whether future CI optimization should avoid rerunning Rust tests in Python-flavored paths when the dedicated Rust job is already sufficient

## Next Steps

- open and merge the issue-scoped PR for `#208`
- reuse the Rust-change guardrail in future local and CI validation flows

## Artifacts

- `.github/workflows/python-ci.yml`
- `scripts/run-agent-preflight.sh`
- `.githooks/pre-push`
- `tests/test_preflight_script.py`
- `tests/test_pre_push_hook.py`
