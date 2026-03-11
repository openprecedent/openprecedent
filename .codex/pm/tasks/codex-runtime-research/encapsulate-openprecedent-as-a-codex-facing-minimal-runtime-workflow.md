---
type: task
epic: codex-runtime-research
slug: encapsulate-openprecedent-as-a-codex-facing-minimal-runtime-workflow
title: Encapsulate OpenPrecedent as a Codex-facing minimal runtime workflow
status: done
labels: feature,test,docs
issue: 130
depends_on: 129
---

## Context

Codex now has imported history, semantic extraction, and project-local precedent validation, but it still lacks a narrow runtime-facing workflow for consuming decision-lineage context during later development work.

## Deliverable

Add a Codex-facing minimal runtime workflow that requests semantic decision-lineage briefs and preserves invocation observability.

## Scope

- add a repository-local Codex runtime workflow entrypoint
- add a Codex-facing local skill that teaches when and how to use it
- document the workflow and validate that invocation results are inspectable

## Acceptance Criteria

- Codex has a documented and runnable minimal workflow for requesting decision-lineage context
- the workflow stays research-scoped and avoids generic runtime abstraction
- runtime invocation remains inspectable after the workflow runs

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_codex_runtime_workflow_script.py`
- `PYTHONPATH=src .venv/bin/pytest tests/test_cli.py -k 'codex_runtime_decision_lineage_skill_exists'`
