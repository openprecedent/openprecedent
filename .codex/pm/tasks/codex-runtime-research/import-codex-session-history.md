---
type: task
epic: codex-runtime-research
slug: import-codex-session-history
title: Import Codex session history into OpenPrecedent as replayable cases and events
status: done
labels: feature,test,docs
issue: 126
depends_on: 125
---

## Context

Codex cannot serve as a serious research runtime unless its session history can be ingested into replayable `case` and `event` records.

## Deliverable

Add a minimal Codex rollout import path that produces replayable cases and events.

## Scope

- support importing one real Codex rollout JSONL source into OpenPrecedent
- normalize core Codex interaction data into ordered events
- preserve enough context for replay, later semantic extraction, and precedent use
- keep the scope Codex-specific and local-first

## Acceptance Criteria

- at least one real Codex development session can be imported successfully
- replay of the imported case is understandable and preserves the key interaction timeline
- the importer does not depend on generic runtime abstraction work

## Validation

- `PYTHONPATH=src .venv/bin/pytest tests/test_api.py tests/test_cli.py -k 'codex_rollout or openclaw_runtime_trace'`
