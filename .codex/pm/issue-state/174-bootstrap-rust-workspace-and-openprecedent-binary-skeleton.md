---
type: issue_state
issue: 174
task: .codex/pm/tasks/public-cli-foundation/bootstrap-rust-workspace-and-openprecedent-binary-skeleton.md
title: Bootstrap the Rust workspace and openprecedent binary skeleton
status: done
delivery_stage: pr_opened
pr_url: https://github.com/openprecedent/openprecedent/pull/188
---

## Summary

Bootstrap the Rust workspace and the `openprecedent` binary so later command slices can land on a stable crate layout and top-level command taxonomy.

## Validated Facts

- the repository now has a root `Cargo.toml` workspace for the Rust public CLI workstream
- the workspace includes `openprecedent-cli`, `openprecedent-contracts`, `openprecedent-core`, `openprecedent-store-sqlite`, `openprecedent-capture-openclaw`, and `openprecedent-capture-codex`
- the Rust binary is named `openprecedent`
- the top-level command roots already exist in the Rust skeleton: `case`, `event`, `decision`, `replay`, `precedent`, `capture`, `lineage`, `eval`, `doctor`, and `version`
- `cargo test` passes for the new workspace
- `cargo run -p openprecedent-cli -- version` and `cargo run -p openprecedent-cli -- --help` both succeed locally

## Open Questions

- whether the next slice should prioritize global config or begin introducing shared CLI argument types alongside issue `#175`

## Next Steps

- review and merge PR `#188` into `codex/issue-172-rust-public-cli`
- start `#175` from the refreshed integration branch after the workspace bootstrap lands

## Artifacts

- `Cargo.toml`
- `Cargo.lock`
- `rust/openprecedent-cli/`
- `rust/openprecedent-contracts/`
- `rust/openprecedent-core/`
- `rust/openprecedent-store-sqlite/`
- `rust/openprecedent-capture-openclaw/`
- `rust/openprecedent-capture-codex/`
- `tests/test_rust_cli_workspace.py`
