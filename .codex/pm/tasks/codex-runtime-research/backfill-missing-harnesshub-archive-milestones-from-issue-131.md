---
type: task
epic: codex-runtime-research
slug: backfill-missing-harnesshub-archive-milestones-from-issue-131
title: Backfill missing HarnessHub archive milestones from issue 131
status: done
task_type: research
labels: docs
issue: 216
state_path: .codex/pm/issue-state/216-backfill-missing-harnesshub-archive-milestones-from-issue-131.md
---

## Context

Issue `#131` was closed with the first-phase HarnessHub validation archive, but two sanitized archive milestones that support the final narrative remained only as untracked local research artifacts.

The repository should preserve:

- `research-artifacts/harnesshub/2026-03-12T092548Z/` as the last empty-match milestone before live reuse succeeded
- `research-artifacts/harnesshub/2026-03-12T164942Z/` as the strongest missing archive for the first non-empty live `matched_case_ids` result

Issue `#216` should not reopen the first-phase study itself.
It should only backfill the missing git-safe artifacts and make the duplicate-exclusion reasoning explicit.

## Deliverable

Add the missing tracked archive milestones for `2026-03-12T092548Z` and `2026-03-12T164942Z`, and update the first-phase archive documentation so future readers can see where those milestones fit in the evidence trail.

## Scope

- add the two sanitized archive directories to version control
- document why `2026-03-12T165042Z` is not added because it duplicates `2026-03-12T164942Z`
- keep the archival framing attached to issue `#131` rather than reopening the closed study

## Acceptance Criteria

- both missing milestone directories are tracked in the repository
- the validation archive explains why those milestones matter and why the duplicate snapshot is excluded
- local task and issue-state metadata for issue `#216` are present and aligned

## Validation

- verify the backfilled archive directories contain the expected sanitized files and counts
- verify `2026-03-12T165042Z` remains excluded because its sanitized invocation payload duplicates `2026-03-12T164942Z`
- run repository preflight after the archive and documentation updates
