---
type: issue_state
issue: 246
task: .codex/pm/tasks/mvp-release-closeout/add-rust-and-python-coverage-reporting-to-ci-and-release-readiness.md
title: Add Rust and Python coverage reporting to CI and release readiness
status: backlog
---

## Summary

Add standard Rust and Python coverage reporting so release readiness can measure the MVP baseline rather than infer it from raw test counts.

## Next Steps

- choose practical coverage tooling for Python and Rust in this repository
- expose the resulting reports in CI or release-readiness workflows
- hand the measured baseline to `#243`
