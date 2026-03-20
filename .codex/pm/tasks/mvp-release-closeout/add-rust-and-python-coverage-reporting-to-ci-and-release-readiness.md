---
type: task
epic: mvp-release-closeout
slug: add-rust-and-python-coverage-reporting-to-ci-and-release-readiness
title: Add Rust and Python coverage reporting to CI and release readiness
status: done
task_type: implementation
labels: test
issue: 246
state_path: .codex/pm/issue-state/246-add-rust-and-python-coverage-reporting-to-ci-and-release-readiness.md
---

## Context

The repository runs Python and Rust tests in CI, but it does not yet produce a standard coverage report for either implementation language. Before publishing the MVP release, coverage must become visible and reviewable rather than inferred from test counts alone.

## Deliverable

Standard Rust and Python coverage reporting wired into CI and release-readiness workflows.

## Scope

- choose practical coverage tooling for Python and Rust in this repository
- make coverage results visible in CI or release-readiness outputs
- document how release preparation should read the resulting coverage data
- keep the scope focused on reporting, not yet raising the baseline itself

## Acceptance Criteria

- both Python and Rust code paths produce coverage outputs in a standard workflow
- coverage is visible enough to support release gating decisions
- release-readiness guidance points to the coverage outputs

## Validation

- run the repository coverage workflow locally or through CI
- verify that both language stacks emit coverage data
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

This issue precedes the explicit 90 percent release gate so the repository can measure its baseline before enforcing it.
