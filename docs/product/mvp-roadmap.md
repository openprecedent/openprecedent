# OpenPrecedent MVP Roadmap

## Current Status

As of 2026-03-10, the MVP core loop is implemented and validated in a real local target environment.

Completed:

- repository foundation, governance, CI, and review workflow
- core schemas for `case`, `event`, `decision`, `artifact`, and `precedent`
- SQLite-backed ingestion, replay, extraction, and precedent APIs
- CLI flows for case/event/replay/decision/precedent operations
- OpenClaw-style runtime trace import
- OpenClaw session transcript import for silent trajectory collection
- automated OpenClaw session collection with a local cursor/state file
- curated MVP evaluation fixture suite for regression checks
- unsupported OpenClaw record type reporting during import and evaluation
- additional OpenClaw transcript mapping for `checkpoint` session records
- follow-up user clarification extraction on multi-turn OpenClaw transcripts
- anonymized real-session evaluation fixtures through the existing evaluation flow
- precedent ranking improvements validated against anonymized real-session cases
- real-environment scheduled collector rollout validated through cron
- first collected OpenClaw session replayed and evaluated end-to-end in the target environment

Still open:

- reduce real-session noise in imported OpenClaw messages and derived decisions
- improve transcript mapping coverage for real-world OpenClaw record types that still carry useful signal
- strengthen precedent quality and evaluation depth on larger real-case histories

## Objective

Deliver a working MVP that proves the minimal decision loop:

1. capture a case
2. structure the event stream
3. extract decisions
4. replay and explain decisions
5. retrieve precedent

## Phase 0: Foundation

Status:

- completed

Goal:

- align strategy, MVP requirements, design, competitive landscape, and technical direction in-repo

Deliverables:

- strategy summary
- MVP PRD
- MVP design summary
- competitive landscape
- technical selection
- repository scaffold

Exit criteria:

- repository can serve as the single implementation home for the MVP

Completed work:

- in-repo strategy, PRD, design, roadmap, and competitive research
- repository governance, branch protection, review policy, CI, and notification setup

## Phase 1: Core Schemas

Status:

- completed

Goal:

- stabilize the core object model

Deliverables:

- `case` schema
- `event` schema
- `decision` schema
- `artifact` schema
- `precedent` schema

Exit criteria:

- schema names and fields are stable enough for ingestion and replay work

Completed work:

- stable first-pass schemas for `case`, `event`, `decision`, `artifact`, and `precedent`
- explanation contract and precedent response contract

## Phase 2: Event Ingestion

Status:

- completed

Goal:

- accept and store case events with minimal validation

Deliverables:

- ingestion API endpoints
- event normalization layer
- basic persistence contract

Exit criteria:

- a full sample case can be written as ordered events

Completed work:

- case/event API and SQLite persistence
- JSONL import path for sample traces
- CLI ingestion commands
- OpenClaw-style runtime trace import

## Phase 3: Replay

Status:

- completed

Goal:

- replay a single case in both raw and decision-centric forms

Deliverables:

- case replay API
- raw timeline response
- decision timeline response

Exit criteria:

- a reviewer can understand a case after the fact

Completed work:

- replay API
- CLI replay rendering for raw events, decisions, and derived artifacts
- artifact derivation from message, command, and file events

## Phase 4: Decision Extraction

Status:

- completed for MVP v1

Goal:

- derive high-value decisions from event streams

Deliverables:

- rule-based extractor
- evidence binding
- first explanation contract

Exit criteria:

- extracted decisions are meaningfully more useful than raw logs alone

Completed work:

- rule-based decision extractor
- explanation contract with goal, evidence, constraints, reason, and result
- support for `plan`, `clarify`, `select_tool`, `apply_change`, `retry_or_recover`, and `finalize`

Remaining gaps:

- broader decision coverage may still be needed as real collected transcripts reveal new patterns
- stronger extraction quality evaluation on a growing set of real collected trajectories

## Phase 5: Precedent Retrieval

Status:

- completed for MVP v1

Goal:

- return historically similar cases

Deliverables:

- case summary generation
- structural and semantic retrieval inputs
- precedent response schema

Exit criteria:

- historical cases can help a user interpret a current task

Completed work:

- case summary generation
- fingerprint-based precedent retrieval
- precedent response with similarities, differences, score, and reusable takeaway
- curated fixture-based precedent evaluation
- anonymized real-session precedent evaluation coverage
- improved ranking for read-heavy real-session search cases

Remaining gaps:

- stronger retrieval quality validation on larger continuously collected real history
- richer semantic retrieval beyond current lightweight matching

## Phase 6: Local Runtime Validation

Status:

- completed for MVP rollout

Goal:

- validate the loop against a real local agent workflow

Deliverables:

- one local runtime integration path
- one end-to-end captured case
- one replayed and explained case
- one precedent retrieval example

Exit criteria:

- the MVP proves value on a real task, not only synthetic samples

Completed work:

- OpenClaw session transcript import from `~/.openclaw/agents/main/sessions/`
- session discovery and `--latest` import flow
- automated collector command with local state cursor for silent collection
- curated evaluation suite for summary and recovery trajectories
- anonymized real-session evaluation suite through `eval fixtures`
- operational collector assets for `systemd` / `cron`
- path-aware installer script for collector scheduling assets
- collected-session evaluation/report command for real imported sessions
- unsupported OpenClaw record type reporting in import and collected-session evaluation output
- `checkpoint` session record mapping into replayable raw events
- follow-up user clarification extraction on multi-turn session transcripts
- precedent ranking tuned and regression-tested against anonymized real-session cases
- validated cron-based rollout in the real target environment
- first live collected session replayed and evaluated end-to-end
- rollout findings and caveats documented in `docs/engineering/openclaw-collector-rollout-validation.md`

Remaining gaps:

- reduce import-time noise and false-positive decision extraction on real collected sessions
- validate replay/extraction/precedent quality on a broader set of real collected sessions
- keep improving precedent ranking and record-type coverage as real history grows

## Next Tasks

The next MVP work should focus on improving quality on top of the validated live collection path:

1. strip operator policy and transport metadata noise from imported OpenClaw session messages
2. tighten `clarify` decision extraction against real multi-turn sessions
3. extend transcript mapping for additional OpenClaw record types only where live collection exposes useful signal
4. grow the real-session evaluation set and re-tune precedent ranking against the larger history
