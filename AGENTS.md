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
