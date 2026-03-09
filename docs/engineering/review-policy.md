# Review Policy

## Goal

OpenPrecedent should maintain high confidence in both code and documentation changes.

This repository uses a layered review approach:

- human review for product, architecture, and behavior
- automated review for code quality and consistency
- lint-style checks for documentation hygiene

## Human Review

Human review remains mandatory for:

- product-facing behavior changes
- schema changes
- replay and decision logic changes
- retrieval logic changes
- architecture and storage changes
- major documentation changes

Codex can be used as a review agent for:

- code review
- PR review
- design review
- documentation review
- regression and testing gap review

## Recommended Automated Review Tools

### CodeFactor

Recommended as a baseline code quality reviewer.

Why:

- widely installed on GitHub
- low-friction quality feedback
- useful for continuous repository hygiene

### CodeAnt AI

Recommended as an AI-assisted PR review layer.

Why:

- strong PR-oriented review workflow
- can surface quality and security concerns
- useful for early-stage repositories that change quickly

## Recommended Documentation Review Tools

### Vale

Recommended for writing quality, terminology, and style consistency.

### markdownlint

Recommended for Markdown structure consistency.

## Suggested Policy

Minimum review expectation for normal changes:

1. author opens PR from fork
2. automated checks run
3. at least one human review is completed
4. PR is merged only after comments are resolved

## Initial Rollout

Phase 1:

- use Codex for manual review
- add markdownlint or Vale

Phase 2:

- add CodeFactor
- add CodeAnt AI

Phase 3:

- convert stable review rules into required checks

## Important Constraint

Automated review tools should assist review, not replace product and design judgment.

OpenPrecedent's core risk is not only code quality. It is also whether the system preserves correct decision semantics, explanation quality, and precedent value.
