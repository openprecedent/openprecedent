---
type: task
epic: codex-runtime-research
slug: research-contamination-controls-for-decision-lineage-retrieval
title: Research contamination controls for decision-lineage retrieval
status: backlog
task_type: research
labels: research
issue: 163
state_path: .codex/pm/issue-state/163-research-contamination-controls-for-decision-lineage-retrieval.md
---

## Context

OpenPrecedent has now validated that HarnessHub rounds can be exported, imported into the shared runtime, retrieved as matched cases, and reused in later live decision-lineage queries.

A separate research question is now visible and more concrete after `#220`: the current matcher and brief assembly may still allow partially related cases to contribute irrelevant constraints, success criteria, or cautions into the returned context.

Now that invocation reliability has been re-established under the current local setup, contamination and retrieval hygiene become more important than before.
The next question is no longer "will lineage trigger at all", but "when lineage triggers, how do we prevent weakly related context from polluting the returned brief".

## Deliverable

When prioritized, produce a research plan that compares contamination-control approaches for decision-lineage retrieval, identifies the smallest next experiment worth running, and clarifies how contamination should be evaluated now that `#220` has answered the invocation-reliability question positively.

## Scope

- capture the contamination-risk question without committing to immediate optimization
- preserve candidate directions such as typed memory, provenance-aware brief assembly, scoped retrieval, and graph or relation-aware memory
- capture sub-questions around adopted versus merely retrieved context, irrelevant constraints in assembled briefs, and how contamination should be measured per unit, per case, or per brief
- connect contamination risk to context-cost and brief-quality tradeoffs rather than treating it as a generic search-quality issue
- defer implementation until a concrete harmful failure or stronger product need is observed

## Acceptance Criteria

- the issue records the contamination-risk question and why it is not yet being optimized
- the issue records why contamination is now a more relevant next-step risk after `#220`
- the task preserves concrete sub-questions for future research rather than a vague "clean up retrieval" goal
- future work can pick this up without losing the current reasoning context
- the task does not commit the project to a graph or embedding redesign prematurely

## Validation

- verify the issue and local task twin preserve the current reasoning context
- verify the issue reflects the post-`#220` transition from invocation reliability to retrieval hygiene
- keep the task in backlog until concrete retrieval contamination failures are observed
