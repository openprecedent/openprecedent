---
type: task
epic: real-history-quality
slug: refresh-mvp-status-docs
title: Refresh MVP status and architecture docs after core loop completion
status: done
labels: docs
issue: 96
---

## Context

The roadmap already states that MVP v1 is complete, but the surrounding product and architecture docs still present a partially in-flight picture.
Some current docs describe the shipped system accurately, while older Chinese MVP drafts still read like the active plan and the English PRD does not explicitly mark the core loop as complete.

## Deliverable

A documentation-only refresh that makes the repository's MVP status consistent across roadmap, PRD, architecture, and a new summary note.

## Scope

- refresh the English MVP PRD so it reflects the shipped MVP v1 state instead of only the original target state
- add a concise MVP status note that summarizes the completed core loop and separates post-MVP work from MVP-blocking scope
- update the English and Chinese MVP architecture docs where the shipped runtime integration picture has changed
- mark stale Chinese Context Graph MVP drafts as historical/superseded so they are not mistaken for the current shipped plan

## Acceptance Criteria

- a reader can tell from the repo docs that the MVP core loop is fully implemented and validated
- architecture and product docs consistently frame remaining work as post-MVP validation and quality iteration
- older draft docs are clearly labeled so they do not conflict with the current OpenPrecedent MVP narrative

## Validation

- read the refreshed docs together and confirm they present one consistent MVP-complete story
- confirm that no updated doc implies that core-loop engineering is still blocked or incomplete

## Implementation Notes

- Keep the change documentation-only.
- Prefer explicit status language over broad rewrites.
- Added `docs/product/mvp-status.md` as the repository-level summary of MVP completion and post-MVP boundaries.
- Refreshed the English PRD, roadmap, and English/Chinese MVP architecture docs to reflect the shipped MVP v1 state.
- Marked the older Chinese Context Graph MVP PRD and design docs as historical drafts so they do not compete with the current OpenPrecedent MVP narrative.
