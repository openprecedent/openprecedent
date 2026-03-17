---
type: task
epic: real-history-quality
slug: add-explicit-date-metadata-to-plugmem-research-notes
title: Add explicit date metadata to PlugMem research notes and define a date-placement convention
status: done
task_type: implementation
labels: docs
issue: 223
state_path: .codex/pm/issue-state/223-add-explicit-date-metadata-to-plugmem-research-notes.md
---

## Context

The PlugMem analysis from `#221` now lives in dedicated English and Chinese subdirectories under `docs/research/plugmem/` and `docs/zh/research/plugmem/`, but the documents still lack explicit date metadata.

Because these research notes may be linked and read individually, the repository needs a durable rule for where research-note dates belong. The current research surface also needs directory-level date indexing so later readers can track chronology without opening every file.

## Deliverable

Define a repository-level date-placement convention for research notes and apply it to the current research document surface, including PlugMem and the pre-existing competitive-landscape notes.

## Scope

- add a durable documentation rule for research-note date metadata
- choose a single placement convention for note dates
- add directory-level research indexes with date information
- backfill explicit date metadata into the PlugMem English and Chinese documents
- backfill explicit date metadata into the pre-existing competitive-landscape research documents
- update the local PM state for issue `#223`

## Acceptance Criteria

- `AGENTS.md` defines where research-note date metadata belongs
- the active research directories expose date information at the directory level
- every PlugMem note under `docs/research/plugmem/` includes explicit date metadata
- every PlugMem note under `docs/zh/research/plugmem/` includes matching explicit date metadata
- the current non-PlugMem research notes also include explicit date metadata
- the date placement is consistent across the indexed English and Chinese research note set

## Validation

- run `./scripts/run-agent-preflight.sh`
- verify the research directories show dated indexes
- verify the current research note set shows explicit dates directly under the title in both languages

## Implementation Notes

- use the document top, directly below the title, as the canonical date placement
- use `README.md` as the directory-level research index when a directory needs chronology tracking
- keep the English and Chinese dates identical for the same note pair
