# File Model

The local Codex PM workspace lives under `.codex/pm/`.

## Layout

```text
.codex/
  skills/
    ccpm-codex/
      SKILL.md
      references/
  pm/
    prds/
    epics/
    tasks/
    context/
    updates/
```

## Document Types

### PRD

- path: `.codex/pm/prds/<slug>.md`
- frontmatter keys:
  - `type: prd`
  - `slug`
  - `title`
  - `status`

### Epic

- path: `.codex/pm/epics/<slug>.md`
- frontmatter keys:
  - `type: epic`
  - `slug`
  - `title`
  - `status`
  - `prd`

### Task

- path: `.codex/pm/tasks/<epic>/<slug>.md`
- frontmatter keys:
  - `type: task`
  - `epic`
  - `slug`
  - `title`
  - `status`
  - `issue`
  - `labels`
  - `depends_on`
  - `status_reason`

## Status Values

- `backlog`
- `in_progress`
- `blocked`
- `done`

## Conventions

- Keep one task file aligned with one GitHub issue.
- Keep one issue aligned with one branch and one PR.
- Use the task file as the canonical source for issue and PR body text.
- Use `context/` and `updates/` only for local supporting notes, not for replacing GitHub issue state.
