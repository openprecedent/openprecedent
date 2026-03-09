# AGENTS.md

## Project

OpenPrecedent is an open decision replay and precedent layer for agents.

The first implementation target is a local single-agent workflow. The current goal is to validate this loop:

1. capture a case
2. store the event timeline
3. extract decision records
4. replay and explain decisions
5. retrieve similar precedent

## Repository Intent

- `docs/`: technical and operational documentation
- `src/`: implementation code
- `tests/`: automated tests
- `scripts/`: local tooling and setup helpers

## Working Rules

- Keep the scope focused on decision capture, replay, explanation, and precedent retrieval.
- Prefer small, auditable changes over broad scaffolding.
- Preserve a clear separation between raw events and derived decision records.
- Prefer simple local-first development flows.
- Once a PR branch has been merged, do not add new commits to that branch. Start a fresh branch from `upstream/main` for all follow-up work.
- Track agent development as GitHub issues broken down to the smallest deliverable unit that can be completed and reviewed independently.
- When an agent starts work on one issue, create a fresh branch from the latest `upstream/main` for that issue only.
- After completing one issue, open exactly one PR for that issue instead of batching multiple issues into the same PR.
- Link the PR to its issue in the PR body using a closing reference such as `Closes #24` so the issue is closed automatically when the PR is merged.
- After a PR is merged, continue the next task on a new branch and a new PR linked to the next issue.

## Documentation Rules

- Update docs when schemas, APIs, or core object models change.
- Keep naming consistent with `case`, `event`, `decision`, `artifact`, and `precedent`.
- Do not describe the project as a generic graph database, memory store, or trace viewer.

## Near-Term Priorities

- event schema
- decision schema
- replay API
- precedent retrieval
- local runtime integration
