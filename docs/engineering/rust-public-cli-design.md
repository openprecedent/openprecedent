# Rust Public CLI Design

## Purpose

This document defines the long-term public command interface for OpenPrecedent.

For the shipped implementation summary, see:

- [rust-public-cli-implementation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/rust-public-cli-implementation.md)

The goal is not to port the current Python `argparse` tree one command at a time.
The goal is to establish a stable, extensible, product-facing `openprecedent` CLI implemented in Rust and treated as the sole supported external executable surface.

After cutover, the following are no longer supported as public interfaces:

- the current Python `openprecedent` CLI implementation
- repository-local shell scripts used as public command entrypoints
- skill integrations that depend on repository layout or shell-composition tricks instead of calling `openprecedent` directly

## Design Principles

The Rust CLI is designed under these rules:

1. `openprecedent` is the stable command identity.
2. JSON output is the machine contract.
3. Text output is for humans and may evolve without being the automation contract.
4. Public commands are organized around product domains, not around the current Python module layout or MVP plumbing.
5. Skills and automation call the CLI directly, never repository-local wrapper scripts.
6. Internal implementation language is allowed to evolve, but the public CLI contract must remain stable across that change.
7. Public cutover removes the Python CLI and public script entrypoints rather than leaving them as parallel long-term surfaces.

## Public Surface

The long-term public command tree is:

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

### `case`

Case lifecycle commands:

- `openprecedent case create`
- `openprecedent case list`
- `openprecedent case show`

### `event`

Explicit event-writing commands:

- `openprecedent event append`
- `openprecedent event import-jsonl`

### `decision`

Decision-oriented commands:

- `openprecedent decision extract`
- `openprecedent decision list`

This replaces the plural top-level noun used by the current Python CLI.
The public contract should align with the product's singular domain-object naming.

### `replay`

Replay and explanation commands:

- `openprecedent replay case`

### `precedent`

Precedent lookup commands:

- `openprecedent precedent find`

### `capture`

Runtime-specific ingest commands belong under `capture`, not under a generic `runtime` bucket.

- `openprecedent capture openclaw list-sessions`
- `openprecedent capture openclaw import-session`
- `openprecedent capture openclaw collect-sessions`
- `openprecedent capture openclaw import-jsonl`
- `openprecedent capture codex import-rollout`

This keeps runtime-specific collection and import behavior explicit without making `runtime` the long-term public namespace.

### `lineage`

Decision-lineage retrieval is its own public domain:

- `openprecedent lineage brief`
- `openprecedent lineage invocation list`
- `openprecedent lineage invocation inspect`

This is the command family that skills should call directly.

### `eval`

Evaluation commands:

- `openprecedent eval fixtures`
- `openprecedent eval captured-openclaw-sessions`

### `doctor`

Operator and automation diagnostics:

- `openprecedent doctor paths`
- `openprecedent doctor storage`
- `openprecedent doctor environment`

This becomes the supported availability-probe surface for skills instead of shell-based file/path probing.

### `version`

Version and build metadata:

- `openprecedent version`

## Global Flags

All public commands support these global flags where applicable:

- `--format json|text`
- `--home <path>`
- `--db <path>`
- `--invocation-log <path>`
- `--config <path>`
- `--no-color`

Commands that manage collected state also support:

- `--state-file <path>`

Default rules:

- skills and automation use `--format json`
- humans default to `text`
- runtime-home defaults remain anchored in `~/.openprecedent/runtime`

## Configuration Contract

Configuration precedence is fixed and documented:

1. explicit CLI flag
2. environment variable
3. config file
4. compiled default

Default path expectations remain:

- `OPENPRECEDENT_HOME` -> runtime home
- database path derived from runtime home unless overridden
- invocation-log path derived from runtime home unless overridden
- collector state path derived from runtime home unless overridden

The Rust CLI should preserve current path defaults during cutover so interface migration does not simultaneously become a storage migration.

## Output Contract

JSON output is the public machine contract.

Rules:

- each command returns either one stable JSON object or one stable JSON array
- object keys are treated as semantically stable across minor releases
- automation and skills must not depend on text rendering
- text rendering may improve for human readability without changing the machine contract

This especially applies to:

- `lineage brief`
- `lineage invocation list`
- `lineage invocation inspect`
- `capture ...`
- `doctor ...`

## Error Contract

Exit-code policy is fixed:

- `0` success
- `1` domain failure, validation failure, runtime failure, or environment failure
- `2` CLI usage error

stderr rules:

- human-readable error messages go to stderr
- JSON output remains on stdout for successful command execution
- diagnostic subcommands under `doctor` may return success with machine-readable health payloads even when they report degraded environment state

## Public vs Internal Interfaces

The Rust public CLI becomes the only supported public executable interface.

This means:

- Python CLI is not retained as a public fallback
- shell wrappers are not retained as a public fallback
- repository-local PM commands such as `openprecedent-pm` remain internal tooling and are not folded into the public product CLI
- repository-local harness scripts may continue to exist only as internal developer tooling, not as product-facing command surfaces

## Skill Integration Policy

Skills must call the CLI directly.

Allowed:

```bash
openprecedent lineage brief --format json ...
openprecedent doctor paths --format json
```

Not allowed after cutover:

- `./scripts/run-codex-decision-lineage-workflow.sh`
- `./scripts/run-harnesshub-decision-lineage-workflow.sh`
- `python -c 'from openprecedent.cli import run; run()'`
- skills that depend on repository-local absolute script paths

The skill integration contract is:

- availability probe uses `openprecedent doctor ...`
- lineage retrieval uses `openprecedent lineage brief --format json`
- follow-up inspection uses `openprecedent lineage invocation ... --format json`

## Rust Architecture

The implementation should use a Rust workspace rather than a single monolithic binary crate.

Recommended workspace layout:

- `crates/openprecedent-cli`
- `crates/openprecedent-core`
- `crates/openprecedent-contracts`
- `crates/openprecedent-store-sqlite`
- `crates/openprecedent-capture-openclaw`
- `crates/openprecedent-capture-codex`

Responsibilities:

- `openprecedent-cli`
  command parsing, output rendering, config loading, error mapping
- `openprecedent-core`
  domain workflows for case, event, decision, replay, precedent, lineage, and eval
- `openprecedent-contracts`
  public types, config types, JSON output shapes, error categories
- `openprecedent-store-sqlite`
  SQLite schema access and migrations
- `openprecedent-capture-openclaw`
  OpenClaw session discovery, import, and collection
- `openprecedent-capture-codex`
  Codex rollout import

The Rust CLI must not shell out to the Python CLI or treat Python as its runtime backend.

## Migration Phases

### Phase 1: Contract Baseline

Ship the design baseline and create the Rust workspace skeleton.

Required outputs:

- command tree
- global flags
- config precedence
- output contract
- error contract
- `doctor` and `version` skeleton

### Phase 2: Core Domain Commands

Migrate Rust-native implementations for:

- `case`
- `event`
- `decision`
- `replay`
- `precedent`

These commands must read and write the existing persisted store without introducing an incompatible storage migration.

### Phase 3: Capture and Lineage

Migrate Rust-native implementations for:

- `capture openclaw ...`
- `capture codex import-rollout`
- `lineage brief`
- `lineage invocation list`
- `lineage invocation inspect`

This phase is the cutover prerequisite for skill migration.

### Phase 4: Eval and Skill Cutover

Migrate:

- `eval fixtures`
- `eval captured-openclaw-sessions`

Then update skills to call Rust CLI directly.

### Phase 5: Public Cutover

Once the Rust CLI reaches the documented cutover threshold:

- remove public Python CLI support
- remove public shell-wrapper entrypoints
- update public docs to point only at Rust CLI
- keep internal-only scripts out of the supported product interface

## Cutover Criteria

Public cutover is allowed only when all of the following are true:

- Rust CLI covers all currently supported public use cases
- skill integrations have moved to direct CLI invocation
- public documentation uses the Rust CLI
- data compatibility is verified against the current SQLite store and runtime-home layout
- parity tests pass for the currently shipped public behaviors

Once those conditions are met, public cutover is one-way.
The Python CLI and public shell wrappers are removed instead of being left as a long-term fallback path.

## Test Strategy

### Contract Tests

- `--help` snapshots
- JSON output golden tests
- global-flag precedence tests
- error-code tests
- `doctor` output and degradation tests

### Compatibility Tests

- open existing SQLite database fixtures
- read existing invocation-log fixtures
- verify current runtime-home defaults remain valid

### Parity Tests

For the migration window, compare Rust behavior against the currently shipped public behavior for:

- case operations
- event operations
- decision extraction and listing
- replay
- precedent lookup
- OpenClaw capture
- Codex rollout capture
- lineage brief and invocation inspection
- evaluation commands

### Integration Tests

- skill invocation through `openprecedent lineage brief --format json`
- direct CLI-based availability probing through `doctor`
- validation harnesses updated to use the CLI instead of script wrappers

## Out of Scope

This design does not define:

- a generic SDK for arbitrary third-party runtimes
- a hosted multi-tenant API architecture
- a long-term HTTP API redesign
- a plugin framework for all future agents

Those can be revisited later, but the CLI must be stabilized first because it is the immediate public interface boundary.
