---
name: ccpm-codex
description: Use when work should follow a spec-to-epic-to-issue GitHub workflow inside this repository using Codex instead of Claude Code. Provides a project-local equivalent of ccpm for PRDs, epics, task files, issue bodies, PR bodies, next-task selection, and issue-scoped execution.
---

# CCPM For Codex

Use this skill for project-management work in this repository when the task involves PRDs, epics, task decomposition, GitHub issue creation, issue-driven execution, or PR body generation.

## Workflow

1. Initialize the local PM workspace if `.codex/pm/` is missing:
   - `python3 -m openprecedent.codex_pm init`
2. Create or update the planning documents:
   - PRD: `python3 -m openprecedent.codex_pm prd-new <slug> --title "<title>"`
   - Epic: `python3 -m openprecedent.codex_pm epic-new <slug> --title "<title>" --prd <prd-slug>`
   - Task: `python3 -m openprecedent.codex_pm task-new <epic> <slug> --title "<title>" --issue <n> --labels feature,test`
3. Treat each task file as the local twin of one GitHub issue.
4. Keep task status in sync with the branch and PR state:
   - start work: `set-status ... in_progress`
   - blocked: `blocked ... --reason "..."`
   - merged: `set-status ... done`
5. Generate GitHub text from the task file instead of rewriting it each time:
   - issue body: `python3 -m openprecedent.codex_pm issue-body <task-path>`
   - PR body: `python3 -m openprecedent.codex_pm pr-body <task-path> --issue <n> --tests "..."`
   - PR creation: `python3 -m openprecedent.codex_pm pr-create <task-path> --tests "..."`
6. Pick the next local task with:
   - `python3 -m openprecedent.codex_pm next`

## Repository Rules

- One issue per branch.
- One issue per PR.
- Always branch from the latest `upstream/main`.
- Use `Closes #<issue>` in the PR body.
- Do not append commits to a branch whose PR has already been merged.

## Read Next

- Command mapping and command equivalents: `references/command-map.md`
- File model and local PM directory layout: `references/file-model.md`
