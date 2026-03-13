---
type: task
epic: public-cli-foundation
slug: implement-global-config-path-resolution-doctor-and-version-contracts-in-rust-cli
title: Implement global config, path resolution, doctor, and version contracts in the Rust CLI
status: done
task_type: implementation
labels: cli,rust,interface
issue: 175
state_path: .codex/pm/issue-state/175-implement-global-config-path-resolution-doctor-and-version-contracts-in-rust-cli.md
---

## Context

The Rust workspace from `#174` already established the binary and crate layout.
This slice needs to turn the Rust CLI from a pure topology scaffold into a machine-usable contract surface by adding global flags, config precedence, and the first real commands: `doctor` and `version`.

## Deliverable

Implement the Rust-side config resolution contract and expose `openprecedent doctor ...` and `openprecedent version` as working commands with stable JSON output.

## Scope

- implement global CLI flags for `--format`, `--home`, `--db`, `--invocation-log`, `--state-file`, `--config`, and `--no-color`
- define resolution precedence across flags, environment variables, optional config file, and defaults
- implement `doctor paths`, `doctor storage`, and `doctor environment`
- implement `version` with both text and JSON output
- add Rust integration tests that exercise the contract directly through the compiled binary

## Acceptance Criteria

- the Rust CLI exposes the global configuration contract from the design doc
- `doctor` and `version` work without depending on the Python CLI
- JSON output is stable enough for skill availability probes and automation
- local tests cover precedence behavior and the initial doctor reports

## Validation

- run `. \"$HOME/.cargo/env\" && cargo test -p openprecedent-cli -p openprecedent-core -p openprecedent-contracts`
- run `. \"$HOME/.cargo/env\" && cargo run -p openprecedent-cli -- doctor paths --format json`
- run `./scripts/run-pytest.sh -q tests/test_rust_cli_workspace.py`

## Implementation Notes

- The Rust CLI now defaults runtime home to `~/.openprecedent/runtime`, matching the design baseline instead of the current Python CLI cwd fallback.
- Non-implemented command families still return explicit not-implemented errors, but now use the more accurate long-term subcommand tree.
