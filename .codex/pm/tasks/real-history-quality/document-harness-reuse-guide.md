---
type: task
epic: real-history-quality
slug: document-harness-reuse-guide
title: Document the current OpenPrecedent harness and how to reuse it in other repositories
status: done
task_type: docs
labels: docs,ops
issue: 123
---

## Context

OpenPrecedent now has a meaningful harness across PM workflow, local guardrails, preflight, repository-local validation, live runtime validation, and research support.
That capability is distributed across many files, which makes reuse too dependent on repository memory.

## Deliverable

Add one engineering document that inventories the current harness and explains how to reuse or transplant it into another existing repository or a new repository.

## Scope

- summarize the current harness by capability layer
- distinguish OpenPrecedent-specific parts from broadly reusable patterns
- document export paths for existing repositories and new repositories
- keep the output in `docs/engineering/`

## Acceptance Criteria

- one engineering doc can serve as the current harness inventory
- the doc explains how to export the harness to another repository with reasonable effort
- reusable patterns are separated from product-specific logic

## Validation

- `.venv/bin/pytest tests/test_cli.py -k 'harness_reuse_guide_exists'`

## Implementation Notes

This document should complement the existing harness analysis rather than duplicate its MVP retrospective framing.
