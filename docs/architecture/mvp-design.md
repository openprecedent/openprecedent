# OpenPrecedent MVP Design

## Design Principles

- event stream first
- raw events and derived decisions are separate layers
- explanations must bind to evidence
- rule-based extraction comes before heavy model-driven extraction
- MVP uses simple storage and indexing before graph-specific infrastructure

## Core Objects

### Case

A complete task lifecycle.

### Event

An atomic fact in time.

### Decision

A structured, high-value judgment derived from events.

### Artifact

An important file, output, or referenced object associated with the case.

### Precedent

A retrieval result linking current work to historically similar cases.

## MVP Event Types

- `case.started`
- `message.user`
- `message.agent`
- `model.invoked`
- `model.completed`
- `tool.called`
- `tool.completed`
- `command.started`
- `command.completed`
- `file.read`
- `file.write`
- `user.confirmed`
- `case.completed`
- `case.failed`

## MVP Decision Types

- `clarify`
- `plan`
- `select_tool`
- `apply_change`
- `retry_or_recover`
- `finalize`

## Replay Model

Replay has two layers:

- raw timeline: what happened
- decision timeline: why key steps happened

## Retrieval Model

Precedent retrieval should mix:

- structural similarity
- semantic similarity

The first implementation can keep this simple and case-oriented rather than graph-oriented.
