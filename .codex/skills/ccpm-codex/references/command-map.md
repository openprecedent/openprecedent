# Command Map

This skill ports the ccpm command model into Codex-friendly local commands.

## Core Planning

- `/pm:init`
  - Codex equivalent: `python3 -m openprecedent.codex_pm init`
- `/pm:prd-new`
  - Codex equivalent: `python3 -m openprecedent.codex_pm prd-new <slug> --title "<title>"`
- `/pm:epic-new`
  - Codex equivalent: `python3 -m openprecedent.codex_pm epic-new <slug> --title "<title>" --prd <prd-slug>`
- `/pm:task-new`
  - Codex equivalent: `python3 -m openprecedent.codex_pm task-new <epic> <slug> --title "<title>" --issue <n> --labels feature,test`

## Execution Flow

- `/pm:next`
  - Codex equivalent: `python3 -m openprecedent.codex_pm next`
- `/pm:issue-start`
  - Codex equivalent:
    1. `python3 -m openprecedent.codex_pm set-status <task-path> in_progress`
    2. create a new branch from `upstream/main`
    3. start implementation for that issue only
- `/pm:blocked`
  - Codex equivalent: `python3 -m openprecedent.codex_pm blocked <task-path> --reason "<reason>"`
- `/pm:done`
  - Codex equivalent: `python3 -m openprecedent.codex_pm set-status <task-path> done`

## Sync Helpers

- `/pm:issue-sync`
  - Codex equivalent: regenerate the issue body from the task file:
    `python3 -m openprecedent.codex_pm issue-body <task-path>`
- `/pm:issue-create`
  - Codex equivalent:
    `python3 -m openprecedent.codex_pm issue-create <task-path>`
- `/pm:pr-body`
  - Codex equivalent:
    `python3 -m openprecedent.codex_pm pr-body <task-path> --issue <n> --tests "<cmd>"`
- `/pm:pr-create`
  - Codex equivalent:
    `python3 -m openprecedent.codex_pm pr-create <task-path> --tests "<cmd>"`
- `/pm:standup`
  - Codex equivalent: `python3 -m openprecedent.codex_pm standup`

## GitHub Usage

Pair the local commands with `gh`:

- create issue:
  - `python3 -m openprecedent.codex_pm issue-create <task-path>`
- create PR:
  - `python3 -m openprecedent.codex_pm pr-create <task-path> --tests "..."`
