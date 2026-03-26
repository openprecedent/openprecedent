---
type: task
epic: real-history-quality
slug: establish-repository-wide-doc-chronology-and-entrypoints
title: Establish repository-wide documentation chronology and canonical entrypoint conventions
status: in_progress
task_type: docs
labels: documentation
issue: 265
state_path: .codex/pm/issue-state/265-establish-repository-wide-doc-chronology-and-entrypoints.md
---

## Context

The repository already has meaningful documentation categories under `docs/`, including architecture, engineering, product, research, and Chinese companion trees.
However, the current documentation surface still has a navigation and chronology problem:

- readers often cannot tell the creation or revision order of related documents from names alone
- long-lived discussion notes can grow by accretion and become harder to scan as "current canonical view" versus "historical discussion trail"
- some directories have a clear local entrypoint while others rely on file browsing and implicit naming
- date metadata and chronology cues exist in some note sets but not as a repository-wide convention

The goal is not to force every document into date-prefixed filenames.
The stronger goal is to make the `docs/` tree easier to navigate by giving readers explicit entrypoints, chronology cues, and lifecycle boundaries.

Recent review of Kubernetes documentation practices suggests a useful direction:

- organize primarily by topic tree rather than by time-stamped filename alone
- use explicit metadata and directory-level entrypoints to signal order and canonical reading paths
- separate "current canonical documentation" from historical or versioned material instead of letting one file silently absorb every discussion round

OpenPrecedent should adopt a repository-scaled version of that idea for the full `docs/` tree rather than treating this only as a product-doc issue.

## Deliverable

Define and document a repository-wide documentation convention for chronology, canonical entrypoints, and lifecycle boundaries across `docs/` and `docs/zh/`, then apply the minimal structural updates needed so readers can tell where to start and how to interpret document age and status.

## Scope

- audit the top-level documentation categories under `docs/` and `docs/zh/` for missing entrypoints, chronology cues, and inconsistent date or status metadata
- define a repository convention for directory-level indexes or README entrypoints where chronology or reading order matters
- define how evolving discussion docs should distinguish current canonical notes from archived rounds, drafts, or superseded material
- define the minimum metadata expected for documents that need chronology tracking, such as date, status, and document type
- update the relevant repository documentation rules so later contributors can follow one consistent pattern
- make only the smallest structural doc edits needed to demonstrate the convention on the current tree
- keep the work focused on documentation governance and information architecture rather than broader product or implementation planning

## Acceptance Criteria

- the repository has an explicit documented convention for chronology and canonical entrypoints across the `docs/` tree
- readers can tell from repository docs how canonical documents differ from archived, draft, or round-based discussion material
- directories that need chronology tracking or a recommended reading path have a clear local entrypoint
- the convention applies to both English and Chinese documentation trees where parallel materials exist
- the resulting approach improves `docs/` discoverability without forcing every file into date-prefixed naming

## Validation

- read the updated documentation-governance guidance and confirm it explains chronology, canonical entrypoints, and lifecycle boundaries clearly
- inspect the affected `docs/` and `docs/zh/` directories and confirm a reader can tell where to start and how to interpret document order or status
- verify the chosen convention does not conflict with existing repository documentation rules about naming, Chinese translation, and research-note date metadata

## Implementation Notes

- Prefer a topic-tree plus explicit metadata approach over a filename-only chronology scheme.
- Reuse existing directory `README.md` entrypoints where that pattern already exists or fits naturally.
- Keep the convention lightweight enough that future issue-scoped documentation updates can follow it without large mechanical overhead.
- Consider Kubernetes documentation organization as a reference pattern for topic-first structure, explicit entrypoints, and metadata-driven ordering, but adapt it pragmatically to this repository rather than copying its full site-generation model.
