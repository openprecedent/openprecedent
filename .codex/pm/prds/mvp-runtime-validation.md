---
type: prd
slug: mvp-runtime-validation
title: MVP runtime validation and quality
status: draft
---

# MVP runtime validation and quality

## Summary

Backfill the remaining MVP validation and quality work into the local Codex PM workspace so future development can run through repository-local PRD, epic, and task files instead of relying only on ad hoc issue discovery.

## Problem

The repository now has a Codex-native project-management workflow, but the remaining roadmap work is still represented only as standalone GitHub issues. That means agents cannot yet use the local PM workspace to understand the remaining MVP scope, pick the next task, or render issue and PR text from local planning documents.

## Goals

- mirror the remaining open roadmap work into `.codex/pm/`
- group the remaining issues under stable epics tied to the MVP roadmap
- keep one local task file aligned with one GitHub issue
- make `next`, `tasks`, and `standup` useful for the remaining MVP work

## Non-Goals

- rewrite the roadmap itself
- replace GitHub issues as the source of truth for issue state
- introduce a multi-agent swarm or worktree orchestration layer
- close open issues automatically from the backfill alone

## Success Criteria

- the remaining open roadmap issues `#23`, `#26`, and `#28` are represented in `.codex/pm/tasks/`
- the local PM workspace contains epics that explain how the remaining issues fit together
- `python3 -m openprecedent.codex_pm next --json` returns one of the remaining backlog tasks
- future agents can start from the local PM workspace without reconstructing the remaining roadmap by hand

## Dependencies

- GitHub issues `#23`, `#26`, and `#28`
- existing local Codex PM skill and CLI
- the MVP roadmap in `docs/product/mvp-roadmap.md`
