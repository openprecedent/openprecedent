---
type: issue_state
issue: 240
task: .codex/pm/tasks/codex-runtime-research/study-hybrid-semantic-plus-passive-capture-architecture-beyond-explicit-cli-triggered-invocation.md
title: Study hybrid semantic-plus-passive capture architecture beyond explicit CLI-triggered invocation
status: backlog
---

## Summary

Preserve a future research direction for hybrid semantic-plus-passive capture without treating passive observation, eBPF, or similar techniques as near-term implementation work.

## Validated Facts

- current explicit semantic capture has already been validated across multiple real HarnessHub task classes
- passive capture may become relevant later for observability or miss-reduction questions
- there is not yet enough evidence to justify the complexity cost of introducing passive capture technology

## Open Questions

- which misses are truly observability problems rather than workflow-composition problems
- which passive signals would improve lineage reconstruction rather than only generate low-value telemetry noise
- whether a later hybrid design could preserve semantic capture as the primary signal while adding targeted passive support

## Next Steps

- keep this issue behind the current quality and explainability research
- only revisit it after the nearer-term issues have clarified whether observability gaps remain a major bottleneck

## Artifacts

- `.codex/pm/tasks/codex-runtime-research/study-hybrid-semantic-plus-passive-capture-architecture-beyond-explicit-cli-triggered-invocation.md`
- `.codex/pm/tasks/codex-runtime-research/frame-long-horizon-capture-and-storage-research-after-issue-220.md`
