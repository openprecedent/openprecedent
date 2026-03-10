---
type: task
epic: real-history-quality
slug: model-additional-openclaw-record-types
title: Model additional real-session OpenClaw record types from live collection
status: done
labels: feature,test
issue: 46
---

## Context

The first validated live OpenClaw collector run surfaced two previously unsupported session record types: `custom` and `thinking_level_change`.
Those records should not be treated as user-visible chat messages, but they can still carry replay or explanation signal that should be preserved when importing real sessions.

## Deliverable

Extend OpenClaw session import so useful `custom` and `thinking_level_change` records are normalized into the existing event model instead of being reported as unsupported.

## Scope

- map `thinking_level_change` into a non-chat event that preserves the new level and change source
- map `custom` records only when they expose replayable signal such as a named action or text/details payload
- keep unsupported-record reporting for session record types that still cannot be normalized safely
- add targeted fixture, API coverage, and CLI coverage for the new record types

## Acceptance Criteria

- importing a session fixture with `custom` and `thinking_level_change` records yields replayable events for both record types
- those records no longer appear in `unsupported_record_type_counts`
- the new mapping does not create false user-message or clarify decisions

## Validation

- run targeted API and CLI tests covering OpenClaw session import and replay for the new record types

## Implementation Notes

Prefer a conservative mapping into existing event types over introducing new schema objects just for OpenClaw-specific transcript variants.
