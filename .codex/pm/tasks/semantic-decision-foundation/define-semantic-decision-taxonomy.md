---
type: task
epic: semantic-decision-foundation
slug: define-semantic-decision-taxonomy
title: Define semantic decision taxonomy and product principles
status: done
labels: feature,docs
issue: 68
---

## Context

OpenPrecedent needs a hard product-level correction: `decision` must capture semantic, high-value judgment lineage from human-agent collaboration rather than execution-layer operations.
The current MVP drifted toward operational outputs such as tool selection and file writes, but those should remain event evidence instead of precedent-worthy decisions.
This task defines the normative contract for the rest of the refactor.

## Deliverable

Publish the decision-lineage product principles and the first semantic decision taxonomy in the repository documentation and architecture guidance.

## Scope

- define the principle that `event` records process evidence while `decision` records reusable judgment
- explicitly ban tool choice, file writes, retries, command execution, and similar operational moves from the decision taxonomy
- define the first semantic decision taxonomy for high-value latent decisions
- document how decisions relate to evidence events, replay, and precedents
- codify the workflow rule that implementation work must be tied to a concrete issue and dedicated branch
- update the core architecture and usage documentation as needed to reflect the new direction

## Acceptance Criteria

- repository guidance and decision-oriented docs clearly exclude operational actions from the decision taxonomy
- the first semantic taxonomy is documented with stable names and intended semantics
- the docs explain that future runtime reuse should inherit judgment lineage rather than operational behavior
- the workflow guidance explicitly states that implementation work must be tied to a concrete issue and dedicated branch

## Validation

- review the updated docs to confirm the taxonomy, boundary, and workflow rule are all stated unambiguously
- confirm the written taxonomy can serve as the direct dependency for schema and extraction work

## Implementation Notes

This task defines the contract. It should land before schema, extraction, evaluation, or runtime integration work.
