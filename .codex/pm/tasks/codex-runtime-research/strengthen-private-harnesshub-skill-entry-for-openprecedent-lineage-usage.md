---
type: task
epic: codex-runtime-research
slug: strengthen-private-harnesshub-skill-entry-for-openprecedent-lineage-usage
title: Strengthen private HarnessHub skill entry for OpenPrecedent lineage usage
status: done
task_type: implementation
labels: research,harness,skill
issue: 170
state_path: .codex/pm/issue-state/170-strengthen-private-harnesshub-skill-entry-for-openprecedent-lineage-usage.md
---

## Context

Maintain the private HarnessHub validation skill in OpenPrecedent as the canonical source, then install that skill into HarnessHub so the outward-facing trial skill stays consistent without turning OpenPrecedent into a public HarnessHub dependency.

## Deliverable

Add an OpenPrecedent-maintained HarnessHub validation skill source plus a local install path that syncs the skill bundle into a HarnessHub checkout with the strengthened entry choreography.

## Scope

- add a canonical skill source under `skills/`
- add an install script that copies the skill into HarnessHub's private `.codex/skills/` path
- rewrite the skill wording around availability probe, composition, fallback, and lighter progressive disclosure
- document the install path in OpenPrecedent docs

## Acceptance Criteria

- the canonical HarnessHub validation skill lives in OpenPrecedent rather than only in a copied HarnessHub bundle
- the install path rewrites OpenPrecedent repo references into the installed HarnessHub bundle
- the installed skill explicitly composes with HarnessHub issue-execution workflow and degrades safely when OpenPrecedent is unavailable
- targeted regression tests cover installation and placeholder rewriting

## Validation

- `PYTHONPATH=src .venv/bin/python -m pytest -q tests/test_harnesshub_skill_install_script.py tests/test_codex_runtime_workflow_script.py tests/test_live_validation_script.py`

## Implementation Notes
