# Repository Governance

## Purpose

This document records the intended repository governance state for OpenPrecedent.

GitHub branch protection and repository settings are enforced outside Git history. This file exists so the expected rules are still reviewable and auditable inside the repository.

## Default Collaboration Model

OpenPrecedent uses a fork-and-pull-request workflow.

Expected model:

1. contributors work on branches in their own fork
2. contributors open pull requests into `openprecedent/openprecedent`
3. `main` is updated only through pull request merges

## Main Branch Protection

The intended protection state for `main` is:

- direct pushes are blocked
- force pushes are blocked
- branch deletion is blocked
- linear history is required
- conversation resolution is required before merge
- admins cannot bypass protection

## Review Requirements

The intended review state for `main` is:

- direct self-approval should not be required for admin-authored pull requests
- non-admin pull requests should still require review
- this is enforced through a custom required check instead of GitHub's native required approval rule

Current owner model:

- repository default owner: `@yaoyinnan`

## Required Checks

The intended required checks for `main` are:

- `markdownlint`
- `python-ci`
- `pr-review-gate`

These checks should remain required once the workflows are present on the default branch and stable.

## Local Review Guardrail

In addition to GitHub-side checks, the repository uses a local pre-push hook.

Expected local behavior:

- authors run a Codex review before push
- authors record the result in `.codex-review`
- the local pre-push hook blocks the push if the review note is missing

This is a local reliability measure, not a substitute for repository review requirements.

## Change Control

Changes to repository governance should follow this rule:

- repository content changes go through pull requests
- GitHub settings changes are applied directly by an admin
- any meaningful GitHub settings change should also be reflected in this document

## Review Gate Model

OpenPrecedent uses a custom review gate for pull requests:

- if the PR author is a repository admin, the review gate passes without a separate approval
- if the PR author is not a repository admin, at least one approval from another reviewer is required

This model is intended for the current stage of the project, where the repository may still have a single primary maintainer but should not require direct pushes to `main`.

## Bootstrap Exception

The first bootstrap PR may require temporary relaxation of required checks or review rules if the workflows or templates are being introduced in that same PR.

Once bootstrap changes are merged into `main`, the intended steady-state rules should be restored.
