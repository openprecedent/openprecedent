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

Strengthen the private HarnessHub validation skill itself so the skill exposes a clearer single-entry surface for session composition and lineage retrieval when it is installed locally, while still keeping OpenPrecedent private and optional.

## Scope

- strengthen the private HarnessHub validation skill metadata and session-entry instructions so one skill carries both the composition rule and the validation workflow
- keep the HarnessHub private skill installer focused on that one validation skill
- update repository docs to describe the strengthened single-skill integration accurately
- record the local PM outcome for issue `#233`

## Acceptance Criteria

- the OpenPrecedent-maintained HarnessHub validation skill itself clearly instructs local HarnessHub issue sessions to pair it with `harness-issue-execution` or `harness-multi-issue-delivery`
- the validation skill carries both the session-composition guidance and the lineage-query workflow
- the installer refreshes the strengthened validation skill into a local HarnessHub workspace
- the change does not turn missing OpenPrecedent setup into a HarnessHub repository error

## Validation

- run `./scripts/run-pytest.sh -q tests/test_harnesshub_skill_install_script.py`
- run `./scripts/run-agent-preflight.sh`
- refresh the private validation skill into the local HarnessHub checkout and confirm the updated skill text is present

## Implementation Notes

- prefer a stronger one-skill private entry surface over splitting composition and validation into separate local skills
- keep the fix targeted at session composition rather than adding a hard dependency to `issue-deliver`
- verified the strengthened skill by refreshing the local HarnessHub checkout and confirming the updated single-skill instructions were installed
- this issue improves the skill-side entry surface but does not by itself prove that later stable loading can be attributed solely to the repository-side skill change
