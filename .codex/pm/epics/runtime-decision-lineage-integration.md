---
type: epic
slug: runtime-decision-lineage-integration
title: Runtime decision-lineage integration
status: backlog
prd: decision-lineage-refocus
---

## Outcome

Expose OpenPrecedent as a runtime decision-lineage capability that OpenClaw can call safely, then validate where and whether that capability improves downstream task judgment.

## Scope

- encapsulate OpenPrecedent retrieval behind a dedicated OpenClaw-facing skill or service surface
- define a runtime `decision lineage brief` output instead of operational recommendations
- evaluate trigger timing and practical benefit inside OpenClaw task execution

## Acceptance Criteria

- the epic contains one task for runtime skill encapsulation
- the epic contains one task for trigger-policy and effect validation
- runtime integration work depends on the semantic decision foundation rather than the old operational taxonomy

## Child Issues

- `#72` Encapsulate OpenPrecedent as an OpenClaw decision-lineage skill
- `#73` Validate OpenClaw runtime triggers and impact for decision-lineage retrieval

## Notes

The first goal is not autonomous tool steering. The first goal is controlled reuse of semantic task framing, constraints, authority signals, and success criteria during later OpenClaw runs.
