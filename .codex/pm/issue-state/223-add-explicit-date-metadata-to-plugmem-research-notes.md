---
type: issue_state
issue: 223
task: .codex/pm/tasks/real-history-quality/add-explicit-date-metadata-to-plugmem-research-notes.md
title: Add explicit date metadata to PlugMem research notes and define a date-placement convention
status: in_progress
---

## Summary

Backfill explicit date metadata into the PlugMem research-note set and define a reusable repository convention for where research-note dates belong.

## Validated Facts

- the PlugMem note set now lives under `docs/research/plugmem/` and `docs/zh/research/plugmem/`
- the current documents do not yet show explicit date metadata at the top of each note
- the repository does not yet have a durable rule for research-note date placement

## Open Questions

- whether research-note date metadata should live in the directory index, in each document, or both

## Next Steps

- define the date-placement rule in `AGENTS.md`
- choose the document top as the canonical date location for this note set
- backfill the PlugMem English and Chinese notes with explicit dates
- run repository preflight and close the loop on `#223`

## Artifacts

- `AGENTS.md`
- `docs/research/plugmem/plugmem-openprecedent-analysis.md`
- `docs/research/plugmem/plugmem-reusable-knowledge-layer.md`
- `docs/research/plugmem/plugmem-fact-vs-prescription.md`
- `docs/research/plugmem/plugmem-memory-utility-evaluation.md`
- `docs/research/plugmem/plugmem-fine-grained-retrieval-units.md`
- `docs/zh/research/plugmem/plugmem-openprecedent-analysis.md`
- `docs/zh/research/plugmem/plugmem-reusable-knowledge-layer.md`
- `docs/zh/research/plugmem/plugmem-fact-vs-prescription.md`
- `docs/zh/research/plugmem/plugmem-memory-utility-evaluation.md`
- `docs/zh/research/plugmem/plugmem-fine-grained-retrieval-units.md`
