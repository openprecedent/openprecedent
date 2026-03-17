---
type: issue_state
issue: 221
task: .codex/pm/tasks/codex-runtime-research/analyze-plugmem-and-knowledge-centric-agent-memory-against-openprecedent.md
title: Analyze PlugMem and knowledge-centric agent memory against OpenPrecedent
status: done
---

## Summary

Study PlugMem and the companion Microsoft Research memory blog as external research input for OpenPrecedent's current work on decision lineage, precedent retrieval, and reusable agent memory.

## Validated Facts

- PlugMem argues that raw trajectories should be transformed into reusable knowledge units rather than retrieved as verbose memory logs.
- OpenPrecedent already distinguishes raw event evidence from reusable decision lineage, making the paper directly relevant rather than merely adjacent.
- the external work also introduces design and evaluation claims that OpenPrecedent has not yet fully matched, especially around reusable knowledge units, task-agnostic transfer, and memory utility versus context cost.

## Open Questions

- where should OpenPrecedent keep its current case-level replay model versus move toward finer-grained reusable knowledge units
- whether OpenPrecedent should explicitly model fact-like versus prescriptive decision knowledge
- how much of PlugMem's task-agnostic memory framing is compatible with OpenPrecedent's current local-first, issue-scoped product direction

## Next Steps

- merge the expanded literature analysis so the external research comparison becomes durable repository context
- track the PlugMem research-note date metadata follow-up in issue `#223`
- track reusable-knowledge-layer follow-up research in issue `#224`
- track fact-versus-prescription follow-up research in issue `#225`
- track memory-utility-versus-context-cost follow-up research in issue `#226`
- track smaller-retrieval-unit follow-up research in issue `#227`

## Artifacts

- `docs/research/plugmem/plugmem-openprecedent-analysis.md`
- `docs/zh/research/plugmem/plugmem-openprecedent-analysis.md`
- `docs/research/plugmem/plugmem-reusable-knowledge-layer.md`
- `docs/zh/research/plugmem/plugmem-reusable-knowledge-layer.md`
- `docs/research/plugmem/plugmem-fact-vs-prescription.md`
- `docs/zh/research/plugmem/plugmem-fact-vs-prescription.md`
- `docs/research/plugmem/plugmem-memory-utility-evaluation.md`
- `docs/zh/research/plugmem/plugmem-memory-utility-evaluation.md`
- `docs/research/plugmem/plugmem-fine-grained-retrieval-units.md`
- `docs/zh/research/plugmem/plugmem-fine-grained-retrieval-units.md`
