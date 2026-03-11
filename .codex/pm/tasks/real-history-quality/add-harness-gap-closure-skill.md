---
type: task
epic: real-history-quality
slug: add-harness-gap-closure-skill
title: Add a harness-gap closure skill for repeated workflow failures
status: done
labels: docs,feature
issue: 142
---

## Context

Repeated workflow mistakes are often really harness gaps, but the repository does not yet have a reusable local skill that turns that signal into issue-scoped hardening work.

## Deliverable

Add a repository-local skill that guides Codex to diagnose, issue-track, implement, and regression-protect harness fixes.

## Scope

- define when a repeated workflow failure should be treated as a harness gap
- codify the issue-scoped hardening loop
- register the skill in repository guidance

## Acceptance Criteria

- the new skill is concise and reusable
- it requires issue linkage before harness code changes
- it covers diagnosis, implementation, tests or guardrails, and documentation follow-through

## Validation

- manual review of the skill against recent harness hardening issues such as `#133`, `#136`, and `#139`
