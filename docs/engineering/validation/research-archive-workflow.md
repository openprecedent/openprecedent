# Research Archive Workflow

## Purpose

Define how OpenPrecedent research evidence from a real runtime environment should be archived without committing the entire live runtime state into git.

The archive workflow exists to preserve:

- enough raw evidence to justify a research conclusion
- a stable, reviewable sanitized artifact inside the repository
- a repeatable path for future cross-project studies such as the HarnessHub validation

## Archive Model

Research archiving should always separate three layers:

### 1. Raw Snapshot

This is the local operational capture taken from the live runtime environment.

Examples:

- `openprecedent-runtime-invocations.jsonl`
- a read-only copy of `openprecedent.db`
- temporary study notes

This layer should stay outside git by default.
Store it in a local operations path such as:

- `/workspace/03-operations/admin/runtime-state/openprecedent-research-archive/`

### 2. Sanitized Research Artifact

This is the git-safe evidence set.

It should:

- remove secrets and machine-specific identifiers
- normalize absolute file paths
- keep enough structure for later replay and comparison

This layer belongs in the OpenPrecedent repository.

Recommended path:

- `research-artifacts/<study-slug>/<stamp>/`

### 3. Derived Report

This is the human-readable conclusion:

- what was run
- what was observed
- how confidence changed
- what follow-up should happen next

This layer belongs in:

- `docs/engineering/validation/`

## What Should Enter Git

Commit only the sanitized research artifact and the derived report.

That typically includes:

- sanitized runtime invocation samples
- selected case or decision summaries
- an archive manifest explaining provenance and sanitization
- a study README for interpretation

Do not commit:

- the live runtime database itself
- unredacted session identifiers when they can reveal sensitive context
- raw absolute paths
- credentials, tokens, or `.env` content
- large operational logs that are not needed for the research claim

## Sanitization Rules

At minimum, sanitize these fields before archiving:

- `known_files`
  - convert absolute paths to repo-relative paths when possible
- `case_id`
  - optionally anonymize if it exposes sensitive business context
- `session_id`
  - anonymize or drop unless needed for cross-reference
- free-text notes containing tokens, hostnames, usernames, or machine-local paths

Keep these fields when they directly support the research conclusion:

- `recorded_at`
- `query_reason`
- `task_summary`
- `current_plan`
- `candidate_action`
- `matched_case_ids`
- `task_frame`
- `accepted_constraints`
- `success_criteria`
- `rejected_options`
- `authority_signals`
- `cautions`
- `suggested_focus`

## Recommended Repository Layout

```text
openprecedent/
├── docs/
│   └── engineering/
│       └── validation/
│           ├── harnesshub-real-project-validation-plan.md
│           ├── harnesshub-real-project-observation-log.md
│           ├── harnesshub-real-project-validation-report.md
│           ├── harnesshub-real-project-validation-archive.md
│           └── research-archive-workflow.md
├── research-artifacts/
│   └── harnesshub/
│       └── 2026-03-11T1530Z/
│           ├── archive-manifest.json
│           ├── runtime-invocations-sanitized.jsonl
│           ├── archive-summary.json
│           └── README.md
```

## Quick Archive Procedure

Use the repository script:

```bash
export OPENPRECEDENT_HOME="$HOME/.openprecedent/runtime"
python3 scripts/archive_research_artifacts.py \
  --study harnesshub \
  --query HarnessHub \
  --repo-root /workspace/02-projects/active/HarnessHub
```

This creates a timestamped sanitized archive under:

- `research-artifacts/harnesshub/<stamp>/`

## Archive Contents

The quick archive script currently produces:

- `archive-manifest.json`
  - archive metadata, source paths, and sanitization settings
- `runtime-invocations-sanitized.jsonl`
  - sanitized invocation records matching the study query
- `archive-summary.json`
  - aggregate counts and query filters
- `README.md`
  - minimal interpretation guide for the archived evidence

## When To Archive

Archive at these moments:

- after a meaningful research milestone
- before rebasing away a long-running local branch
- before cleaning or rotating local runtime state
- at the end of a validation round before writing the derived report

## Current HarnessHub Rule

For issue `#131`, use a quick archive after each meaningful HarnessHub validation round rather than waiting until the entire study is complete.

This keeps the research evidence inspectable even if the live runtime state changes later.

## Historical Note

Earlier archived captures from this study remain under `research-artifacts/clawpack/` because that was the active project name at the time they were created.
New archives should use `research-artifacts/harnesshub/`.
