---
type: task
epic: codex-runtime-research
slug: extract-semantic-decision-lineage-from-codex-development-sessions
title: Extract semantic decision lineage from Codex development sessions
status: done
labels: feature,test,docs
issue: 128
depends_on: 127
---

## Context

Codex becomes useful as a research runtime only if imported development sessions can yield semantic decision lineage rather than just replayable events.

## Deliverable

Extend semantic extraction so Codex rollout imports can produce reusable judgment records under the current taxonomy.

## Scope

- apply the semantic taxonomy to Codex rollout-derived user and agent messages
- infer approval and authority signals from Codex user guidance when they appear as ordinary messages
- add Codex-style semantic regression fixtures and tests

## Acceptance Criteria

- at least one representative Codex rollout yields semantic decisions under the current taxonomy
- tool and command evidence are not promoted into decisions
- regression coverage protects Codex semantic extraction behavior

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_api.py tests/test_cli.py -k 'codex_rollout or codex_semantic'`
