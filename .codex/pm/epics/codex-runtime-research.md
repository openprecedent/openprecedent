---
type: epic
slug: codex-runtime-research
title: Codex runtime research
status: backlog
prd: decision-lineage-refocus
parent_issue: 100
---

## Outcome

Use Codex as a second, research-only runtime so OpenPrecedent can gather dense real development history, derive semantic decision lineage from it, and later test whether that lineage is reusable in a new project.

## Scope

- define the Codex-specific minimal integration boundary
- ingest and normalize Codex session history into replayable cases and events
- extract semantic decision lineage from Codex development sessions
- validate precedent quality on Codex real history
- expose a minimal Codex-facing runtime workflow for decision-lineage retrieval
- run a later real-project validation to determine whether Codex-derived lineage helps satisfy the research exit criteria in issue `#100`

## Acceptance Criteria

- the epic contains task files for the full Codex minimal integration path
- the Codex work is explicitly scoped as research support rather than generic multi-runtime abstraction
- the final task in the chain is a real-project validation that feeds evidence back into issue `#100`

## Child Issues

- `#125` Define the Codex runtime integration boundary for research-only minimal support
- `#126` Import Codex session history into OpenPrecedent as replayable cases and events
- `#127` Model Codex-specific event normalization and noise stripping
- `#128` Extract semantic decision lineage from Codex development sessions
- `#129` Validate precedent retrieval quality on Codex real development history
- `#130` Encapsulate OpenPrecedent as a Codex-facing minimal runtime workflow
- `#131` Validate Codex real-project decision-lineage reuse across project development
- `#163` Research contamination controls for decision-lineage retrieval

## Notes

This epic is intentionally narrow.
Its purpose is to generate research evidence for issue `#100`, not to introduce a generalized adapter framework for arbitrary agents.
