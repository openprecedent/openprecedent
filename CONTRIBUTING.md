# Contributing

## Workflow

OpenPrecedent uses a fork-and-pull-request workflow.

Expected flow:

1. fork the repository
2. create a feature branch
3. make a focused change
4. run local checks when possible
5. complete a local Codex review note before push
6. open a pull request into `openprecedent/openprecedent`

## Before Opening a PR

- update docs if schemas, APIs, or repository rules changed
- keep terminology consistent with:
  - `case`
  - `event`
  - `decision`
  - `artifact`
  - `precedent`
- avoid broad refactors unless explicitly scoped

## Review Expectations

- required checks must pass
- the pull request review gate must pass
- conversations should be resolved before merge

## Scope Discipline

Prefer small changes that clearly move one of these forward:

- event capture
- decision extraction
- replay and explanation
- precedent retrieval

Avoid reframing the project as:

- a generic graph database
- a generic memory graph
- a generic trace viewer
