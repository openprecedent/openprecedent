---
type: task
epic: real-history-quality
slug: reduce-false-clarify-decisions
title: Reduce false clarify decisions on wrapped OpenClaw multi-turn sessions
status: done
labels: bug,test
issue: 45
---

## Context

Live OpenClaw collection exposes wrapped multi-turn sessions where a later user message can restate the same request instead of refining scope. The current extractor treats any later user message as a `clarify` decision, which overstates decision count and degrades replay quality.

## Deliverable

Reduce false `clarify` decisions on wrapped OpenClaw multi-turn sessions while preserving true clarification extraction when the user materially narrows or changes the task.

## Scope

- tighten clarify extraction so repeated or near-duplicate follow-up user messages do not produce a `clarify` decision
- preserve existing true-positive clarify behavior for real follow-up scope changes
- add a wrapped-session regression fixture and API/CLI coverage for the false-positive case

## Acceptance Criteria

- wrapped multi-turn sessions that repeat the same user intent no longer emit a `clarify` decision
- existing real clarify fixtures still emit the expected `clarify` decision
- regression coverage locks both the false-positive and true-positive cases

## Validation

- run targeted API and CLI regression coverage for clarify extraction

## Implementation Notes

Prefer a small, auditable heuristic tied to user-intent similarity rather than a broad decision-extraction rewrite.
