# OpenPrecedent MVP Roadmap

## Objective

Deliver a working MVP that proves the minimal decision loop:

1. capture a case
2. structure the event stream
3. extract decisions
4. replay and explain decisions
5. retrieve precedent

## Phase 0: Foundation

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

## Phase 1: Core Schemas

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

## Phase 2: Event Ingestion

Goal:

- accept and store case events with minimal validation

Deliverables:

- ingestion API endpoints
- event normalization layer
- basic persistence contract

Exit criteria:

- a full sample case can be written as ordered events

## Phase 3: Replay

Goal:

- replay a single case in both raw and decision-centric forms

Deliverables:

- case replay API
- raw timeline response
- decision timeline response

Exit criteria:

- a reviewer can understand a case after the fact

## Phase 4: Decision Extraction

Goal:

- derive high-value decisions from event streams

Deliverables:

- rule-based extractor
- evidence binding
- first explanation contract

Exit criteria:

- extracted decisions are meaningfully more useful than raw logs alone

## Phase 5: Precedent Retrieval

Goal:

- return historically similar cases

Deliverables:

- case summary generation
- structural and semantic retrieval inputs
- precedent response schema

Exit criteria:

- historical cases can help a user interpret a current task

## Phase 6: Local Runtime Validation

Goal:

- validate the loop against a real local agent workflow

Deliverables:

- one local runtime integration path
- one end-to-end captured case
- one replayed and explained case
- one precedent retrieval example

Exit criteria:

- the MVP proves value on a real task, not only synthetic samples
