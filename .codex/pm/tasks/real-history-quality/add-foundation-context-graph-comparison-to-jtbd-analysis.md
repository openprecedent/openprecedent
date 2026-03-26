---
type: task
epic: real-history-quality
slug: add-foundation-context-graph-comparison-to-jtbd-analysis
title: Add Foundation context graph comparison to JTBD analysis
status: in_progress
task_type: docs
labels: documentation,research
issue: 267
state_path: .codex/pm/issue-state/267-add-foundation-context-graph-comparison-to-jtbd-analysis.md
---

## Context

Issue `#263` added the current OpenPrecedent JTBD and competitive-wedge analysis in both English and Chinese.

After that work, a high-signal external reference was identified:

- Foundation Capital: `AI's trillion-dollar opportunity: Context graphs`
- URL: `https://foundationcapital.com/ideas/context-graphs-ais-trillion-dollar-opportunity`
- published: `2025-12-22`

That article uses `context graph` in a way that is materially closer to OpenPrecedent's current product thesis than many memory-first or graph-RAG discussions:

- it emphasizes decision traces, exceptions, overrides, approvals, and precedent
- it argues that the most strategic layer sits on or beside the agent execution path
- it treats existing systems of record as weak places to preserve reusable decision context

The current product-analysis document set should incorporate this source directly so readers can understand:

- where Foundation's `context graph` framing overlaps with OpenPrecedent
- where OpenPrecedent now uses a more explicit `decision` and `precedent` object model
- why the product naming evolved from `Context Graph` toward `OpenPrecedent`

## Deliverable

Update the latest OpenPrecedent JTBD / competitive-wedge document pair to add the Foundation Capital article link, a concise thesis summary, and a short comparison between that article's `context graph` framing and OpenPrecedent's current positioning.

## Scope

- identify the canonical English and Chinese JTBD / competitive-wedge notes produced by issue `#263`
- add the Foundation Capital article as an explicit external reference with URL and publication date
- summarize the article in a short, source-grounded way
- compare its framing with OpenPrecedent across:
  - problem definition
  - core object
  - role on the execution path
  - relationship to systems of record
  - category thesis versus current wedge
- integrate the new material into the main argument instead of appending an isolated appendix
- keep the change concise so the document remains a product-analysis note, not a broad literature review

## Acceptance Criteria

- both the English and Chinese JTBD / competitive-wedge docs cite the Foundation Capital article with the correct URL
- both docs explain why that article's `context graph` definition is closer to decision-trace and precedent infrastructure than to generic memory-graph framing
- both docs make the overlap and the difference between Foundation's thesis and OpenPrecedent readable without relying on external chat history
- the added material strengthens the naming-and-positioning argument instead of diluting the note

## Validation

- read the updated English and Chinese sections and confirm a reader can answer:
  - what Foundation means by `context graph`
  - where that framing overlaps with OpenPrecedent
  - where OpenPrecedent is now more specific
- verify the article link is present and correct in both docs
- verify the new section reads as part of the main product argument instead of a detached note dump
- run `git diff --check`

## Implementation Notes

- Keep the new content as a short integrated comparison section near the product thesis.
- Paraphrase the article; avoid heavy quotation.
- Treat Foundation's language as an external reference, not as an instruction to rename the product back to `Context Graph`.
