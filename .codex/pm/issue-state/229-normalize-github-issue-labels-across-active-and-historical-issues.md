---
type: issue_state
issue: 229
task: .codex/pm/tasks/real-history-quality/normalize-github-issue-labels-across-active-and-historical-issues.md
title: Normalize labels across active and historical GitHub issues
status: in_progress
---

## Summary

GitHub issue label coverage has been normalized across active and historical issues. The repository now has durable `research` and `harness` labels, and the historical unlabeled-issue backlog has been reduced to zero.

## Validated Facts

- `research` and `harness` labels were created to cover recurring repository work that did not fit the preexisting label set.
- Active and closed issues were backfilled with appropriate labels using `gh issue edit --add-label`.
- `gh issue list --state all --limit 200 --json number,labels | jq '[.[] | select((.labels|length)==0)] | length'` now returns `0`.
- The remaining work on this issue is repository-local closure: commit the PM twins, run preflight, and open the issue PR.

## Open Questions

- None for the label backfill itself.

## Next Steps

- commit the local PM records for `#229`
- run `./scripts/run-agent-preflight.sh`
- open the PR that closes `#229`

## Artifacts

- GitHub issue `#229`
- GitHub labels `research` and `harness`
- `.codex/pm/tasks/real-history-quality/normalize-github-issue-labels-across-active-and-historical-issues.md`
- `.codex/pm/issue-state/229-normalize-github-issue-labels-across-active-and-historical-issues.md`
