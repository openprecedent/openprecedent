# OpenPrecedent MVP PRD

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
