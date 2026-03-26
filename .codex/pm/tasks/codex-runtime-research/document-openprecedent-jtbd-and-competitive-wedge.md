---
type: task
epic: codex-runtime-research
slug: document-openprecedent-jtbd-and-competitive-wedge
title: Document OpenPrecedent jobs-to-be-done, substitute solutions, and competitive wedge
status: done
task_type: research
labels: documentation,research
issue: 263
state_path: .codex/pm/issue-state/263-document-openprecedent-jtbd-and-competitive-wedge.md
---

## Context

OpenPrecedent's current repository positioning is decision replay and precedent reuse for agents, but the strongest user-facing product job is still being clarified.

Recent discussion in this repository has sharpened several important points:

- users do not want a generic replay database or memory store
- the likely primary job is action-time inheritance of prior judgment structure rather than post-hoc trace inspection alone
- the real competition includes not only tracing and memory tools, but also code search, PR and issue history, Slack and meeting notes, expert recall, and non-consumption
- some of the most important decision context lives outside the raw runtime transcript in human conversations and repository-specific exceptions

This issue exists to turn that product discussion into a durable repository artifact that can be revised across multiple later rounds instead of being lost in chat history.

## Deliverable

Create first-pass English and Chinese product discussion notes that capture OpenPrecedent's candidate jobs-to-be-done, substitute solutions, competitive wedge, and open questions about current versus future product direction.

## Scope

- document the primary and secondary user jobs OpenPrecedent may be hired to solve
- distinguish the current MVP's strongest validated job from the future product job that may be more competitive
- analyze substitute solutions, including non-consumption, observability, memory, code search, documentation, chat history, and human expert recall
- include the role of off-transcript decision context such as meetings, Slack, IM, and customer-specific exceptions
- add a Chinese companion note that stays aligned with the English canonical note
- position the document as a living note that later discussion rounds can refine rather than as a finalized strategy memo
- keep the output focused on product analysis, not implementation planning or organization-wide roadmap expansion

## Acceptance Criteria

- the repository contains a dedicated written note for this discussion under `docs/product/`
- the repository contains a Chinese companion note under `docs/zh/product/`
- the note states at least one candidate primary JTBD and explains why it should or should not be the wedge
- the note identifies substitute solutions and explains when users may choose them instead of OpenPrecedent
- the note distinguishes current validated product value from future target value
- the note ends with explicit open questions so later discussion rounds can iterate on it

## Validation

- read the English and Chinese notes and confirm they reflect the repository discussion about action-time decision support, substitute solutions, and off-transcript context loss
- verify the GitHub issue exists and the local task twin references it
- verify the note is framed as revisable and does not pretend the current analysis is final

## Implementation Notes

- Maintain one English canonical note in `docs/product/` and one aligned Chinese companion in `docs/zh/product/`.
- Prefer a high-signal structure: problem framing, candidate JTBDs, substitute solutions, why users would hire or not hire OpenPrecedent, and open questions.
- Treat this as a living product-analysis artifact that future issue-scoped follow-up edits can extend.
