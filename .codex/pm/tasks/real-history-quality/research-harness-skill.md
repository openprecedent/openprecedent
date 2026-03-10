---
type: task
epic: real-history-quality
slug: research-harness-skill
title: Add a research-harness skill and experiment templates for hypothesis-driven work
status: done
task_type: implementation
labels: feature,docs
issue: 105
---

## Context

OpenPrecedent is now in a post-MVP research validation phase, but the repository-local workflow still mostly looks like implementation tracking.
That makes research issues too easy to frame loosely and too hard to compare across repeated product-learning loops.

## Deliverable

Add a project-local research harness skill and lightweight experiment templates that fit the current issue-task-PR workflow.

## Scope

- add a local `research-harness` skill under `.codex/skills/`
- include templates for research issue framing, experiment planning, and result capture
- point the skill at the existing PM and issue-state mechanisms instead of inventing a separate system
- document the skill as part of the repository's current research validation phase

## Acceptance Criteria

- research issues can be framed with explicit hypothesis, method, artifact, and interpretation structure
- the skill remains compatible with the current issue-task-PR process
- later sessions can reuse the templates instead of reconstructing research workflow from memory

## Validation

- `.venv/bin/pytest tests/test_cli.py -k 'research_harness_skill_exists or mvp_status_mentions_research_harness_skill'`

## Implementation Notes

This skill is intentionally lightweight.
It improves the structure of research-shaped work without turning the repository into a separate experiment-management platform.
