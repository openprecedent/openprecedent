---
type: issue_state
issue: 248
task: .codex/pm/tasks/mvp-release-closeout/add-mvp-quickstart-and-new-project-installation-guide.md
title: Add MVP quickstart and new-project installation guide
status: done
---

## Summary

Add a concise quickstart and installation path so a new project can adopt the published MVP without deep repository archaeology.

## Outcome

- Added a dedicated quickstart at `docs/engineering/cli/mvp-quickstart.md`.
- Reordered the public doc entrypoints so README and the longer usage guide point to the quickstart first.
- Validated the documented path from a clean temporary directory through:
  - CLI install
  - case creation
  - event append
  - decision extraction
  - replay
  - precedent retrieval
- Explicitly documented that `$HOME/.cargo/bin` should be kept ahead of older installs in `PATH` so the quickstart does not resolve a stale binary.
