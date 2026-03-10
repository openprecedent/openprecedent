---
type: task
epic: real-history-quality
slug: openclaw-live-validation-skill
title: Create an OpenClaw live validation skill for runtime integration tasks
status: done
task_type: implementation
labels: feature,docs
issue: 120
---

## Context

The repository already has a live OpenClaw validation harness script, but Codex still needed an explicit workflow-level reminder about when to run it and how to interpret the result.
That made runtime smoke validation too dependent on manual prompting.

## Deliverable

Add a project-local `openclaw-live-validation` skill that orchestrates when and how to use the live validation harness for runtime integration work.

## Scope

- add a local `openclaw-live-validation` skill under `.codex/skills/`
- encode trigger conditions for runtime integration, trigger-policy, and shared-runtime-path changes
- point the skill at `scripts/run-openclaw-live-validation.sh` and current runtime validation docs
- require stable outcome capture in issue state or validation notes

## Acceptance Criteria

- runtime integration tasks have a clear skill-based trigger for real OpenClaw smoke validation
- the skill reuses the existing live validation harness instead of duplicating it
- expected runtime outcome classes are explicit enough to guide follow-up work

## Validation

- `.venv/bin/pytest tests/test_cli.py -k 'openclaw_live_validation_skill_exists or tooling_setup_mentions_live_validation_skill'`

## Implementation Notes

This skill intentionally orchestrates the existing harness and documentation chain.
It should make the agent more likely to run live smoke validation at the right moment, not introduce a second validation system.
