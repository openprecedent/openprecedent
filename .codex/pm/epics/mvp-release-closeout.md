---
type: epic
slug: mvp-release-closeout
title: MVP release closeout
status: backlog
prd: mvp-release-closeout
---

## Outcome
Deliver a standard research-oriented MVP release baseline for OpenPrecedent that can be installed and used in new projects, without confusing post-MVP research work with MVP-blocking implementation.


## Scope

- coverage visibility and release gating
- release scope and positioning
- versioning and release wording cleanup
- new-project installation and quickstart guidance
- release validation checklist
- release artifacts and publication flow
- final release closeout and post-release research handoff

## Acceptance Criteria

- child issues define all required release closeout work
- release gating explicitly includes a 90 percent coverage threshold
- the final release can be validated and published without reopening MVP product scope
- post-release research issues remain clearly separated from release-blocking work

## Child Issues

- `#244` Frame MVP release closeout plan and issue breakdown
- `#246` Add Rust and Python coverage reporting to CI and release readiness
- `#243` Raise the MVP release coverage baseline to 90 percent
- `#245` Define the MVP release scope and positioning
- `#249` Unify MVP versioning and release wording
- `#248` Add MVP quickstart and new-project installation guide
- `#251` Codify the MVP release validation checklist
- `#247` Prepare standard MVP release artifacts and publication flow
- `#250` Close out the MVP release baseline and hand off post-release research

## Notes

This epic is specifically for standardizing the current MVP into a publishable baseline. It should not absorb ongoing post-MVP research issues such as `#163`, `#235`, `#236`, `#237`, `#224`, `#225`, `#226`, `#227`, `#240`, or `#241`.
