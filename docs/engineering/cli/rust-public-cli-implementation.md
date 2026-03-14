# Rust Public CLI Implementation

## Purpose

This document describes the Rust CLI that is now actually shipped on `main`.

It is the implementation companion to:

- [rust-public-cli-design.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/rust-public-cli-design.md)

The design document defines the long-term public contract.
This document explains what was implemented, how the code is organized today, what was cut over from the earlier Python and shell entrypoints, and what remains intentionally internal.

## Outcome

The repository now exposes Rust `openprecedent` as the stable public executable surface.

That cutover includes:

- Rust-native command parsing and output rendering
- Rust-native config and path resolution
- Rust-native SQLite access and schema initialization
- Rust-native implementations of case, event, decision, replay, precedent, capture, lineage, and eval commands
- skill and validation workflow migration to direct Rust CLI invocation
- removal of the public Python `openprecedent` console script and the retired Python CLI module that backed it
- removal of repository-local shell wrappers as the supported public interface

The Python codebase remains in the repository for internal service logic, PM tooling, and repository-local harness scripts, but the retired Python public CLI implementation itself has been removed and no longer competes with the supported Rust contract.

## Implemented Command Surface

The shipped Rust CLI command tree is:

```text
openprecedent case
openprecedent event
openprecedent decision
openprecedent replay
openprecedent precedent
openprecedent capture
openprecedent lineage
openprecedent eval
openprecedent doctor
openprecedent version
```

The implemented command families are:

- `case create|list|show`
- `event append|import-jsonl`
- `decision extract|list`
- `replay case`
- `precedent find`
- `capture openclaw list-sessions|import-session|collect-sessions|import-jsonl`
- `capture codex import-rollout`
- `lineage brief`
- `lineage invocation list|inspect`
- `eval fixtures|captured-openclaw-sessions`
- `doctor paths|storage|environment`
- `version`

Global flags implemented across the public surface include:

- `--format`
- `--home`
- `--db`
- `--invocation-log`
- `--state-file`
- `--config`
- `--no-color`

These are resolved through the documented precedence order of CLI flag, environment variable, config file, and default.

## Workspace Layout

The Rust implementation is organized as a workspace rooted at:

- [Cargo.toml](/workspace/02-projects/incubation/openprecedent/Cargo.toml)

The crates are:

- `rust/openprecedent-cli`
  The public binary crate. It owns command parsing, public command topology, text and JSON rendering, and CLI-level error handling.
- `rust/openprecedent-contracts`
  Shared public data shapes used by the CLI, including cases, events, decisions, replay responses, precedent matches, lineage payloads, evaluation reports, and doctor responses.
- `rust/openprecedent-core`
  Runtime configuration resolution and higher-level shared CLI logic.
- `rust/openprecedent-store-sqlite`
  SQLite-backed persistence, schema initialization, schema compatibility handling, and record round-tripping.
- `rust/openprecedent-capture-openclaw`
  OpenClaw-specific transcript discovery, list, import, and collection logic.
- `rust/openprecedent-capture-codex`
  Codex rollout import logic.

This layout keeps the command surface, shared contracts, persistence layer, and runtime-specific capture logic separate without turning the public CLI into a thin wrapper over the Python implementation.

## Data and Compatibility Model

The Rust CLI was implemented against the existing local-first runtime layout rather than introducing a second storage system.

The current behavior is:

- runtime home still defaults to `~/.openprecedent/runtime`
- SQLite remains the persistent store
- invocation logs remain file-backed and compatible with lineage inspection
- schema initialization and compatibility upgrades are handled in Rust
- earlier persisted runtime data remains readable after the cutover

That compatibility layer lives primarily in:

- [lib.rs](/workspace/02-projects/incubation/openprecedent/rust/openprecedent-store-sqlite/src/lib.rs)

The implementation preserves the MVP data model of:

- raw cases
- raw events
- derived decisions
- replay artifacts
- precedent retrieval over stored case history

## Public Contract Implementation

The Rust CLI directly implements the public contract instead of delegating command execution to the old Python CLI.

Key contract choices now enforced in code are:

- `openprecedent` is the stable binary name
- JSON output is the machine-facing contract
- human-readable text output remains available for local use
- `capture` is the stable namespace for runtime-specific ingest
- `lineage` is the stable namespace for decision-lineage retrieval and inspection
- `doctor` is the stable availability and environment diagnosis surface for skills and automation

The main public command tree and argument parsing live in:

- [main.rs](/workspace/02-projects/incubation/openprecedent/rust/openprecedent-cli/src/main.rs)

## Capture and Lineage Surfaces

Two product-facing areas were especially important in this migration.

### Capture

The Rust CLI now owns the supported capture surfaces for:

- OpenClaw transcript listing and import
- OpenClaw collected-session ingestion
- Codex rollout import

This replaced public reliance on older repository-local wrappers and gave capture flows a stable command identity under `openprecedent capture ...`.

### Lineage

The Rust CLI now owns:

- `openprecedent lineage brief`
- `openprecedent lineage invocation list`
- `openprecedent lineage invocation inspect`

These commands are the intended machine-facing surface for skill-driven precedent retrieval and runtime invocation inspection.

## Skill and Workflow Cutover

The migration was not complete until the repository's own runtime-facing skills and validation workflows stopped depending on the earlier script-shaped public interface.

After the cutover:

- skills are expected to call the Rust CLI directly
- availability probing should use `openprecedent doctor ...`
- lineage retrieval should use `openprecedent lineage ... --format json`
- validation harnesses and remaining helper scripts resolve or build the Rust binary, then call it directly

To support repo-local tooling and tests without reintroducing the old public shell interface, the repository now includes internal Rust-binary resolution helpers:

- [openprecedent-rust-cli.sh](/workspace/02-projects/incubation/openprecedent/scripts/lib/openprecedent-rust-cli.sh)
- [openprecedent_rust_cli.py](/workspace/02-projects/incubation/openprecedent/scripts/lib/openprecedent_rust_cli.py)

These helpers are internal developer tooling.
They are not the public product interface.

## What Was Removed from the Public Surface

The cutover intentionally removed two earlier public surfaces.

### Python public CLI

The packaged Python `openprecedent` console script is no longer exposed as the product-facing command entrypoint, and the retired Python CLI module that previously implemented that surface has been removed from `src/openprecedent/cli.py`.

Python still remains in the repository for internal service logic and PM tooling, but the supported public executable interface is now Rust `openprecedent`.

### Public shell-script entrypoints

Repository-local shell scripts are no longer treated as the supported product-facing command surface.

Some scripts remain in `scripts/` for repository-local operations, validation, installation, and development harnessing, but they are internal helpers around the CLI rather than the CLI itself.

## Verification and Regression Coverage

The implementation was validated through a mix of Rust contract tests, Python regression tests, and repository preflight checks.

The important verification layers are:

- Rust CLI contract tests under [rust/openprecedent-cli/tests](/workspace/02-projects/incubation/openprecedent/rust/openprecedent-cli/tests)
- repository Python regressions covering wrappers, harnesses, imports, and workspace assumptions under [tests](/workspace/02-projects/incubation/openprecedent/tests)
- repository preflight and review gates under [run-agent-preflight.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-agent-preflight.sh)

The migration train was validated with:

- `cargo test`
- targeted Python regression runs for Rust CLI integration surfaces
- full agent preflight before final merge-back

## Migration Scope Covered by the Train

The Rust CLI migration was delivered through issue `#172` and child issues `#174` through `#187`.

That train covered:

- workspace bootstrap
- config, doctor, and version contracts
- SQLite store and schema compatibility
- case commands
- event commands
- decision commands
- replay and precedent commands
- OpenClaw capture
- Codex capture
- lineage brief
- lineage invocation inspection
- eval commands
- skill and validation workflow migration
- public cutover away from Python CLI and public shell entrypoints

## What Remains Internal

The following remain intentionally internal or repository-local:

- `openprecedent-pm` and Codex PM workflow tooling
- repository maintenance scripts
- Python modules used for repo-local harnessing and support logic
- historical research artifacts and older command examples kept only as evidence context

These are not part of the supported public CLI contract.

## Practical Reading Order

If you are trying to understand the system now, use this order:

1. [using-openprecedent.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/using-openprecedent.md)
2. this implementation document
3. [rust-public-cli-design.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/rust-public-cli-design.md)

That sequence moves from current usage, to actual implementation, to long-term contract intent.
