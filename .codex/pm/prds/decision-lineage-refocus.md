---
type: prd
slug: decision-lineage-refocus
title: Refocus OpenPrecedent on semantic decision lineage
status: draft
---

## Summary

Refocus OpenPrecedent so `decision` records capture semantic, high-value judgment lineage from human-agent collaboration rather than execution-layer operations.

## Problem

The current MVP proved that OpenPrecedent can capture sessions, derive decisions, replay them, and retrieve precedents, but the decision model drifted toward execution choices such as tool selection and file writes.
Those operational actions are context-sensitive process steps that should remain evidence in the event timeline, not first-class decision assets that future agents inherit.
If the product continues to treat operational moves as precedent-worthy decisions, runtime reuse will push agents toward imitating old mechanics instead of inheriting task framing, constraints, authority signals, and success criteria.

## Goals

- redefine `decision` around semantic decision lineage rather than operational behavior
- establish a durable taxonomy for high-value latent decisions from human-agent collaboration
- rebuild extraction, evaluation, and precedent logic around that semantic taxonomy
- prepare a clean runtime integration surface for OpenClaw that returns decision-lineage briefs instead of operational recommendations

## Non-Goals

- preserving the current operational decision taxonomy for backward compatibility
- teaching OpenPrecedent to prescribe tools, commands, or file writes directly
- turning the product into a generic memory store or trace viewer
- implementing full OpenClaw runtime policy in the same step as taxonomy and schema refactoring

## Success Criteria

- repository guidance clearly states that implementation changes must be issue-bound and that discussion-phase exploration must not mutate implementation code speculatively
- the semantic decision taxonomy is documented and excludes operational choices such as tool selection, file writes, retries, and command execution
- extraction and evaluation can distinguish high-value semantic decisions from raw process activity
- precedent retrieval can evolve toward semantic decision similarity instead of operational pattern similarity
- runtime integration work has a clear boundary between skill encapsulation and trigger-policy validation

## Dependencies

- the existing MVP event and replay foundation on `upstream/main`
- OpenClaw validation findings already documented in the repository
- repository-local Codex PM workflow under `.codex/pm/`
