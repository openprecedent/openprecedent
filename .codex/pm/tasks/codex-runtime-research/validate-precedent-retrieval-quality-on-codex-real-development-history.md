---
type: task
epic: codex-runtime-research
slug: validate-precedent-retrieval-quality-on-codex-real-development-history
title: Validate precedent retrieval quality on Codex real development history
status: done
labels: test,docs
issue: 129
depends_on: 128
---

## Context

Codex cannot serve as a serious research runtime unless precedent retrieval over Codex-derived history surfaces semantic lineage rather than superficial operational overlap.

## Deliverable

Produce a durable validation artifact and regression coverage for Codex-derived precedent retrieval quality.

## Scope

- validate precedent lookup on Codex rollout-derived cases
- distinguish semantic usefulness from operational similarity
- record the current finding and boundary in an engineering document

## Acceptance Criteria

- at least one durable validation artifact records the findings
- regression coverage locks semantic preference over operational overlap for Codex-derived cases
- the write-up is concrete enough to guide the next Codex runtime research issue

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_api.py tests/test_cli.py -k 'codex_rollout or codex_semantic or semantically_related_codex_case'`
