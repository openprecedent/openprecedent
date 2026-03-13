---
type: epic
slug: public-cli-foundation
title: Public CLI foundation
status: backlog
prd: public-interface-evolution
---

## Outcome

Establish a Rust-based `openprecedent` CLI as the sole stable public interface for OpenPrecedent, replacing public Python CLI exposure and repository-local shell-script command surfaces.

## Scope

- contract-first public CLI design
- Rust workspace and public command skeleton
- configuration, path resolution, versioning, and diagnostics contracts
- migration of core case, event, decision, replay, precedent, capture, lineage, and eval surfaces into Rust-native implementation
- direct skill integration through CLI rather than shell wrappers
- public cutover and removal of Python CLI and public shell wrappers

## Acceptance Criteria

- the epic contains a dedicated task for system design of the Rust public CLI contract
- the epic is explicitly scoped as public interface evolution, not as a research-only runtime adapter effort
- the implementation chain ends with public cutover to Rust CLI as the only supported external command surface

## Child Issues

- `#172` Design and adopt a Rust CLI as the stable public interface for OpenPrecedent

## Notes

This epic is about the product-facing command surface, not about preserving the current MVP implementation topology.
The CLI should be treated as a long-term external contract that survives internal language and architecture evolution.
