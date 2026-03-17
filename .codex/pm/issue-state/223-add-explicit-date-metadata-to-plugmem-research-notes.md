---
type: issue_state
issue: 223
task: .codex/pm/tasks/real-history-quality/add-explicit-date-metadata-to-plugmem-research-notes.md
title: Add explicit date metadata to PlugMem research notes and define a date-placement convention
status: done
---

## Summary

Backfill explicit date metadata into the current research note surface, add directory-level date indexes, and define a reusable repository convention for where research-note dates belong.

## Validated Facts

- the PlugMem note set now lives under `docs/research/plugmem/` and `docs/zh/research/plugmem/`
- the implemented convention places the research-note date directly under the document title
- the PlugMem English and Chinese note pairs now share explicit matching `2026-03-17` date metadata
- the older competitive-landscape research notes now also carry explicit `2026-03-09` document dates
- the research directories now expose date information through `README.md` indexes
- `AGENTS.md` now records the repository rule for research-note date placement

## Open Questions

- whether older research notes outside the PlugMem set should be backfilled under the same rule
- how aggressively to backfill date metadata beyond the current research surface

## Next Steps

- open and merge the issue-scoped PR for `#223`

## Artifacts

- `AGENTS.md`
- `docs/research/README.md`
- `docs/zh/research/README.md`
- `docs/research/plugmem/README.md`
- `docs/zh/research/plugmem/README.md`
- `docs/research/competitive-landscape.md`
- `docs/zh/research/context-graph-competitive-landscape.md`
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
