---
type: task
epic: runtime-decision-lineage-integration
slug: encapsulate-openclaw-decision-lineage-skill
title: Encapsulate OpenPrecedent as an OpenClaw decision-lineage skill
status: backlog
labels: feature,docs
depends_on: 71
issue: 72
---

## Context

Once OpenPrecedent captures semantic decision lineage, it needs a clean runtime-facing integration surface for OpenClaw.
That surface should expose retrieval as a reusable capability without directly prescribing operational actions.

## Deliverable

Encapsulate OpenPrecedent as an OpenClaw-facing runtime skill or service that returns a semantic `decision lineage brief`.

## Scope

- define the runtime input schema for querying semantic decision lineage from the current task context
- define the `decision lineage brief` output shape centered on task framing, constraints, authority signals, success criteria, and rejected options
- implement the retrieval or service layer needed to produce that brief from OpenPrecedent data
- keep the skill focused on retrieval and briefing, not trigger timing or autonomous action steering

## Acceptance Criteria

- OpenClaw has a dedicated capability surface for retrieving decision-lineage briefs from OpenPrecedent
- the brief format does not prescribe tools, commands, or file writes
- the returned information is centered on reusable judgment context rather than operational history
- documentation explains the intended boundary of the skill clearly

## Validation

- verify the skill can be called with representative task context and returns a valid semantic brief
- review the output format to confirm it carries judgment context rather than operational recommendations

## Implementation Notes

This task should start only after the semantic decision foundation is stable enough to supply meaningful retrieval results.
