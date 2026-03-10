---
type: epic
slug: semantic-decision-foundation
title: Semantic decision foundation
status: backlog
prd: decision-lineage-refocus
---

## Outcome

Replace the current operationally biased decision layer with a semantic decision-lineage foundation that captures high-value judgments, evaluates them reliably, and prepares precedent retrieval to use those signals.

## Scope

- document the product principles and first semantic decision taxonomy
- refactor schema and extraction away from operational decisions
- rebuild fixtures and tests around semantic decision expectations
- retune precedent retrieval toward semantic judgment similarity

## Acceptance Criteria

- the epic contains one task for taxonomy and product-principle definition
- the epic contains one task for schema and extraction refactoring
- the epic contains one task for evaluation-fixture and test-baseline migration
- the epic contains one task for precedent ranking migration

## Child Issues

- `#68` Define semantic decision taxonomy and product principles
- `#69` Refactor decision schema and extraction around semantic decision lineage
- `#70` Rebuild evaluation fixtures and tests for semantic decision lineage
- `#71` Retune precedent ranking toward semantic decision similarity

## Notes

This epic intentionally stops short of runtime invocation inside OpenClaw. It establishes the semantic substrate that runtime integration will depend on.
