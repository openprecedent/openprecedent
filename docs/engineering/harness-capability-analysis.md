# Harness Capability Analysis

## Goal

Record a repository-grounded analysis of the current OpenPrecedent development harness so future harness work can build from actual MVP development experience rather than memory or generic agent-tooling advice.

For the current harness inventory and reuse/export path, see:

- [harness-reuse-guide.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/harness-reuse-guide.md)

This document focuses on one question:

- what kind of harness does OpenPrecedent already have
- what repeatedly broke or slowed down agent-driven development during MVP work
- what capabilities are still missing if the goal is faster, higher-quality Codex-driven iteration

## Current Harness Role

As of `2026-03-11`, OpenPrecedent is no longer just a product repository.
It is also a local-first harness for developing and validating an agent product in the open.

In practice, the repository already acts as:

- a local PM and workflow harness for issue-scoped agent work
- a repository-local validation harness for CLI and fixture-backed flows
- a real-runtime validation harness for the OpenClaw integration path
- a post-MVP research validation platform for decision-lineage and precedent-reuse hypotheses

The harness is already useful.
It is not yet complete.

## What The Harness Already Has

### 1. Workflow and governance guardrails

The repository already has explicit rules for:

- one issue per branch
- one issue per PR
- no continued work on already-merged branches
- issue-linked PR closure
- local task twins for tracked work

Relevant components:

- [AGENTS.md](/workspace/02-projects/incubation/openprecedent/AGENTS.md)
- [.codex/skills/ccpm-codex/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/ccpm-codex/SKILL.md)
- [codex_pm.py](/workspace/02-projects/incubation/openprecedent/src/openprecedent/codex_pm.py)

This is already better than a normal lightweight repo because it gives Codex a defined delivery state machine instead of relying on memory.

### 2. Local push guardrails

The repository already has a local pre-push hook:

- [.githooks/pre-push](/workspace/02-projects/incubation/openprecedent/.githooks/pre-push)

It currently prevents two high-value failure modes:

- pushing without a `.codex-review` note
- pushing more commits to a branch that already has a merged PR

These checks are important because both failure modes happened during MVP work and are exactly the kind of procedural drift an agent will repeatedly fall into without explicit guardrails.

### 3. CI and merge validation guardrails

The repository already has:

- unit/regression CI through [python-ci.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/python-ci.yml)
- Markdown structure checks through [markdownlint.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/markdownlint.yml)
- issue/task closure sync validation and review gating through [pr-review-gate.yml](/workspace/02-projects/incubation/openprecedent/.github/workflows/pr-review-gate.yml)
- documented merge-time validation expectations in [merge-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/merge-validation.md)

This means the harness already enforces:

- code must still pass tests
- docs and PM artifacts must stay lint-clean
- issue-linked PRs must update the matching task twin correctly

### 4. Standard repository-local E2E validation

The repository already has a standard E2E script:

- [run-e2e.sh](/workspace/02-projects/incubation/openprecedent/scripts/run-e2e.sh)

That script is meaningful because it packages the full fixture-backed OpenClaw MVP journey into one reproducible command:

- session discovery
- collection
- manual import
- decision extraction
- replay
- precedent lookup
- fixture evaluation
- collected-session evaluation

This is one of the most mature parts of the current harness.

### 5. Real runtime validation history

The repository is not limited to synthetic tests.
It already contains durable records of live OpenClaw integration validation:

- [openclaw-full-user-journey-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-full-user-journey-validation.md)
- [openclaw-real-runtime-decision-lineage-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-real-runtime-decision-lineage-validation.md)
- [openclaw-runtime-decision-lineage-trigger-rerun.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-runtime-decision-lineage-trigger-rerun.md)

This is important because the most valuable bugs in MVP work were not found by unit tests alone.
They were found by putting the system back through the live OpenClaw loop.

### 6. Research-phase framing

The repository now explicitly documents that it has moved into a post-MVP research validation phase:

- [mvp-status.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-status.md)
- umbrella issue `#100`

This matters because it keeps later work from being misread as unfinished MVP plumbing.

## What Actually Went Wrong During MVP Development

The missing capabilities are easier to see if they are grounded in real failure patterns from MVP work.

### 1. Task, issue, and PR state drift happened repeatedly

Real examples from the MVP process included:

- task files not marked correctly when the linked issue was effectively done
- PR body linked to the wrong issue
- documentation-style closure work and umbrella-style open issues needing different handling
- attempts to continue work from a branch whose PR had already merged

Some of this is now partially guarded, but the harness still relies on conventions that are not represented explicitly enough in the PM model.

### 2. Small non-product failures consumed too much iteration time

During MVP work, several CI failures were not substantive product regressions.
They were recurring repository hygiene failures such as:

- extra blank lines in Markdown task files
- local task / PR body mismatch
- forgetting to update task status

These are low-value errors.
They still cost time because the harness catches them late and with too much manual triage.

### 3. Live runtime validation remained too manual

The fixture-backed E2E path is strong.
The live OpenClaw path is not yet as productized.

The MVP process still required manual steps for:

- launching isolated runtime profiles
- injecting the correct shared runtime environment
- copying or checking installed skill content
- running the right prompt
- locating the right session transcript
- checking invocation logs and semantic brief effects

This worked, but it remained operator-heavy instead of harness-driven.

### 4. Long-running development state was too easy to lose

One persistent friction point was not writing code.
It was preserving context such as:

- what had already been validated
- which live session proved which claim
- which issue was current
- which remaining gaps were product questions versus plumbing questions

Codex works well inside a single well-bounded turn.
It works less well when critical project memory is not stored in a stable, issue-scoped form.

### 5. Research work and implementation work were too easy to mix

By the time MVP core-loop engineering was complete, many later tasks had shifted into:

- impact validation
- retrieval quality evaluation
- extraction quality evaluation
- research-governance work

The repository eventually corrected this by documenting the post-MVP research phase and creating umbrella issue `#100`, but the harness still lacks dedicated support for research-shaped work.

## Missing Harness Capabilities

The following capabilities are still missing or underdeveloped.

### 1. Explicit issue and task types

The current PM flow does not yet model distinctions such as:

- implementation
- docs
- research
- umbrella

That missing type system is the main reason the harness still needs manual judgment for questions like:

- should this issue close with the PR
- should this task stay open long-term
- is this a delivery task or a parent framing artifact

Follow-up issue:

- `#103` Add issue and task types to the Codex PM workflow

### 2. One local preflight entrypoint

The harness still makes agents assemble the final local confidence check from multiple habits and commands.
It should expose one preflight command that catches the common avoidable failures before push.

Follow-up issue:

- `#108` Add a unified agent preflight script for local harness checks

### 3. A productized live runtime validation harness

The repository needs a smoother live validation entrypoint for integration work that goes beyond fixture-backed E2E.
This should reduce dependence on manually reassembled shell sequences and terminal memory.

Follow-up issue:

- `#104` Productize a live OpenClaw validation harness for runtime integration work

### 4. Research-specific workflow support

The current PM and skill layer is stronger for implementation tracking than for research tracking.
The harness should provide a structured way to express:

- the hypothesis
- the method
- the artifact
- the success/failure interpretation

Follow-up issue:

- `#105` Add a research-harness skill and experiment templates for hypothesis-driven work

### 5. CI failure triage support

The repository has checks, but it still lacks a smooth local helper for classifying routine CI failures quickly.
That missing layer creates unnecessary repeated debugging work for failures that are often predictable.

Follow-up issue:

- `#107` Add CI failure triage tooling for the agent development harness

### 6. Issue-scoped development state capture

The harness still needs a lightweight mechanism for keeping important development and validation state attached to ongoing work.
This is especially important for long-running, research-heavy, or live-runtime-heavy issue streams.

Follow-up issue:

- `#106` Capture issue-scoped development state for long-running agent work

## Overall Assessment

The current harness is already strong enough to support meaningful agent-driven product work.
That is a real achievement.

It already gives the repository:

- better process discipline than a normal small codebase
- a reproducible repository-local validation baseline
- a real runtime validation path
- a documented post-MVP research phase

But it is still not the final form of a high-autonomy Codex development environment.

Today, the harness is best described as:

- good at preventing obvious process drift
- moderately good at validating repository-local behavior
- good enough to support real product iteration
- still too manual around live runtime validation, long-running memory, and research workflow structure

## Recommended Next Step

The right next step is not one giant harness rewrite.
It is to improve the harness as a set of small, auditable issues tied to the actual failure modes uncovered during MVP work.

That work is now represented by:

- umbrella framing issue: `#100`
- harness improvement issues: `#103`, `#104`, `#105`, `#106`, `#107`, `#108`

This document should be treated as the baseline capability analysis for that next phase.
