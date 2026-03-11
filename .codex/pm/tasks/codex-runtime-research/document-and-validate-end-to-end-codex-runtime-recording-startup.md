---
type: task
epic: codex-runtime-research
slug: document-and-validate-end-to-end-codex-runtime-recording-startup
title: Document and validate end-to-end Codex runtime recording startup
status: done
labels: docs,test,feature
issue: 148
depends_on: 130
---

## Context

Codex minimal runtime support exists, but the repository still needs one practical guide that a human or agent can follow to start OpenPrecedent for Codex project work and verify that runtime recording is actually happening.

## Deliverable

Add one end-to-end startup guide for Codex runtime recording and validate the full startup-and-recording loop in the same PR.

## Scope

- write a practical guide for humans and agents
- add a reusable repository-local Codex live-validation harness
- record one durable startup validation artifact
- file follow-up issues only if the validation reveals missing capabilities

## Acceptance Criteria

- one durable guide explains how to start OpenPrecedent for Codex project work and how to verify recording
- the guide is usable by both humans and agents without hidden local context
- the PR includes a documented end-to-end validation of multiple Codex runtime interactions producing inspectable records

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_codex_live_validation_script.py`
- `PYTHONPATH=src .venv/bin/pytest tests/test_cli.py -k 'codex_runtime_decision_lineage_skill_exists'`
