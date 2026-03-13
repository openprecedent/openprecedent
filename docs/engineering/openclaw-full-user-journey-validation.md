# OpenClaw Full User Journey Validation

## Goal

Record one consolidated end-to-end validation pass for the full OpenClaw user journey on the latest merged OpenPrecedent MVP.

This document is meant to be a durable baseline for:

- future OpenClaw product evolution
- usability improvements for human operators
- integration improvements for agent workflows
- later research on replay, explanation, and precedent quality

## Validation Baseline

- validation date: `2026-03-10`
- repository baseline: `upstream/main` at `d26242d`
- validation mode: repository-local end-to-end run using the current CLI and local fixture-backed OpenClaw session history
- runtime focus: OpenClaw MVP path only

Why this setup was used:

- it exercises the shipped CLI and service layer exactly as a user or local agent would
- it avoids speculative architecture discussion and validates the real command path
- it is reproducible inside the repository without needing a separate live OpenClaw host

## Journey Scope

The validation covered the current OpenClaw MVP journey from:

1. session discovery
2. collection and manual import
3. decision extraction
4. replay
5. precedent lookup
6. fixture evaluation
7. collected-session evaluation

## Validation Setup

A temporary local environment was created under `/tmp/openprecedent-openclaw-journey` with:

- a temporary SQLite database
- a temporary collector state file
- a temporary OpenClaw sessions directory
- three OpenClaw session fixtures:
  - `file-ops-session.jsonl`
  - `search-read-session.jsonl`
  - `sample-session.jsonl`

The main command surface used during validation was `.venv/bin/openprecedent`.

## End-to-End Journey

### 1. Session discovery worked

Command used:

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
OPENPRECEDENT_COLLECTOR_STATE=/tmp/openprecedent-openclaw-journey/collector-state.json \
.venv/bin/openprecedent capture openclaw list-sessions \
  --sessions-root /tmp/openprecedent-openclaw-journey/sessions
```

Observed result:

- the CLI discovered all three sessions from `sessions.json`
- session ordering followed `updatedAt`
- session metadata such as `label`, `model`, `is_active`, and transcript path were surfaced correctly

User impact:

- a human operator can verify what OpenClaw history is available before importing anything
- an agent or orchestrator can treat this as a local discovery step before choosing a target session

### 2. Collector import worked for the newest unseen session

Command used:

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
OPENPRECEDENT_COLLECTOR_STATE=/tmp/openprecedent-openclaw-journey/collector-state.json \
.venv/bin/openprecedent capture openclaw collect-sessions \
  --sessions-root /tmp/openprecedent-openclaw-journey/sessions \
  --limit 1
```

Observed result:

- the collector imported `file-ops-session`
- it created case `openclaw_fileopssession`
- it imported `12` events
- it wrote a collector state file containing `file-ops-session`
- unsupported record type count was empty

User impact:

- the unattended collection path works for the current OpenClaw MVP flow
- the collector uses ordered session metadata rather than the `is_active` flag alone

### 3. Manual session import worked

Commands used:

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
.venv/bin/openprecedent capture openclaw import-session \
  --session-id search-read-session \
  --sessions-root /tmp/openprecedent-openclaw-journey/sessions \
  --case-id case_openclaw_search_read
```

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
.venv/bin/openprecedent capture openclaw import-session \
  --session-id sample-session \
  --sessions-root /tmp/openprecedent-openclaw-journey/sessions \
  --case-id case_openclaw_sample
```

Observed result:

- both manual imports succeeded
- each transcript was normalized into replayable events
- `search-read-session` imported `9` events
- `sample-session` imported `9` events
- unsupported record type count was empty in both imports

User impact:

- the manual import path is good for investigation, debugging, and targeted validation
- an agent developer can use the import path without waiting for scheduled collection

### 4. Decision extraction worked on imported and collected cases

Commands used:

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
.venv/bin/openprecedent decision extract openclaw_fileopssession
```

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
.venv/bin/openprecedent decision extract case_openclaw_search_read
```

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
.venv/bin/openprecedent decision extract case_openclaw_sample
```

Observed result:

- `openclaw_fileopssession` produced `4` decisions:
  - `plan`
  - `select_tool`
  - `select_tool`
  - `apply_change`
- `case_openclaw_search_read` produced `2` decisions:
  - `plan`
  - `select_tool`
- `case_openclaw_sample` produced `2` decisions:
  - `plan`
  - `select_tool`

User impact:

- the current rule-based extractor is good enough to recover high-signal steps from these OpenClaw sessions
- extraction remains explicit rather than automatic, which is operationally clear but one extra step for users

### 5. Replay worked and returned a coherent combined view

Command used:

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
.venv/bin/openprecedent --format json replay case case_openclaw_search_read
```

Observed result:

- replay returned case metadata, ordered events, extracted decisions, derived artifacts, and a summary
- the replay summary was `User session: search roadmap docs: 9 events, 2 decisions, status=started`
- derived artifacts included:
  - the user message
  - the assistant message
  - the command output showing the roadmap hit

User impact:

- the replay surface is already useful for both audit and explanation
- artifact derivation makes the case easier to read than raw event lists alone

### 6. Precedent lookup worked once enough history existed

Command used:

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
.venv/bin/openprecedent precedent find case_openclaw_search_read --limit 3
```

Observed result:

- the top precedent was `openclaw_fileopssession` with score `14`
- the second precedent was `case_openclaw_sample` with score `12`
- the strongest similarity signals were:
  - shared decision types
  - shared tools
  - shared file targets
  - shared read targets
  - shared keywords

User impact:

- precedent retrieval is already producing explainable, inspectable rankings
- it becomes more useful once the local case history has at least a few comparable examples

### 7. Fixture evaluation passed on a clean database

Command used:

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/eval-fixtures.db \
.venv/bin/openprecedent --format json eval fixtures tests/fixtures/evaluation/real_session_suite.json
```

Observed result:

- total cases: `3`
- passed cases: `3`
- failed cases: `0`

User impact:

- the current real-session-oriented evaluation suite still passes against the latest MVP baseline
- this provides a stable regression anchor for future OpenClaw work

### 8. Collected-session evaluation worked on the collected history

Command used:

```bash
OPENPRECEDENT_DB=/tmp/openprecedent-openclaw-journey/openprecedent.db \
OPENPRECEDENT_COLLECTOR_STATE=/tmp/openprecedent-openclaw-journey/collector-state.json \
.venv/bin/openprecedent --format json eval captured-openclaw-sessions \
  --sessions-root /tmp/openprecedent-openclaw-journey/sessions
```

Observed result:

- evaluated cases: `1`
- total sessions from collector state: `1`
- average event count: `12.0`
- average decision count: `4.0`
- top precedent for the collected case was `case_openclaw_search_read` with score `14`

User impact:

- the collected-session evaluation path is already useful as an operations and quality checkpoint
- it is good enough to summarize the current state of silently collected OpenClaw history

## What Worked Well

- the latest MVP supports the whole core OpenClaw journey through real CLI commands
- session discovery is clear and inspectable
- both collection and manual import work
- event normalization produced replayable history with no unsupported record types in this validation set
- decision extraction recovered meaningful steps from the tested sessions
- replay combined facts, decisions, artifacts, and summary into one readable object
- precedent retrieval produced auditable rankings rather than opaque scores
- the clean-room evaluation suite passed against the latest baseline

## What Was Confusing Or Weak

### 1. `eval fixtures` is not idempotent on a used database

Observed behavior:

- running `eval fixtures` against a database that already contains those evaluation case ids failed with:
  - `event conflict for case eval_real_file_ops: event_id or sequence_no already exists`

Why this matters:

- a human user may assume evaluation is safe to rerun on the same DB
- an agent may assume evaluation is a read-mostly regression command
- in practice it currently behaves more like an import into a clean environment

Implication:

- evaluation should currently be treated as a clean-DB workflow unless the command semantics are changed

### 2. Manual import and collector deduplication are not aligned

Observed behavior:

- after manually importing `search-read-session` as `case_openclaw_search_read`, a later collector run still attempted to import the same transcript
- the collector generated canonical case id `openclaw_searchreadsession`
- import then failed with an event-id conflict
- a new empty case shell remained in the database:
  - `openclaw_searchreadsession`
  - `0` events
  - `0` decisions

Why this matters:

- this is a real user-journey footgun
- a human can accidentally create duplicate history paths
- an agent cannot safely mix targeted import and background collection without extra coordination logic

Implication:

- duplicate transcript protection is currently stronger at the collector state layer than at the database identity layer
- future work should unify transcript identity, deduplication, and case creation semantics

### 3. Decision extraction is usable but still deliberately narrow

Observed behavior:

- the tested sessions produced strong `plan`, `select_tool`, and `apply_change` decisions
- richer decision types were not exercised in every path

Why this matters:

- the current experience is understandable
- but more complex real OpenClaw journeys will still expose gaps in decision coverage

## Human Perspective Summary

For a human operator, the current MVP is already workable if the goal is:

- inspect OpenClaw history
- import a task into OpenPrecedent
- derive a concise decision view
- replay what happened
- find similar prior cases
- run quality checks

The main human-facing friction points exposed by this validation are:

- evaluation commands need cleaner isolation expectations
- duplicate transcript handling is not yet safe across mixed manual and collector workflows

## Agent Perspective Summary

For an agent or agent developer, the current MVP already supports a realistic local evidence loop:

- OpenClaw can emit history normally
- OpenPrecedent can import or collect it afterward
- decisions and precedents can be derived from stored history
- evaluation can be used as a quality gate

The main agent-facing friction points exposed by this validation are:

- collectors and manual imports do not yet share one deduplication contract
- evaluation is not currently safe as a repeated in-place command on a shared working DB

## Recommendations For Evolution

### Short-term product fixes

1. make transcript identity deduplication first-class so the same session cannot leave behind conflicting or empty duplicate cases
2. make `eval fixtures` explicitly isolated by default, or fail earlier with a clearer message and no partial writes
3. decide whether decision extraction should remain a manual step or become an optional automatic post-import behavior

### Short-term research and quality work

1. expand full-journey validation beyond the current three-session fixture set
2. add cases with completion, failure, clarification, and longer multi-step recovery
3. compare replay usefulness for humans versus agents using the same collected cases

### Medium-term OpenClaw evolution questions

1. should manual import and scheduled collection converge on one session-identity model
2. should collected-session evaluation operate on an isolated reporting store rather than the active working DB
3. should replay expose a more opinionated user-journey summary on top of the current raw-plus-derived structure

## Bottom Line

The latest MVP already proves the OpenClaw end-to-end loop:

- discover sessions
- import or collect them
- extract decisions
- replay the case
- retrieve precedent
- run evaluation

The system is real and usable today.

The next important work is no longer “can this loop exist.”
It is “can this loop stay safe, repeatable, and legible when humans and agents use multiple entry paths over the same growing local history.”
