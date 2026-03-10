---
type: task
epic: real-history-quality
slug: productize-live-openclaw-validation-harness
title: Productize a live OpenClaw validation harness for runtime integration work
status: done
task_type: implementation
labels: feature,ops,docs,test
issue: 104
---

## Context

The most important runtime integration bugs during MVP were discovered in the live OpenClaw loop rather than repository-local pytest or fixture-only validation.
Those checks still depended on ad hoc shell sequences and manual artifact collection.

## Deliverable

Add a reusable local harness entrypoint that prepares a live OpenClaw validation workspace, optionally seeds shared prior history, and refreshes a structured invocation summary after the live run.

## Scope

- add `scripts/run-openclaw-live-validation.sh`
- support optional seeding of prior history from a supplied OpenClaw session transcript
- emit stable local artifacts such as a manifest, prompt file, launcher, and invocation summary
- document the harness and link it from existing runtime validation docs
- add tests for workspace preparation and invocation summary refresh

## Acceptance Criteria

- live OpenClaw validation no longer depends on remembering ad hoc setup sequences
- the harness produces inspectable artifacts for later debugging and research
- rerunning the harness refreshes invocation evidence from the shared runtime log

## Validation

- `.venv/bin/pytest tests/test_live_validation_script.py`

## Implementation Notes

This harness deliberately stops short of automating the OpenClaw UI or gateway interaction itself.
It standardizes the live validation workspace and evidence collection without turning the repository into a deployment or orchestration system.
