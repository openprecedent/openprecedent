---
type: task
epic: codex-runtime-research
slug: define-codex-runtime-boundary
title: Define the Codex runtime integration boundary for research-only minimal support
status: in_progress
labels: feature,docs
issue: 125
---

## Context

Codex is now the strongest available source of dense, continuous development history for the next research phase.
Before any Codex implementation starts, the repository needs one durable statement of what Codex support is for and what remains out of scope.

## Deliverable

Document the exact Codex integration boundary as a research-only second runtime for OpenPrecedent.

## Scope

- define what Codex minimal integration must support for research
- define the capture surfaces needed from Codex history
- define mapping principles into `case`, `event`, `decision`, `artifact`, and `precedent`
- define explicit non-goals, especially avoiding generic multi-runtime abstraction work
- record how this path is intended to support issue `#100` exit criteria

## Acceptance Criteria

- the repository has one clear Codex runtime boundary artifact
- the artifact is explicitly framed as research support rather than platform expansion
- the required capture surfaces and non-goals are concrete enough to guide the follow-on Codex issues

## Validation

- review the resulting artifact and confirm later Codex issues can derive directly from it without reopening the boundary question
