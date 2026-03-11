# Harness Reuse Guide

## Goal

Summarize the full current OpenPrecedent harness and explain how to reuse or transplant that harness into another existing repository or a brand new repository.

This document is about harness capability inventory and reuse strategy.
It is not a product architecture document.

## Current Harness Inventory

OpenPrecedent now has a repository-local harness with six main layers.

### 1. Workflow and PM layer

This layer keeps agent work issue-scoped and reviewable.

Main components:

- [AGENTS.md](/workspace/02-projects/incubation/openprecedent/AGENTS.md)
- [.codex/skills/ccpm-codex/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/ccpm-codex/SKILL.md)
- [.codex/skills/harness-gap-closure/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/harness-gap-closure/SKILL.md)
- [codex_pm.py](/workspace/02-projects/incubation/openprecedent/src/openprecedent/codex_pm.py)
- `.codex/pm/tasks/`
- `.codex/pm/issue-state/`

Key capabilities:

- one issue per branch
- one issue per PR
- local task twins for GitHub issues
- issue-scoped development state
- explicit task types such as `implementation`, `docs`, `research`, and `umbrella`
- PR-body and task-closure sync checks
- repository-local PR creation that pins the upstream repo and fork head explicitly
- a reusable workflow for turning repeated failures into harness hardening work

### 2. Local guardrail layer

This layer catches predictable local workflow drift before code is pushed.

Main components:

- [.githooks/pre-push](/workspace/02-projects/incubation/openprecedent/.githooks/pre-push)
- [install-hooks.sh](/workspace/02-projects/incubation/openprecedent/scripts/install-hooks.sh)
- [run-codex-review-checkpoint.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-codex-review-checkpoint.sh)
- [check_branch_freshness.py](/workspace/02-projects/incubation/openprecedent/scripts/check_branch_freshness.py)

Key capabilities:

- require `.codex-review`
- block pushing to branches whose PRs already merged
- block stale branches that are behind `upstream/main`
- run local issue/task closure-sync verification before push when PR context is available through `gh`
- provide a fixed local checkpoint for native Codex `/review`

### 3. Local preflight and CI support layer

This layer helps catch common failures before or after opening a PR.

Main components:

- [run-agent-preflight.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-agent-preflight.sh)
- [triage_pr_checks.py](/workspace/02-projects/incubation/openprecedent/scripts/triage_pr_checks.py)
- [pr-review-gate.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/pr-review-gate.yml)
- [python-ci.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/python-ci.yml)
- [markdownlint.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/markdownlint.yml)

Key capabilities:

- one local preflight entrypoint
- optional Markdown lint and E2E inclusion
- local branch freshness and issue-state checks
- local PR closure sync verification
- fast CI failure classification

### 4. Repository-local validation layer

This layer validates the product loop without requiring a separate live runtime host.

Main components:

- [run-e2e.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-e2e.sh)
- [merge-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/merge-validation.md)
- [openclaw-full-user-journey-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-full-user-journey-validation.md)

Key capabilities:

- standard end-to-end validation command
- fixture-backed OpenClaw journey replay
- repeatable merge-time validation baseline

### 5. Live runtime validation layer

This layer handles the real OpenClaw integration path.

Main components:

- [run-openclaw-live-validation.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-openclaw-live-validation.sh)
- [.codex/skills/openclaw-live-validation/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/openclaw-live-validation/SKILL.md)
- [openclaw-live-validation-harness.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-live-validation-harness.md)

Key capabilities:

- prepare a shared runtime home for live validation
- optionally seed prior history
- sync the installed skill bundle into the target profile workspace
- generate prompt, launcher, and structured output artifacts
- tell the agent when a real smoke validation is warranted

### 6. Research workflow layer

This layer supports post-MVP hypothesis-driven work.

Main components:

- [.codex/skills/research-harness/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/research-harness/SKILL.md)
- research templates under `.codex/skills/research-harness/templates/`
- [mvp-status.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-status.md)
- umbrella issue `#100`

Key capabilities:

- explicit hypothesis, method, artifact, and interpretation framing
- lightweight experiment templates
- compatibility with the existing issue-task-PR workflow

## What Is OpenPrecedent-Specific

These parts are tied to this product and should usually not be copied as-is:

- OpenClaw-specific runtime validation docs
- decision-lineage skill content
- OpenPrecedent CLI assumptions
- product-specific issue epics and task names
- precedent or decision-domain language

When reusing the harness elsewhere, treat these as examples rather than common infrastructure.

## What Is Broadly Reusable

These parts are good candidates for reuse in other repositories:

- issue-task-PR local twin workflow
- task types and closure sync checks
- issue-scoped development state
- `.codex-review` checkpoint pattern
- stale-branch and merged-branch guardrails
- unified local preflight
- CI failure triage helper
- research-harness templates
- live-validation skill pattern

These patterns are useful even if the target repository has a different product domain.

## Export Strategy

There are two practical export paths.

### 1. Export into an existing repository

Use this path when the target repo already has its own CI, docs, and contribution model.

Recommended order:

1. copy the minimal workflow layer
2. copy the local guardrails
3. adapt preflight and CI checks
4. add issue-state support
5. add research or live-validation layers only if the product needs them

Minimal reusable set:

- `AGENTS.md` conventions adapted to the target repo
- `.codex/skills/ccpm-codex/` or an equivalent local PM skill
- `src/.../codex_pm.py` equivalent
- `.githooks/pre-push`
- `scripts/install-hooks.sh`
- `scripts/run-agent-preflight.sh`
- task twin directory layout under `.codex/pm/`

Adaptation work:

- replace product-specific file paths
- replace target branch defaults if the repo does not use `upstream/main`
- replace CI workflow names in triage logic
- align test commands with the target repository

### 2. Export into a brand new repository

Use this path when creating a new agent product repo from scratch.

Recommended bootstrap order:

1. add `AGENTS.md`
2. add local PM workspace and `codex_pm`-style tooling
3. add hook installation and pre-push guardrails
4. add unified preflight
5. add one standard E2E or smoke validation entrypoint
6. add research or live-validation skills if the product is expected to need them

For a new repository, it is usually best to start with the reusable harness core and only later add runtime-specific skills.

## Suggested Reuse Profiles

### Profile A: Delivery-only harness

Use when the target repo mainly needs disciplined implementation work.

Include:

- workflow and PM layer
- local guardrail layer
- preflight and CI support layer

Skip initially:

- live runtime validation layer
- research workflow layer

### Profile B: Agent product harness

Use when the target repo has a real runtime integration path similar to OpenPrecedent.

Include:

- workflow and PM layer
- local guardrail layer
- preflight and CI support layer
- repository-local validation layer
- live runtime validation layer

### Profile C: Research validation harness

Use when the target repo is past MVP plumbing and needs repeated hypothesis loops.

Include:

- workflow and PM layer
- issue-state support
- research workflow layer
- whichever validation layer best matches the product

## Practical Porting Checklist

When moving the harness to another repo, confirm:

- branch naming and default base ref are correct
- CI workflow names used by triage still match
- hook messages and docs fit the new repo's terminology
- preflight test commands match the new repo
- task twin metadata fields match the new workflow
- any runtime smoke validation script points at the new product's actual runtime path

## Recommended Packaging Approach

Do not try to transplant everything at once.

The best practical sequence is:

1. start with workflow, hook, and preflight core
2. use that core in one real repo for a few tasks
3. only then add runtime-specific or research-specific layers

This keeps the exported harness small enough to adopt and prevents the target repo from inheriting OpenPrecedent-specific complexity it does not actually need.

## Related Docs

- [Harness capability analysis](/workspace/02-projects/incubation/openprecedent/docs/engineering/harness-capability-analysis.md)
- [Tooling setup](/workspace/02-projects/incubation/openprecedent/docs/engineering/tooling-setup.md)
- [Repository governance](/workspace/02-projects/incubation/openprecedent/docs/engineering/repository-governance.md)
