---
type: task
epic: real-history-quality
slug: refresh-mvp-roadmap
title: Refresh MVP roadmap after closing current implementation issues
status: done
labels: feature,docs
issue: 52
---

## Context

The MVP roadmap still lists several real-session quality items as open even though the corresponding implementation issues have now been merged.
That leaves the roadmap out of sync with the actual repository state and makes it harder to tell whether MVP v1 is complete.

## Deliverable

Refresh the MVP roadmap so it accurately reflects the completed MVP v1 scope and separates post-MVP next steps from the now-closed MVP issue set.

## Scope

- update the current-status summary to reflect that MVP v1 is complete as of 2026-03-10
- add the recently completed real-session quality work to the completed sections
- remove stale "still open" or "next tasks" bullets that refer to already-closed issues
- add a concise post-MVP direction section that points to the next stage without pretending it is still required for MVP v1

## Acceptance Criteria

- roadmap status matches the merged implementation state on `upstream/main`
- readers can distinguish completed MVP v1 work from post-MVP follow-up work
- the document remains concise and auditable

## Validation

- review the updated roadmap against the most recent merged issue set on `upstream/main`

## Implementation Notes

Keep the edit documentation-only and avoid inventing a large new planning framework inside the roadmap.
