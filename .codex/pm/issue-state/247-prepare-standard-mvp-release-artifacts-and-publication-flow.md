---
type: issue_state
issue: 247
task: .codex/pm/tasks/mvp-release-closeout/prepare-standard-mvp-release-artifacts-and-publication-flow.md
title: Prepare standard MVP release artifacts and publication flow
status: done
---

## Summary

Decide how the MVP release will be packaged and published so a new project can obtain the published baseline in a standard way.

## Outcome

- Added a standard publication-flow document at `docs/product/mvp-release-publication-flow.md`.
- Chose a minimal but standard first-release artifact strategy:
  - validated release commit on `main`
  - annotated `v0.1.0` Git tag
  - GitHub Release
  - release notes
  - GitHub-generated tagged source archives
- Explicitly deferred prebuilt binaries, registry publication, and hosted release surfaces so the first MVP release stays aligned with the current local-first, research-oriented product boundary.
- Added a reusable release-notes template at `docs/product/mvp-release-notes-template.md`.
