---
type: task
epic: real-history-quality
slug: document-openprecedent-usage
title: Document how to use OpenPrecedent for humans and agents
status: done
labels: feature,docs
issue: 59
---

## Context

The repository explains what OpenPrecedent is, but it still lacks a practical usage guide for how the current MVP should be used day to day.
That guide needs to serve two different readers: a human operator running the current CLI and an agent developer deciding how to integrate OpenPrecedent into a local workflow.

## Deliverable

Add a usage document that explains the shipped MVP operating model for both humans and agents, then link it from the README.

## Scope

- add a new usage doc under `docs/engineering/`
- explain the current human workflow with concrete CLI examples
- explain the current agent integration patterns and their boundaries
- add a README link to the new usage doc

## Acceptance Criteria

- a human can understand how to run the current MVP end to end
- an agent developer can understand the supported integration patterns today
- the README links directly to the usage doc

## Validation

- review the guide against the current CLI surface, service layer, and OpenClaw collection path
- confirm the README link points to the new document

## Implementation Notes

Keep the guide grounded in the current implementation instead of describing a future hosted product.
