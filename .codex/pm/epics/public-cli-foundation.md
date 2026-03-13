---
type: epic
slug: public-cli-foundation
title: Public CLI foundation
status: done
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
- `#174` Bootstrap the Rust workspace and openprecedent binary skeleton
- `#175` Implement global config, path resolution, doctor, and version contracts in the Rust CLI
- `#176` Implement the Rust SQLite store and schema compatibility layer for the public CLI
- `#177` Migrate case commands to the Rust CLI
- `#178` Migrate event commands to the Rust CLI
- `#179` Migrate decision commands to the Rust CLI
- `#180` Migrate replay and precedent commands to the Rust CLI
- `#181` Migrate OpenClaw capture commands to the Rust CLI
- `#182` Migrate Codex capture commands to the Rust CLI
- `#183` Migrate the lineage brief command to the Rust CLI
- `#184` Migrate lineage invocation inspection commands to the Rust CLI
- `#185` Migrate eval commands to the Rust CLI
- `#186` Migrate skills and validation workflows from scripts to the Rust CLI
- `#187` Cut over to the Rust CLI and remove public Python and script entrypoints

## Notes

This epic is about the product-facing command surface, not about preserving the current MVP implementation topology.
The CLI should be treated as a long-term external contract that survives internal language and architecture evolution.
All child issue PRs under this epic should merge into `codex/issue-172-rust-public-cli` until the full migration train is integrated and ready for the final merge back to `main`.
That child issue chain is now fully integrated on `codex/issue-172-rust-public-cli`; the remaining closure step is the final merge of that special-purpose integration branch back to `main`.
