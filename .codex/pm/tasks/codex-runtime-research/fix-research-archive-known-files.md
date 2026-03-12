---
type: task
epic: codex-runtime-research
slug: fix-research-archive-known-files
title: Fix relative known_files sanitization in research archive output
status: done
task_type: implementation
labels: bug,test
issue: 150
state_path: .codex/pm/issue-state/150-fix-research-archive-known-files.md
---

## Context

Recent HarnessHub research archives exposed a bug in `scripts/archive_research_artifacts.py`.
When runtime invocations store `known_files` as repository-relative paths, the sanitizer resolves them against the current working directory and can misattribute them to the OpenPrecedent repository instead of the target study repository.

## Deliverable

Fix the archive sanitization flow so relative `known_files` values remain associated with the intended external repository root, then add regression coverage for the HarnessHub case.

## Scope

- update `scripts/archive_research_artifacts.py`
- add regression tests for relative and target-repo path handling
- verify archive output for a HarnessHub-style invocation sample

## Acceptance Criteria

- relative `known_files` entries sanitize to the provided target repo root instead of the caller's current working directory
- tests cover the relative-path regression
- a local archive run preserves `HarnessHub/...` output for relative invocation paths

## Validation

- run targeted pytest coverage for the archive script
- run one archive command against a HarnessHub-style runtime fixture and inspect the generated JSONL

Validation completed:

- `../openprecedent/.venv/bin/pytest -q tests/test_research_archive_script.py`
- `python3 scripts/archive_research_artifacts.py --study harnesshub --query HarnessHub --repo-root /workspace/02-projects/active/HarnessHub --runtime-home /root/.openprecedent/runtime --output-root /tmp/openprecedent-issue-150-archive-check`

## Implementation Notes

- This bug was first observed in `research-artifacts/harnesshub/2026-03-12T072058Z/`.
