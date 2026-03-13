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
- During discussion, planning, or taxonomy exploration, do not edit implementation code speculatively.
- Any implementation change to `src/`, `tests/`, or other product behavior must be tied to one explicit GitHub issue and completed only on that issue's dedicated branch.
- Once a PR branch has been merged, do not add new commits to that branch. Start a fresh branch from `upstream/main` for all follow-up work.
- Track agent development as GitHub issues broken down to the smallest deliverable unit that can be completed and reviewed independently.
- When an agent starts work on one issue, create a fresh branch from the latest `upstream/main` for that issue only.
- After completing one issue, open exactly one PR for that issue instead of batching multiple issues into the same PR.
- Link the PR to its issue in the PR body using a closing reference such as `Closes #24` so the issue is closed automatically when the PR is merged.
- After a PR is merged, continue the next task on a new branch and a new PR linked to the next issue.
- When running Python tests, do not stop at a missing global `pytest`; use `./scripts/run-pytest.sh` or the repository-local `.venv` resolution path first.

## Project-Local Codex Skill

- For project-management work in this repository, use the local skill at `.codex/skills/ccpm-codex/`.
- Use it for PRD, epic, task, issue, and PR workflow management instead of inventing an ad hoc process each time.
- When a repeated workflow failure reveals a missing local guardrail, use `.codex/skills/harness-gap-closure/` to turn that failure into issue-scoped harness hardening with regression follow-through.

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
