---
type: issue_state
issue: 175
task: .codex/pm/tasks/public-cli-foundation/implement-global-config-path-resolution-doctor-and-version-contracts-in-rust-cli.md
title: Implement global config, path resolution, doctor, and version contracts in the Rust CLI
status: done
delivery_stage: pr_opened
pr_url: https://github.com/openprecedent/openprecedent/pull/189
---

## Summary

Implement the cross-cutting Rust CLI contract for config and diagnostics so later command-family migrations can rely on one stable resolution model and one machine-readable availability surface.

## Validated Facts

- the Rust CLI now accepts the planned global flags for format, path overrides, config file input, and no-color
- config resolution now follows the intended precedence: flags, environment variables, config file, then defaults
- `doctor paths`, `doctor storage`, `doctor environment`, and `version` all execute through the Rust binary
- the default Rust runtime home is `~/.openprecedent/runtime`
- Rust integration tests now cover precedence behavior and the doctor or version output contracts

## Open Questions

- whether later command-family slices should start reusing the current resolved-config types directly or first factor more CLI helper modules

## Next Steps

- review and merge PR `#189` into `codex/issue-172-rust-public-cli`
- start `#176` from the refreshed integration branch after the config and doctor contract lands

## Artifacts

- `rust/openprecedent-contracts/src/lib.rs`
- `rust/openprecedent-core/src/lib.rs`
- `rust/openprecedent-cli/src/main.rs`
- `rust/openprecedent-cli/tests/doctor_contract.rs`
