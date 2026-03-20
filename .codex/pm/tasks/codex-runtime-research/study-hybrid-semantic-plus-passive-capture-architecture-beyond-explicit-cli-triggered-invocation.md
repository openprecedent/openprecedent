---
type: task
epic: codex-runtime-research
slug: study-hybrid-semantic-plus-passive-capture-architecture-beyond-explicit-cli-triggered-invocation
title: Study hybrid semantic-plus-passive capture architecture beyond explicit CLI-triggered invocation
status: backlog
task_type: research
labels: research
issue: 240
state_path: .codex/pm/issue-state/240-study-hybrid-semantic-plus-passive-capture-architecture-beyond-explicit-cli-triggered-invocation.md
---

## Context

OpenPrecedent currently records high-value decision-lineage context through explicit agent-triggered semantic invocation.

That approach has now been validated across multiple real HarnessHub task classes, but it still depends on the agent or local workflow choosing to enter the lineage path.
This creates a legitimate long-horizon research question:
should OpenPrecedent eventually add a passive observation layer, such as process-level or system-level telemetry, to complement explicit semantic capture?

This question is worth preserving for later study, but it is not ready for immediate implementation.
Before adopting eBPF or similar lower-level capture techniques, the project needs stronger answers about:

- which misses are actually caused by insufficient observability rather than workflow composition
- which passive signals would improve later decision-lineage reconstruction
- what noise, privacy, portability, and complexity costs such capture would introduce

## Deliverable

Produce a research framing issue for a future study of hybrid semantic-plus-passive capture architecture.

## Scope

- evaluate passive observation as a possible complement to explicit semantic capture, not an automatic replacement
- focus on future research questions rather than a migration or implementation plan
- define the unanswered product questions that would need to be resolved before introducing eBPF, system tracing, or similar mechanisms
- keep the issue explicitly behind the current near-term research stack of `#163`, `#235`, `#236`, `#237`, `#226`, `#225`, `#227`, and `#224`

## Acceptance Criteria

- the issue clearly states why passive capture is interesting from a long-term architecture perspective
- the issue clearly states why the project should not adopt passive capture technology yet
- the issue identifies the minimum pre-research questions that must be answered before implementation becomes justified
- the issue preserves the principle that technology should be introduced to solve validated product problems rather than to pursue infrastructure novelty

## Validation

- verify the issue is labeled `research`
- verify the issue text explicitly says this is a future-direction study, not an active implementation plan
- verify the issue text explains that passive capture would add complexity unless it solves a demonstrated observability or recall problem

## Implementation Notes

Potential questions to answer later:

- which kinds of lineage misses would passive observation realistically reduce
- whether passive capture should collect system events, file/process events, or a narrower agent-runtime subset
- how passive low-level traces would map back to semantic decision records instead of only producing noisy event logs
- whether a hybrid design could preserve the strengths of semantic capture while improving observability for missed rounds
