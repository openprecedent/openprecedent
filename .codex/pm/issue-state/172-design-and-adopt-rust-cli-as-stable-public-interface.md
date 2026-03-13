---
type: issue_state
issue: 172
task: .codex/pm/tasks/public-cli-foundation/design-and-adopt-rust-cli-as-stable-public-interface.md
title: Design and adopt a Rust CLI as the stable public interface for OpenPrecedent
status: done
---

## Summary

Create the design baseline for OpenPrecedent's long-term public interface evolution by defining a Rust-based `openprecedent` CLI that replaces public Python CLI and public shell-wrapper exposure.

## Validated Facts

- the shipped MVP currently presents a Python CLI as the public executable surface
- multiple skill and validation workflows still rely on repository-local shell scripts, which makes the effective external interface unstable
- the current command surface already includes more than decision-lineage: case, event, replay, extraction, precedent, runtime capture, and evaluation
- the repository currently has no Rust workspace or Rust implementation scaffold, so the first deliverable must be a contract-first design rather than an incremental code port

## Open Questions

- whether a future follow-up issue should separately redesign the HTTP or API surface after the CLI contract is stabilized

## Next Steps

- land the design baseline through issue `#172`
- use this document as the parent contract for later Rust CLI implementation issues under the public CLI foundation epic
- keep future CLI execution issues scoped to implementation slices instead of reopening command-contract decisions

## Artifacts

- `.codex/pm/prds/public-interface-evolution.md`
- `.codex/pm/epics/public-cli-foundation.md`
