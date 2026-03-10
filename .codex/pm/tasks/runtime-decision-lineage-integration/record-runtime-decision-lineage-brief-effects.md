---
type: task
epic: runtime-decision-lineage-integration
slug: record-runtime-decision-lineage-brief-effects
title: Record decision-lineage brief outputs and downstream effects
status: completed
labels: feature,observability,docs
depends_on: 72
issue: 82
---

## Context

Even if OpenPrecedent records that a skill lookup happened, real validation still needs visibility into what semantic brief was returned and how that brief related to later task judgment.
At the moment, this relationship is not captured as structured evidence.

## Deliverable

Add a minimal mechanism for inspecting the semantic content returned by the runtime decision-lineage brief and relating it to subsequent agent decisions or messages.

## Scope

- record the returned semantic brief in an inspectable way, at least as a structured summary
- preserve the key runtime brief fields needed for later validation, such as matched cases, task frame, constraints, success criteria, rejected options, and authority signals
- expose enough linkage in replay or documentation-oriented output to compare the returned brief with subsequent semantic decisions
- avoid turning this into a full causal inference system

## Acceptance Criteria

- a reviewer can inspect what semantic brief was returned during runtime use
- the repository provides enough evidence to compare the brief with later task framing or constraint handling
- the output is stable enough to support later validation documentation

## Validation

- execute at least one runtime lookup and verify that both the returned brief summary and the subsequent relevant task signals can be inspected together

## Implementation Notes

This task should stay focused on observability of returned semantic context and its nearby downstream effects.
