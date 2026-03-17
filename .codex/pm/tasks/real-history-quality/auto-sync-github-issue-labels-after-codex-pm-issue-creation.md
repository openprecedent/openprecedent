---
type: task
epic: real-history-quality
slug: auto-sync-github-issue-labels-after-codex-pm-issue-creation
title: Automatically synchronize GitHub issue labels after Codex PM issue creation
status: done
task_type: implementation
labels: harness,docs
issue: 231
state_path: .codex/pm/issue-state/231-auto-sync-github-issue-labels-after-codex-pm-issue-creation.md
---

## Context

Task twins already carry label metadata, but GitHub issue creation still happens through ad hoc `gh issue create` calls. That leaves issue labels as a manual follow-up step and allowed unlabeled issues to accumulate across the repository archive.

## Deliverable

Add a repository-local `codex_pm issue-create` path that creates the GitHub issue and automatically applies the task twin label set to the created issue.

## Scope

- add a new `issue-create` Codex PM command
- render the GitHub issue body from the task twin without duplicating labels inside the issue text
- apply task-twin labels to the created GitHub issue automatically
- add regression coverage for labeled and unlabeled task twins
- update the local CCPM skill docs to route issue creation through the guarded command

## Acceptance Criteria

- `python3 -m openprecedent.codex_pm issue-create <task-path>` creates the GitHub issue
- labeled task twins automatically apply their labels to the created issue
- unlabeled task twins still create issues successfully without any extra label-edit step
- docs point repository issue creation to the new guarded command instead of raw `gh issue create`

## Validation

- `OPENPRECEDENT_PYTHON_BIN=/workspace/02-projects/incubation/openprecedent/.venv/bin/python ./scripts/run-pytest.sh -q tests/test_codex_pm.py -k 'issue_create or renderers_skip_placeholder_section_bodies or task_new_generates_markdownlint_clean_placeholders'`
- `OPENPRECEDENT_PYTHON_BIN=/workspace/02-projects/incubation/openprecedent/.venv/bin/python ./scripts/run-agent-preflight.sh`

## Implementation Notes

- `issue-create` creates the issue first, parses the returned issue number from the GitHub URL, and then applies each task label with `gh issue edit --add-label`
- the issue body used for `issue-create` omits the `## Labels` section because labels are now synchronized through GitHub metadata instead of duplicated inside the issue text
