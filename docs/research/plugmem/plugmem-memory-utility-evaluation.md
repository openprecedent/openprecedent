# PlugMem Follow-Up: Memory Utility Versus Context Cost

Date: 2026-03-17

Chinese version: [引入 memory utility / context cost 评价视角](/workspace/02-projects/incubation/openprecedent/docs/zh/research/plugmem/plugmem-memory-utility-evaluation.md)

Main analysis: [PlugMem And OpenPrecedent](/workspace/02-projects/incubation/openprecedent/docs/research/plugmem/plugmem-openprecedent-analysis.md)

## Purpose

Explore how OpenPrecedent should evaluate runtime memory not only by retrieval success, but by the decision value it delivers relative to the context it consumes.

## Why This Matters

PlugMem emphasizes a practical principle:

- useful memory is not the memory that stores the most
- useful memory is the memory that delivers the most decision-relevant value per unit of context

This matters for OpenPrecedent because runtime briefs already compete for scarce context budget.

## Current OpenPrecedent Position

OpenPrecedent currently evaluates runtime memory through signals such as:

- was lineage invoked
- were matched cases empty or non-empty
- did the retrieved material influence the task
- did contamination appear

These are valuable, but they still leave out a key dimension:

- how efficient the retrieved memory was

## What A Utility Lens Would Ask

A stronger evaluation framework would ask:

- how much of the brief was actually used
- how much of the brief was redundant
- how much context did the brief consume
- how much of the final decision can be traced back to the brief
- whether a shorter brief could have produced the same effect

## Why This Is Hard

Memory utility is harder to measure than hit rate because:

- a brief may influence framing without being quoted explicitly
- some useful memory prevents bad choices rather than producing visible new work
- some long briefs may still be efficient if they prevent expensive mistakes

So this likely needs mixed evaluation:

- structured fields
- human judgment
- downstream outcome comparison

## Candidate Metrics

Possible evaluation directions:

- ratio of brief items that were later reflected in the resulting change
- proportion of retrieved units judged decision-relevant by a reviewer
- brief token count versus number of adopted constraints or decisions
- number of irrelevant or unused retrieved items per successful round

## Relation To Current Research

This is a natural extension of OpenPrecedent's current phase-two work.
The repository is already asking:

- was retrieval invoked
- was it useful
- was it contaminated

The utility lens adds:

- was it efficient

That is especially important if OpenPrecedent eventually retrieves smaller knowledge units instead of whole-case context.

## Likely Next Moves

- start with lightweight human-reviewed utility scoring on real runtime briefs
- compare a few successful and unsuccessful rounds for context efficiency
- avoid over-formalizing the metric before enough real examples exist

## Bottom Line

OpenPrecedent should eventually evaluate memory utility, not only retrieval presence or match quality.
This is one of the most important PlugMem-inspired upgrades because it changes the question from “did memory show up” to “was memory worth the context it cost.”
