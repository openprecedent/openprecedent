---
type: issue_state
issue: 243
task: .codex/pm/tasks/mvp-release-closeout/raise-mvp-release-coverage-baseline-to-90-percent.md
title: Raise the MVP release coverage baseline to 90 percent
status: done
---

## Summary

Raise the measured MVP release coverage baseline to 90 percent and make that threshold a release blocker.

## Outcome

- Added a scoped release gate script at `scripts/check_mvp_coverage_gate.py`.
- Wired the gate into `.github/workflows/coverage.yml` so coverage failures block the standard coverage workflow.
- Set the gate boundary to the MVP release surface:
  - Python product modules under `src/openprecedent/`, excluding `codex_pm.py`
  - Rust release implementation library crates under `rust/**/src/lib.rs`, excluding CLI shell glue in `rust/openprecedent-cli/src/main.rs`
- Verified locally on `2026-03-20`:
  - Python release surface: `92.8%` (`1354 / 1459`)
  - Rust release implementation core: `90.6%` (`1266 / 1398`)

## Next Steps

- issue complete once the PR is merged
