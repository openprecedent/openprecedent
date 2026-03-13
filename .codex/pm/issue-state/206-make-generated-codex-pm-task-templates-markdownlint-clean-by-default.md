---
type: issue_state
issue: 206
task: .codex/pm/tasks/real-history-quality/make-generated-codex-pm-task-templates-markdownlint-clean-by-default.md
title: Make generated Codex PM task templates markdownlint-clean by default
status: done
---

## Summary

Harden `openprecedent.codex_pm task-new` so generated task twins are markdownlint-clean by default and placeholder content does not leak into rendered issue or PR bodies.

## Validated Facts

- repeated task-twin work has hit the same markdownlint spacing failure on generated empty sections
- the generator currently creates empty Markdown sections for task twins, which is the root cause of the repeated CI failures
- a local harness fix belongs in the generator and regression suite rather than in repeated one-off markdown edits

## Open Questions

- whether any future PM document generators beyond `task-new` should adopt the same placeholder convention for consistency

## Next Steps

- open and merge the issue-scoped PR for `#206`
- rely on the generator-level guardrail instead of manual spacing cleanup for future task twins

## Artifacts

- `src/openprecedent/codex_pm.py`
- `tests/test_codex_pm.py`
