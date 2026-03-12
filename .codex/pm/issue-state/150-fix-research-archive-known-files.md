---
type: issue_state
issue: 150
task: .codex/pm/tasks/codex-runtime-research/fix-research-archive-known-files.md
title: Fix relative known_files sanitization in research archive output
status: done
---

## Summary

Fix the research archive sanitization bug that misattributes relative `known_files` paths to the wrong repository during HarnessHub archival.

## Validated Facts

- The archive script currently resolves relative `known_files` paths against the current working directory.
- This produced incorrect OpenPrecedent-flavored sanitized paths in `research-artifacts/harnesshub/2026-03-12T072058Z/`.
- The fix should keep relative paths anchored to the provided target repo root.

## Open Questions

- Should relative paths fall back to the only provided repo root even when the file does not exist on disk?

## Next Steps

- open PR for review

## Artifacts

- `scripts/archive_research_artifacts.py`
- `tests/test_research_archive_script.py`
- `/tmp/openprecedent-issue-150-archive-check/harnesshub/2026-03-12T072557Z/runtime-invocations-sanitized.jsonl`
