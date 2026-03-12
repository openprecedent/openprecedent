---
type: issue_state
issue: 152
task: .codex/pm/tasks/codex-runtime-research/export-harnesshub-codex-rounds-as-importable-searchable-history-artifacts.md
title: Export completed HarnessHub Codex rounds as importable searchable-history artifacts
status: done
---

## Summary

Export one completed HarnessHub Codex development round as a minimal importable searchable-history bundle.

## Validated Facts

- HarnessHub currently has completed issue-scoped rounds with local task twins, issue-state files, mergeable commit history, and matching runtime invocation records.
- The shared runtime database remains empty for the study, so the first missing link is a durable round export artifact.
- Existing OpenPrecedent event import and decision extraction can consume an `events.jsonl` bundle if the case is created later.

## Open Questions

- How much of the completed round should be exported as synthetic events versus copied as source context only?

## Next Steps

- open PR for review

## Artifacts

- `scripts/export_harnesshub_codex_round.py`
- `tests/test_harnesshub_round_export_script.py`
- `research-artifacts/harnesshub-rounds/issue-53-refine-verification-into-explicit-readiness-clas-2026-03-12T082148Z/`
