---
type: task
epic: codex-runtime-research
slug: model-codex-specific-event-normalization-and-noise-stripping
title: Model Codex-specific event normalization and noise stripping
status: done
labels: feature,test,docs
issue: 127
depends_on: 126
---

## Context

Raw Codex rollout history includes runtime wrapper records and transport metadata that would pollute replay and later semantic extraction if imported directly.

## Deliverable

Strip low-value Codex rollout noise while preserving replay-relevant semantic evidence.

## Scope

- ignore Codex transport or wrapper records that do not improve replay
- clean retained tool evidence so wrapper output lines do not dominate the payload
- add regression fixtures for noisy Codex rollout samples

## Acceptance Criteria

- replay of imported Codex rollout history is cleaner than the raw source
- retained events still preserve semantic user, agent, and tool evidence
- regression coverage locks the chosen normalization behavior

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_api.py tests/test_cli.py -k 'codex_rollout'`
