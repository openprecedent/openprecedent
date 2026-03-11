# Codex Precedent Retrieval Validation

## Goal

Record a durable validation artifact for issue `#129`:

- whether precedent retrieval over Codex-derived development history is semantically useful
- whether the current behavior is better explained by shared judgment lineage than by superficial operational overlap

## Validation Method

This validation uses three Codex rollout-derived cases imported through the current Codex runtime path:

1. a current case asking for a docs-only recommendation inside a constrained Codex runtime scope
2. a semantically related prior case with the same docs-only recommendation shape, constraint pattern, and approval pattern
3. an operationally similar but semantically different prior case that also reads the same Codex runtime document, but does so for architecture-summary work rather than constrained recommendation work

The validation then runs precedent lookup on the current case and reviews which prior case ranks first.

## Representative Cases

Fixtures:

- [codex_rollout_precedent_current.jsonl](/workspace/02-projects/incubation/openprecedent/tests/fixtures/codex_rollout_precedent_current.jsonl)
- [codex_rollout_precedent_semantic_match.jsonl](/workspace/02-projects/incubation/openprecedent/tests/fixtures/codex_rollout_precedent_semantic_match.jsonl)
- [codex_rollout_precedent_operational_overlap.jsonl](/workspace/02-projects/incubation/openprecedent/tests/fixtures/codex_rollout_precedent_operational_overlap.jsonl)

## Finding

Current precedent retrieval prefers the semantically related Codex case over the merely operationally similar one.

In this validation, the stronger match is driven by shared semantic lineage:

- docs-only constraint
- recommendation-oriented success framing
- explicit approval / authority language

The weaker match shares a document read and command shape, but not the same task framing or decision semantics.

That is the behavior OpenPrecedent should prefer at this phase.

## Interpretation

This is a positive signal for Codex as a research runtime.

It suggests the current system can already do something more useful than “same tool, same file, same command” matching.
It can retrieve prior Codex cases that share meaningful judgment structure.

## Current Boundary

This validation is still project-local.

It does not yet prove:

- cross-project portability
- usefulness on larger and messier Codex history
- usefulness when multiple semantically related precedents compete at once

It does prove a narrower but important point:

- Codex-derived precedent retrieval is already capable of preferring semantic lineage over operational overlap on representative development cases

## Why This Matters For The Next Step

This result is enough to justify the next Codex research issue:

- `#130` Codex-facing minimal runtime workflow

That next issue should treat the current result as a local retrieval-quality baseline, not as proof of broader portability.
