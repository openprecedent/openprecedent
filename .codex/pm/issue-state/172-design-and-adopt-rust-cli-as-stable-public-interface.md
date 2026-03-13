---
type: issue_state
issue: 172
task: .codex/pm/tasks/public-cli-foundation/design-and-adopt-rust-cli-as-stable-public-interface.md
title: Design and adopt a Rust CLI as the stable public interface for OpenPrecedent
status: in_progress
delivery_stage: in_progress
---

## Summary

Keep the Rust public CLI design baseline authoritative while using issue `#172` as the long-lived parent for the full migration train on the dedicated integration branch `codex/issue-172-rust-public-cli`.

## Validated Facts

- the shipped MVP currently presents a Python CLI as the public executable surface
- multiple skill and validation workflows still rely on repository-local shell scripts, which makes the effective external interface unstable
- the current command surface already includes more than decision-lineage: case, event, replay, extraction, precedent, runtime capture, and evaluation
- PR `#173` merged the contract-first Rust CLI design baseline into `main`
- issue `#172` has been reopened so the migration can proceed under one explicit parent issue instead of spawning disconnected implementation tracks
- child issues `#174` through `#187` now cover the Rust workspace, config, store, command families, skill migration, and final cutover in reviewable slices

## Open Questions

- whether any additional split is needed inside the larger capture or lineage slices after implementation starts
- when the integration branch is complete enough to begin the final cutover PR back to `main`

## Next Steps

- implement child issues `#174` through `#187` on branches that merge into `codex/issue-172-rust-public-cli`
- use issue `#172` as the parent reference and branch-policy source for the Rust CLI migration train
- merge the dedicated integration branch back to `main` only after the child issue chain reaches the cutover gate defined in the design doc

## Artifacts

- `.codex/pm/prds/public-interface-evolution.md`
- `.codex/pm/epics/public-cli-foundation.md`
- `.codex/pm/tasks/public-cli-foundation/`
