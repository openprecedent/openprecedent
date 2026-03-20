---
type: task
epic: mvp-release-closeout
slug: raise-mvp-release-coverage-baseline-to-90-percent
title: Raise the MVP release coverage baseline to 90 percent
status: done
task_type: implementation
labels: test
issue: 243
state_path: .codex/pm/issue-state/243-raise-mvp-release-coverage-baseline-to-90-percent.md
---

## Context

The MVP release should not publish without a concrete test coverage baseline. After coverage reporting exists, the repository needs a defined release gate that requires at least 90 percent coverage for the current MVP release baseline.

## Deliverable

A release gate that requires the current MVP baseline to reach 90 percent coverage before publication.

## Scope

- inspect the initial reported coverage baseline
- identify and close the most meaningful coverage gaps needed to reach 90 percent
- wire the 90 percent threshold into release readiness or CI gating
- keep the scope bounded to current MVP code rather than speculative future coverage work

## Coverage Gate Boundary

The `90%` release gate should measure the MVP release surface defined in `docs/product/mvp-release-scope.md`, not every repository-local support surface.

- Python gate scope:
  - `src/openprecedent/**/*.py`
  - excluding `src/openprecedent/codex_pm.py`
- Rust gate scope:
  - `rust/**/src/lib.rs` release implementation crates
  - excluding `rust/openprecedent-cli/src/main.rs`

The Rust CLI shell remains part of the stable public interface, but its command-routing and text-rendering surface should continue to be enforced through CLI contract tests and the later release validation checklist instead of this line-coverage gate.

## Acceptance Criteria

- the repository can demonstrate 90 percent MVP release coverage
- the threshold is enforced in a standard release path
- the release checklist treats failure to meet the threshold as a blocker

## Validation

- run the coverage workflow and confirm the threshold is met
- run the full release validation path
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

This issue should not start until coverage reporting exists and the measured baseline is visible.
