# Documentation Governance

Date: 2026-03-26
Status: Active

## Purpose

This document defines the repository-wide conventions for documentation chronology, canonical entrypoints, and lifecycle boundaries across `docs/` and `docs/zh/`.

The goal is not to force every document into a date-prefixed naming scheme.
The goal is to help readers answer three questions quickly:

1. where should I start reading in this directory
2. which document is the current canonical reference
3. which documents are drafts, historical notes, archived rounds, or supporting evidence

## Topic Tree First

OpenPrecedent documentation should be organized primarily by topic tree:

- `docs/product/`
- `docs/architecture/`
- `docs/research/`
- `docs/engineering/`

Time is still important, but it should usually be expressed through metadata and directory indexes rather than by encoding chronology only in filenames.

## Directory Entrypoints

Add a directory-level `README.md` when any of the following is true:

- the directory contains multiple documents and readers need a recommended entrypoint
- the directory contains both canonical and historical material
- chronology matters for interpreting the document set
- the directory has enough scope that file browsing alone is no longer clear

The `README.md` should explain:

- what the directory is for
- which document is the current recommended starting point
- which documents are current, historical, draft, or archival
- any chronology cues that matter for reading order

## Canonical Versus Historical Material

When a directory contains evolving material, the repository should distinguish between:

- canonical current docs
- draft or exploratory notes
- historical drafts
- archive or evidence logs

Use explicit wording such as:

- `Active`
- `Draft`
- `Historical draft`
- `Archive`
- `Observation log`
- `Closeout`

Do not expect readers to infer lifecycle state only from prose or old filenames.

## Date Metadata

Include explicit date metadata when chronology affects interpretation.
This is especially important for:

- research note sets
- evolving product discussion notes
- validation logs and closeouts
- historical drafts retained for reference

Repository-acceptable patterns include:

- `Date: YYYY-MM-DD`
- `日期：YYYY-MM-DD`
- structured document-info sections that include date and status

The key requirement is not one exact syntax.
The key requirement is that the date and lifecycle state are easy to find near the top of the document or in the directory index.

## Canonical Discussion Notes

For long-running discussion topics:

- keep one stable canonical note when a topic needs a continuously maintained current view
- avoid appending every future discussion round into the canonical note without restructuring
- when historical discussion rounds matter on their own, separate them from the canonical note through archive or round-specific material

Readers should not have to reverse-engineer chronology from a very long document alone.

## Chinese And English Trees

When English and Chinese documentation both exist:

- keep directory entrypoints aligned where practical
- keep chronology cues aligned across both trees
- make it explicit when one side is canonical and the other is a companion or retained original-language reference

## Current Repository Pattern

The current repository pattern should be:

- `docs/README.md` and `docs/zh/README.md` describe the top-level trees
- category directories such as `docs/product/`, `docs/architecture/`, `docs/zh/product/`, and `docs/zh/architecture/` use local `README.md` entrypoints when they contain multiple or mixed-lifecycle documents
- research directories continue to use dated indexes where chronology is part of the reading model

## Non-Goals

This convention does not require:

- date-prefixed filenames for every document
- a full static-site generator or Kubernetes-style website pipeline
- mechanically rewriting all legacy docs in one pass

The standard should stay lightweight enough for normal issue-scoped documentation work.
