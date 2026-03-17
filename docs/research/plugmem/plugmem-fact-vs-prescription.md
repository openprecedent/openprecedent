# PlugMem Follow-Up: Fact-Like Versus Prescriptive Knowledge

Chinese version: [在 decision lineage 中区分事实型知识与处方式知识](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem/plugmem-fact-vs-prescription.md)

Main analysis: [PlugMem And OpenPrecedent](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem/plugmem-openprecedent-analysis.md)

## Purpose

Evaluate whether OpenPrecedent should explicitly distinguish fact-like reusable knowledge from prescriptive reusable knowledge inside its semantic decision model.

## Why This Matters

PlugMem separates:

- propositional knowledge
- prescriptive knowledge

That split matters because memory systems often fail when they blur:

- what is true
- what should be done

Those are both valuable, but they are not the same kind of reusable asset.

## Current OpenPrecedent Position

OpenPrecedent already has a semantic decision taxonomy, but it currently groups reusable judgment without clearly distinguishing:

- stable factual statements about the repository, environment, or operating context
- recommended or previously validated actions to take under similar conditions

This can make retrieval less precise because a brief may mix:

- facts
- constraints
- norms
- advice

without a clear internal boundary.

## Why A Split Could Help

An explicit split could improve:

- extraction quality
- retrieval precision
- runtime brief structure
- contamination control

This is especially plausible because prescriptive carryover is usually riskier than factual carryover.

## Example Distinction

Fact-like knowledge:

- the repository uses one issue per branch
- a runtime path is shared under a specific home
- a manifest field has a stable meaning

Prescriptive knowledge:

- use `initial_planning` before major implementation work
- avoid widening the task into a broad architecture rewrite
- treat merged-branch reuse as a guardrail violation

Both may appear in the same case, but they should not necessarily be stored, ranked, or surfaced the same way.

## Risks

- over-modeling the distinction too early
- forcing borderline items into rigid categories
- increasing extraction complexity before evaluation catches up

## Research Questions

- should this be a taxonomy split, a metadata split, or only a retrieval-time distinction
- which current semantic decision types are mostly fact-like versus mostly prescriptive
- whether a fact/prescription split reduces contamination in runtime briefs

## Likely Next Moves

- test the split first in analysis or evaluation, not only in schema
- inspect real retrieved briefs and classify their contents into fact-like versus prescriptive units
- use that evidence to judge whether a formal taxonomy change is warranted

## Bottom Line

This distinction is one of the most plausible near-term improvements suggested by PlugMem.
It is narrower than a full memory redesign, but potentially high leverage for extraction quality, retrieval precision, and contamination control.
