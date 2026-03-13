---
type: issue_state
issue: 172
task: .codex/pm/tasks/public-cli-foundation/design-and-adopt-rust-cli-as-stable-public-interface.md
title: Design and adopt a Rust CLI as the stable public interface for OpenPrecedent
status: done
delivery_stage: done
---

## Summary

Issue `#172` started as the Rust public CLI design issue, later served as the parent integration issue for the migration train, and is now in final closeout with a repository-local implementation summary that documents what the shipped Rust CLI actually provides on `main`.

## Validated Facts

- the shipped MVP currently presents a Python CLI as the public executable surface
- multiple skill and validation workflows still rely on repository-local shell scripts, which makes the effective external interface unstable
- the current command surface already includes more than decision-lineage: case, event, replay, extraction, precedent, runtime capture, and evaluation
- PR `#173` merged the contract-first Rust CLI design baseline into `main`
- issue `#172` was reopened so the migration could proceed under one explicit parent issue instead of spawning disconnected implementation tracks
- child issues `#174` through `#187` now cover the Rust workspace, config, store, command families, skill migration, and final cutover in reviewable slices
- child issues `#174` through `#187` have merged into `codex/issue-172-rust-public-cli`
- the integration branch now exposes the Rust `openprecedent` CLI as the supported public command surface and removes the public Python CLI and public shell-script entrypoints
- PR `#202` merged the completed migration train back into `main`
- the repository now contains a dedicated engineering implementation summary for the shipped Rust CLI
- integrated validation passed through `cargo test`, targeted Python regression coverage, and `./scripts/run-agent-preflight.sh`

## Open Questions

- none

## Next Steps

- merge the closeout documentation PR that closes issue `#172`

## Artifacts

- `.codex/pm/prds/public-interface-evolution.md`
- `.codex/pm/epics/public-cli-foundation.md`
- `.codex/pm/tasks/public-cli-foundation/`
