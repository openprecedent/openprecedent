---
name: openprecedent-harnesshub-composition
description: Use for issue-scoped or multi-issue delivery work in a local HarnessHub workspace so the private OpenPrecedent validation skill is composed with HarnessHub's normal workflow when available.
user-invocable: false
---

# OpenPrecedent HarnessHub Composition

Use this skill inside `/workspace/02-projects/active/HarnessHub` for normal local HarnessHub delivery sessions.

This skill exists to make the private OpenPrecedent validation layer part of the default local session composition without changing HarnessHub's public repository workflow.

## Goal

Improve lineage-invocation adherence across later HarnessHub issue rounds while keeping OpenPrecedent optional and private.

## Default Composition Rule

If the private validation skill is installed locally, treat it as the default companion to HarnessHub's main workflow skills.

- For normal single-issue work, compose:
  - `harness-issue-execution`
  - `openprecedent-harnesshub-validation`
- For multi-issue delivery work, compose:
  - `harness-multi-issue-delivery`
  - `openprecedent-harnesshub-validation`

If the private validation skill is absent, continue with the normal HarnessHub workflow without treating that absence as a repository problem.

## Session Entry Behavior

1. Check whether `.codex/skills/openprecedent-harnesshub-validation/SKILL.md` exists in the local HarnessHub workspace.
2. If it exists, treat `openprecedent-harnesshub-validation` as part of the default session composition for this delivery session.
3. Let that validation skill decide whether the local Rust `openprecedent` CLI is available and whether lineage should run at `initial_planning`, `before_file_write`, or `after_failure`.
4. If the validation skill is absent or OpenPrecedent is unavailable, continue the HarnessHub task normally.

## Guardrails

- Do not turn missing OpenPrecedent setup into a HarnessHub repository error.
- Do not edit HarnessHub's public workflow docs to make OpenPrecedent appear required.
- Do not force `issue-deliver`, preflight, or merge flows to depend on OpenPrecedent success.

## Read Next

- `harness-issue-execution`
- `harness-multi-issue-delivery`
- `openprecedent-harnesshub-validation`
