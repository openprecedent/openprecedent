---
type: task
epic: real-history-quality
slug: document-mvp-architecture
title: Document MVP architecture with diagrams and capability boundaries
status: in_progress
labels: feature,docs
issue: 54
---

## Context

The repository has roadmap and implementation docs, but it still lacks a single architecture document that shows the shipped MVP v1 system clearly.
Readers should be able to understand the exact MVP capability boundary without reading the full codebase or reconstructing it from issue history.

## Deliverable

Publish an MVP architecture document that explains the current shipped system, includes PlantUML diagrams, and makes MVP capability boundaries explicit.

## Scope

- expand the MVP architecture doc around the current implementation on `upstream/main`
- include PlantUML diagrams for system context and end-to-end flow
- include at least one additional diagram that clarifies core object relationships or capability boundaries
- document exact MVP interfaces, supported event and decision coverage, and non-goals

## Acceptance Criteria

- a reader can understand the accurate MVP v1 architecture from one document
- the document includes PlantUML diagrams plus at least one additional useful diagram
- the content stays aligned with the current merged implementation and roadmap

## Validation

- review the document against the current CLI, service layer, storage model, and MVP roadmap
- confirm that the capability boundary does not claim an unshipped API or platform layer

## Implementation Notes

Prefer an implementation-grounded architecture summary over a speculative future-state design.
