---
type: issue_state
issue: 251
task: .codex/pm/tasks/mvp-release-closeout/codify-mvp-release-validation-checklist.md
title: Codify the MVP release validation checklist
status: done
---

## Summary

Define a standard release validation checklist for the MVP baseline, including the 90 percent coverage threshold once it is available.

## Outcome

- Added a release-facing checklist at `docs/product/mvp-release-validation-checklist.md`.
- Defined four release-blocking checks:
  - repository preflight
  - the scoped 90 percent MVP coverage gate
  - Rust CLI smoke verification
  - a clean-directory minimal MVP end-to-end loop
- Linked the checklist from the README, MVP release scope, and runtime tooling guide so it becomes the public validation source of truth for MVP publication.
- Added a regression test that keeps the quickstart, release scope, and validation checklist entrypoints aligned.
