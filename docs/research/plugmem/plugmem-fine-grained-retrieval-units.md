# PlugMem Follow-Up: Smaller Retrieval Units Without Losing Replay

Date: 2026-03-17

Chinese version: [引入小于 case 的 retrieval unit，同时保留 case-level replay](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem/plugmem-fine-grained-retrieval-units.md)

Main analysis: [PlugMem And OpenPrecedent](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem/plugmem-openprecedent-analysis.md)

## Purpose

Evaluate whether OpenPrecedent should retrieve units smaller than the case during runtime while preserving the case as the replay and audit object.

## Why This Matters

Today, OpenPrecedent's precedent model is still strongly case-centered.
That is good for explanation, but it may be too coarse for live reuse.

PlugMem suggests that memory retrieval becomes more useful when the retrieval unit is closer to reusable knowledge than to a full historical episode.

## Current OpenPrecedent Tension

The current design serves two different jobs:

1. replay the full history of a decision
2. surface compact guidance during a live task

These jobs do not necessarily need the same retrieval unit.
The case is excellent for the first job.
It may be suboptimal for the second.

## Candidate Smaller Units

Likely smaller units include:

- one reusable constraint
- one reusable rejected option
- one authority boundary
- one distilled decision judgment
- one stable factual statement

These units do not replace the case.
They provide a more focused access path into the case's reusable contents.

## Why Smaller Units Could Help

Smaller retrieval units could:

- reduce irrelevant narrative baggage
- improve retrieval precision
- make runtime briefs more compact
- support stronger ranking than “which whole case is most similar”

They could also let OpenPrecedent mix evidence from multiple historical cases more naturally.

## Main Risks

- losing too much context when a unit is detached from its case
- returning fragments that are individually true but misleading without their original boundary conditions
- making the product feel like a generic vector store instead of an evidence-grounded precedent system

## Research Questions

- which units are small enough to help but large enough to stay meaningful
- whether ranking small units improves runtime usefulness over case-centered ranking
- when the runtime should return units only versus units plus a supporting case reference
- how to preserve replayability and audit while compressing retrieval

## Likely Next Moves

- experiment first at the retrieval and brief-construction layer
- compare case-centered and unit-centered runtime briefs on the same tasks
- preserve supporting case references in every returned unit so replay is never lost

## Bottom Line

OpenPrecedent should probably keep the case as the replay unit, but it should not assume the case must remain the only runtime retrieval unit.
This is one of the clearest product-design questions raised by PlugMem for OpenPrecedent's next phase.
