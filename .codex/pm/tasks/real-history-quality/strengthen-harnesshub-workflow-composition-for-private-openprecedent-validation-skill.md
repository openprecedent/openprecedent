---
type: task
epic: real-history-quality
slug: strengthen-harnesshub-workflow-composition-for-private-openprecedent-validation-skill
title: Strengthen HarnessHub workflow composition for private OpenPrecedent validation skill
status: done
task_type: implementation
labels: documentation,harness
issue: 233
state_path: .codex/pm/issue-state/233-strengthen-harnesshub-workflow-composition-for-private-openprecedent-validation-skill.md
---

## Context

The second-phase HarnessHub reliability study under `#220` found that later real issue rounds completed and merged without any new OpenPrecedent invocation records even though the Rust-CLI-based private validation skill was installed locally. The evidence points to workflow composition drift rather than retrieval degradation or Rust CLI failure: the private validation skill exists, but HarnessHub's main issue workflow can still run end to end without ever bringing that skill into the session.

## Deliverable

Strengthen the private HarnessHub skill installation so local issue-delivery sessions have an explicit composition surface that pulls `openprecedent-harnesshub-validation` into the default session workflow when it is installed, while still keeping OpenPrecedent private and optional.

## Scope

- add a private session-composition skill for local HarnessHub work
- update the HarnessHub private skill installer to install the composition skill together with the validation skill
- update repository docs to describe the installed private skill bundle accurately
- record the local PM outcome for issue `#233`

## Acceptance Criteria

- the OpenPrecedent-maintained HarnessHub private bundle contains a composition surface in addition to the validation skill
- the composition surface clearly instructs local HarnessHub issue sessions to pair the validation skill with `harness-issue-execution` or `harness-multi-issue-delivery`
- the installer refreshes both private skills into a local HarnessHub workspace
- the change does not turn missing OpenPrecedent setup into a HarnessHub repository error

## Validation

- run `./scripts/run-pytest.sh -q tests/test_harnesshub_skill_install_script.py`
- run `./scripts/run-agent-preflight.sh`
- refresh the private skill bundle into the local HarnessHub checkout and confirm both private skill roots are present

## Implementation Notes

- prefer a private skill-bundle solution over modifying HarnessHub's public tracked workflow files
- keep the fix targeted at session composition rather than adding a hard dependency to `issue-deliver`
- implemented the fix as a second private skill, `openprecedent-harnesshub-composition`, installed alongside `openprecedent-harnesshub-validation`
- verified the bundle by refreshing the local HarnessHub checkout and confirming both private skill roots exist
