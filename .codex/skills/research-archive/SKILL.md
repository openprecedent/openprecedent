---
name: research-archive
description: Use when OpenPrecedent research evidence from a live runtime environment should be sanitized and archived into the repository as reviewable artifacts instead of committing raw runtime state. Covers quick archival for studies such as HarnessHub validation rounds.
---

# Research Archive

Use this skill when a research or validation round has produced runtime evidence that should be preserved in git-safe form.

Typical triggers:

- the user asks to archive current research evidence
- a real-project validation round is ending
- live runtime invocation records should be frozen before the local runtime state changes
- a derived report needs a stable artifact path to cite
- a research observation or progress-analysis turn has just produced a new finding that should become durable evidence

Do not use this skill to back up the entire live runtime directory.
Its purpose is sanitized evidence capture, not operational backup.

## Goal

Create a minimal, reviewable archive that:

1. keeps the master research framing in OpenPrecedent docs
2. preserves sanitized runtime evidence in `research-artifacts/`
3. avoids committing raw databases, secrets, or machine-local state

## Workflow

1. Confirm the study slug and any query filter.
   - Example study: `harnesshub`
   - Example query: `HarnessHub`

2. Make sure the shared runtime home is set.
   - Default:
   - `OPENPRECEDENT_HOME=$HOME/.openprecedent/runtime`

3. Run the archive script:

```bash
python3 scripts/archive_research_artifacts.py \
  --study harnesshub \
  --query HarnessHub \
  --repo-root /workspace/02-projects/active/HarnessHub
```

4. Inspect the generated directory under:
   - `research-artifacts/<study>/<stamp>/`

5. When the archive should support a report or observation log, cite:
   - `archive-manifest.json`
   - `archive-summary.json`

6. For research turns, pair the archive with a log update.
   - Append the finding to the active observation log before finishing the turn.
   - Report both the updated log path and the new archive path in the response.
   - Treat this as the default close-out after a research observation unless the user explicitly says to skip archival.

## Decision Rules

- Prefer narrow query terms that isolate one study round.
- Prefer repo-relative path sanitization when the relevant repo root is known.
- Commit only sanitized artifacts, never the live runtime database.
- If no matching records exist, do not invent an archive; report that nothing was captured.

## Read Next

- [`docs/engineering/research-archive-workflow.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/research-archive-workflow.md)
- [`docs/engineering/harnesshub-real-project-validation-plan.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/harnesshub-real-project-validation-plan.md)
