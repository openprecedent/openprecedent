---
type: issue_state
issue: 246
task: .codex/pm/tasks/mvp-release-closeout/add-rust-and-python-coverage-reporting-to-ci-and-release-readiness.md
title: Add Rust and Python coverage reporting to CI and release readiness
status: done
---

## Summary

Add standard Rust and Python coverage reporting so release readiness can measure the MVP baseline rather than infer it from raw test counts.

## Next Steps

- choose practical coverage tooling for Python and Rust in this repository
- expose the resulting reports in CI or release-readiness workflows
- hand the measured baseline to `#243`

## Progress

- Added a dedicated GitHub `coverage` workflow that runs Python and Rust coverage, publishes a workflow summary, uploads the `coverage/` directory as an artifact, and posts a sticky pull-request comment when possible.
- Added `./scripts/run-coverage.sh` so release-readiness work can generate the same Python and Rust reports locally.
- Added `scripts/render_coverage_summary.py` so Python and Rust coverage outputs render into one markdown summary for workflow and release-readiness review.

## Observed Baseline

Measured locally with `./scripts/run-coverage.sh` on `2026-03-20`:

- Python lines: `83.7%`
- Python statements: `87.6%`
- Python branches: `72.7%`
- Rust lines: `74.7%`
- Rust functions: `60.7%`
- Rust regions: `73.5%`

Issue `#243` should use these reported baselines as the starting point for the explicit `90%` MVP release gate.
