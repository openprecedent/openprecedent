---
type: epic
slug: real-history-quality
title: Real history quality
status: backlog
prd: mvp-runtime-validation
---

## Outcome

Improve the quality of replay, evaluation, and precedent behavior on real or anonymized collected session history instead of relying only on curated fixtures.

## Scope

- add anonymized real-session fixtures
- expand evaluation coverage beyond curated examples
- improve precedent ranking once real-history coverage exists
- keep the work tied to real session behavior instead of abstract algorithm changes

## Acceptance Criteria

- the epic contains task files aligned with the current open quality issues
- the task files make their dependency order explicit
- future agents can see that real-session fixtures should land before precedent-ranking tuning

## Child Issues

- `#26` Add anonymized real-session fixtures to the evaluation suite
- `#28` Improve precedent ranking quality on larger real-case history
- `#166` Add a standard Codex session-start workflow for issue continuity and default direct-fix behavior
- `#164` Resolve repository-local test runner before reporting missing pytest
- `#168` Enforce local task status correctness before PR creation and reconcile remote drift
- `#204` Restore local PM twins for remaining open GitHub issues

## Notes

`#28` depends on `#26` at the local PM layer because ranking quality should be improved against a stronger real-session corpus rather than only the current curated fixtures.
