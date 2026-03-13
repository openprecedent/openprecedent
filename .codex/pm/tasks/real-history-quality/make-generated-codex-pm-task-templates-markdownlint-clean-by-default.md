---
type: task
epic: real-history-quality
slug: make-generated-codex-pm-task-templates-markdownlint-clean-by-default
title: Make generated Codex PM task templates markdownlint-clean by default
status: done
task_type: implementation
labels: ops,test
issue: 206
state_path: .codex/pm/issue-state/206-make-generated-codex-pm-task-templates-markdownlint-clean-by-default.md
---

## Context
Recent task-twin work repeatedly failed CI because `openprecedent.codex_pm task-new` generated empty Markdown sections that were not markdownlint-clean by default.
That turned a repository-generated artifact into a repeatable `MD022` and `MD032` failure mode whenever a new task twin was created and committed before manual cleanup.

## Deliverable
Update the local Codex PM generator so fresh task twins are markdownlint-clean by default and do not leak placeholder content into rendered issue or PR bodies.

## Scope

- change `task-new` to emit lint-safe placeholder section bodies
- keep placeholder content out of generated issue and PR body output
- add regression coverage for both template generation and placeholder rendering behavior

## Acceptance Criteria

- a fresh `task-new` document is markdownlint-clean without manual blank-line fixes
- generated placeholder content does not appear in `issue-body` or `pr-body` output
- regression tests cover the generated task template and placeholder rendering behavior

## Validation

- run `./scripts/run-pytest.sh -q tests/test_codex_pm.py -k 'markdownlint_clean_placeholders or renderers_skip_placeholder_section_bodies or updates_status_and_renders_issue_and_pr_body'`
- run `./scripts/run-agent-preflight.sh`

## Implementation Notes

- Use one lint-safe placeholder form consistently instead of relying on authors to fix spacing by hand after task generation.
