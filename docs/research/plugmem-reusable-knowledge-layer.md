# PlugMem Follow-Up: A Reusable-Knowledge Layer Above Cases

Chinese version: [在 case 之上增加更明确的 reusable-knowledge layer](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem-reusable-knowledge-layer.md)

Main analysis: [PlugMem And OpenPrecedent](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem-openprecedent-analysis.md)

## Purpose

Focus on one design question raised by PlugMem:

Should OpenPrecedent introduce a reusable-knowledge layer that sits above raw event history and is not identical to the case object?

## Why This Matters

OpenPrecedent currently gets several benefits from the case as its main object:

- replay
- explanation
- evidence lineage
- historical narrative

But the case is also a large and heterogeneous unit.
For runtime reuse, it may be too coarse.

PlugMem suggests that reusable memory should be structured around compact knowledge units rather than around long historical episodes.

## Current OpenPrecedent Position

OpenPrecedent already distinguishes:

- `event` as process evidence
- `decision` as reusable judgment

That means the product already contains the first half of a knowledge-centric memory design.
What it does not yet have is a clearly modeled reusable-knowledge layer that can be retrieved independently of the case as the top-level runtime object.

## Candidate Shape

If OpenPrecedent adds such a layer, it should probably not be a generic memory blob.
More plausible reusable units would look like:

- stable factual knowledge distilled from repeated cases
- reusable constraints that often recur in similar work
- reusable rejected options that should not be re-explored blindly
- reusable authority boundaries
- reusable prescriptive guidance grounded in prior successful decisions

Each unit should remain linked to:

- supporting decisions
- supporting cases
- supporting events

So replay and audit are preserved.

## Why This Is Better Than Reusing Cases Directly

Case retrieval is still useful, but case reuse forces runtime retrieval to pay for:

- narrative bulk
- mixed evidence types
- background detail that may matter for replay but not for current action

A reusable-knowledge layer could let OpenPrecedent keep case-level replay while retrieving smaller, more decision-relevant units during live work.

## Main Risks

The main risks are:

- inventing knowledge units that are too abstract to audit
- duplicating information already stored in decisions without adding retrieval value
- losing repository- and case-specific context too early
- introducing a generic “memory store” layer that weakens product focus

## Research Questions

- which reusable units are stable enough to survive beyond one case
- which units should be materialized explicitly versus derived on retrieval
- whether the knowledge layer should be built from repeated patterns across cases or from single-case distilled outputs
- how to keep each unit tightly linked to evidence

## Likely Next Moves

- treat this as a research design question before a schema refactor
- test a few candidate knowledge-unit shapes against real retrieval cases
- measure whether knowledge-unit retrieval is more compact and useful than case-centered retrieval in runtime briefs

## Bottom Line

OpenPrecedent should likely preserve the case as the replay unit, but it should seriously investigate a reusable-knowledge layer above cases for runtime reuse.
This is one of the strongest PlugMem-inspired directions because it extends OpenPrecedent's current architecture without discarding its audit strengths.
