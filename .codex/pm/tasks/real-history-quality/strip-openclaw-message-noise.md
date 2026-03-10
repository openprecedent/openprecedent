---
type: task
epic: real-history-quality
slug: strip-openclaw-message-noise
title: Strip operator policy and transport metadata from imported OpenClaw session messages
status: in_progress
labels: bug,feature
issue: 47
---

## Context

The validated live OpenClaw collector now imports real sessions from the target environment. Those sessions sometimes wrap visible user or assistant text with operator-policy and transport-metadata boilerplate that should not become replay events or decision evidence.

## Deliverable

Strip operator-policy and transport-metadata noise from imported OpenClaw session messages while preserving the user-visible task content that should drive replay and decision extraction.

## Scope

- sanitize imported OpenClaw session message text before it is stored as replayable message events
- drop message bodies that contain only operator-policy or transport-metadata wrapper text
- preserve visible task text when wrappers and real message content are mixed
- add regression fixtures and tests that prove noisy wrappers no longer create false-positive decisions

## Acceptance Criteria

- imported replay messages do not include operator-policy or transport-metadata boilerplate
- metadata-only wrapper messages are skipped during import
- mixed wrapper plus visible-content messages still preserve the visible content
- regression coverage proves noisy wrapper messages do not create false `clarify` decisions

## Validation

- run targeted API and CLI regression coverage for OpenClaw session import and decision extraction

## Implementation Notes

This issue should improve message quality without widening transcript modeling beyond the currently supported record types.
