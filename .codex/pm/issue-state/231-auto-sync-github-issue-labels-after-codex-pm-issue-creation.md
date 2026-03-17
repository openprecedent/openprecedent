---
type: issue_state
issue: 231
task: .codex/pm/tasks/real-history-quality/auto-sync-github-issue-labels-after-codex-pm-issue-creation.md
title: Automatically synchronize GitHub issue labels after Codex PM issue creation
status: pr_opened
---

## Summary

Implement a guarded GitHub issue-creation path for Codex PM so task-twin labels are applied automatically and newly created issues do not reintroduce unlabeled drift.

## Validated Facts

- The repository now has durable `research` and `harness` labels plus a full historical label backfill from `#229`.
- The current gap is at creation time: issue labels can still be skipped because issue creation happens through raw `gh issue create`.
- A new `codex_pm issue-create` command has been implemented in this branch and covered with regression tests for labeled and unlabeled task twins.
- CCPM skill docs have been updated to route issue creation through the guarded command.
- PR `#232` has been opened to land the guardrail.

## Open Questions

- None at the implementation level; remaining work is PR review and merge.

## Next Steps

- monitor PR `#232`
- address any CI or review feedback
- merge the PR to close `#231`

## Artifacts

- `src/openprecedent/codex_pm.py`
- `tests/test_codex_pm.py`
- `.codex/skills/ccpm-codex/SKILL.md`
- `.codex/skills/ccpm-codex/references/command-map.md`
- GitHub PR `#232`
