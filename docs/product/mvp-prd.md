# OpenPrecedent MVP PRD

## Status

- status: shipped MVP v1
- core-loop status date: `2026-03-10`
- repository summary: [mvp-status.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-status.md)
- implementation boundary: [mvp-design.md](/workspace/02-projects/incubation/openprecedent/docs/architecture/mvp-design.md)
- completion roadmap: [mvp-roadmap.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-roadmap.md)

## Current Outcome

The MVP described in this PRD is no longer a planned target only.
As of `2026-03-10`, the core loop is implemented and validated in the repository's OpenClaw-first local environment:

1. capture a case
2. store the ordered event timeline
3. extract decision records
4. replay and explain decisions
5. retrieve similar precedent

What remains after this point is post-MVP validation and quality work rather than unfinished core-loop engineering.

## MVP Anchor

The first MVP is anchored on a local single-agent runtime such as OpenClaw.

The minimal product loop is:

1. a user starts a task
2. the agent executes through messages, tools, commands, and file operations
3. the system captures the full event stream
4. the system extracts key decisions
5. the user replays and explains the case
6. the system returns similar precedent from history

## Goals

- capture a full case timeline
- extract high-value decision nodes
- replay both raw execution and structured decisions
- explain decisions with evidence binding
- retrieve similar historical cases

## Non-Goals

- multi-agent coordination
- a full enterprise control plane
- a generic graph platform
- fully automated decision optimization
- broad workflow orchestration

## Core User Value

- understand what the agent did
- understand why a decision happened
- identify where a decision went wrong
- reuse historical precedent in similar cases

## Scope

In scope:

- single local agent instance
- case-level event capture
- decision extraction
- replay
- explanation
- precedent retrieval

Out of scope:

- organization-wide governance
- complex approval workflows
- broad third-party connector coverage
- cross-case graph analytics

## Success Criteria

- case capture is reliable
- decision explanations are evidence-backed
- replay is useful for real post-hoc review
- precedent retrieval returns helpful historical cases

## Post-MVP Boundary

The next stage should focus on:

- measuring whether runtime precedent usage improves downstream task quality
- improving extraction and retrieval quality on a broader real-history corpus
- deciding whether to deepen OpenClaw-specific quality work or validate a second runtime

Those are important, but they are no longer prerequisites for calling the MVP core loop complete.
