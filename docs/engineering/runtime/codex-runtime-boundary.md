# Codex Runtime Boundary For Research

## Purpose

This document defines the Codex integration boundary for the current post-MVP research phase.

It is intentionally narrow.
The goal is not to make OpenPrecedent a generic multi-runtime adapter layer.
The goal is to add Codex as a second, research-only runtime so the repository can gather denser real development history and test semantic decision-lineage reuse more aggressively than the current OpenClaw-only path allows.

Parent research umbrella:

- GitHub issue `#100` `Define the post-MVP research evolution framework for OpenPrecedent`

Controlling implementation issue:

- GitHub issue `#125` `Define the Codex runtime integration boundary for research-only minimal support`

## Why Codex Is The Next Runtime

OpenClaw remains the first validated runtime path.
However, current real usage density is higher in Codex-driven repository development itself.

That makes Codex the better next research runtime because it already provides:

- long continuous development sessions
- dense user-agent collaboration
- repeated issue, branch, PR, rebase, review, and merge decisions
- realistic semantic constraints and approval boundaries

In short, Codex is the best current source of real decision-rich history for the next research stage.

## Boundary Statement

For the current research phase, Codex support means:

- importing real Codex development history into OpenPrecedent
- replaying that history as `case` and `event` records
- extracting semantic decision lineage from that history
- retrieving precedent over that history
- later exposing a narrow Codex-facing runtime workflow for requesting decision-lineage context during real development

Codex support does not mean:

- creating a generic runtime abstraction layer for arbitrary agents
- designing a stable public adapter SDK
- solving hosted multi-user production architecture
- solving cross-runtime normalization for all future agents now

Those belong to a later product phase, if issue `#100` is satisfied strongly enough to justify industrial-grade architecture planning.

## Required Capture Surfaces

The Codex research path needs to capture enough history to answer semantic questions about development judgment.

The minimum required surfaces are:

### 1. Session identity and scope

Each imported Codex case should preserve:

- a stable session or run identity when available
- repository or workspace identity
- timestamps
- the working task or issue context

This gives later replay and precedent enough scope to distinguish one development thread from another.

### 2. User intent and constraints

Codex research is primarily about semantic lineage.
That means user-side messages and instructions are first-class evidence.

The import path must preserve signals such as:

- scope boundaries
- approval boundaries
- completion criteria
- requests to discuss rather than edit
- branch / PR / review requirements

### 3. Agent reasoning outputs that change task direction

Not every assistant message is equally important.
The goal is to keep the parts that reveal semantic shifts such as:

- task reframing
- accepted assumptions
- rejected options
- explicit plans that redefine the work boundary

Operational chatter can remain event evidence, but it should not dominate the imported history.

### 4. Tool and execution evidence

Tool use, shell commands, file reads, file writes, and review checkpoints remain important evidence.
They are not first-class semantic decisions, but they often explain why a later semantic decision was made.

Codex support therefore must preserve them as event evidence for:

- replay readability
- evidence binding
- later inspection of decision lineage

### 5. Development governance context

Codex work in this repository often includes issue-driven development and review checkpoints.
That context is valuable because it carries authority and completion signals.

Where available, the Codex path should preserve evidence such as:

- issue references
- branch identity
- PR creation or review checkpoints
- merge or closure-related user instructions

This does not mean OpenPrecedent needs full GitHub platform modeling at this stage.
It means Codex research history should not discard governance signals that materially affect semantic decision lineage.

## Object Mapping Principles

Codex support should map into the current object model using the same normative rule used elsewhere in the repository:

- `event` records process evidence
- `decision` records reusable judgment

The mapping principles are:

### `case`

A Codex case should represent one coherent development thread or bounded task context.
It should be narrow enough to replay meaningfully, but broad enough to preserve the semantic continuity of the task.

### `event`

Codex events should preserve:

- user instructions
- agent responses
- tool calls and results
- command and file evidence
- task or governance context that materially changes later judgment

Codex-specific wrappers, transport metadata, or repeated execution noise should be normalized away when they do not help replay or semantic extraction.

### `decision`

Codex decisions must continue to use the semantic taxonomy only:

- `task_frame_defined`
- `constraint_adopted`
- `success_criteria_set`
- `clarification_resolved`
- `option_rejected`
- `authority_confirmed`

Tool choice, command execution, file write selection, and retry behavior must remain event evidence only.

### `artifact`

Codex artifacts should remain derived summaries or durable references that help explain the task.
At this stage they do not need a Codex-specific abstraction layer.

### `precedent`

Codex precedent should rank by semantic similarity, not operational mimicry.
The main question is whether one Codex development case helps interpret or guide another through shared judgment lineage.

## Research Questions This Boundary Must Support

The Codex path exists to answer concrete research questions under issue `#100`:

1. Can Codex development sessions be imported cleanly enough to support replay and extraction?
2. Do Codex sessions contain dense enough semantic decisions to be a better research data source than sparse OpenClaw usage?
3. Can precedent over Codex history return semantically useful prior judgment?
4. Can lineage from one real project later help work in a second project?

If the Codex path cannot support those questions, it should not expand further in the current phase.

## Non-Goals

The following are explicitly out of scope for the Codex minimal integration path:

- a general runtime plugin framework
- a public integration SDK for third-party agents
- universal schema contracts for all agent runtimes
- production service decomposition for many runtimes
- hosted tenancy, permissions, or access-control design for Codex users
- broad platform work justified only by anticipated future runtimes

## How This Supports Issue `#100`

The Codex path is meant to help satisfy the issue `#100` exit criteria in three ways:

1. it can provide a denser stream of real semantic decision data
2. it can provide a second runtime perspective without premature generic abstraction
3. it can support a later cross-project validation where earlier development judgment is tested against a new real project

That later real-project validation is the strongest expected signal for whether OpenPrecedent is ready to move from research framing into formal product architecture planning.

## Follow-On Issue Chain

The planned follow-on issues for this boundary are:

- `#126` Import Codex session history into OpenPrecedent as replayable cases and events
- `#127` Model Codex-specific event normalization and noise stripping
- `#128` Extract semantic decision lineage from Codex development sessions
- `#129` Validate precedent retrieval quality on Codex real development history
- `#130` Encapsulate OpenPrecedent as a Codex-facing minimal runtime workflow
- `#131` Validate Codex real-project decision-lineage reuse across project development

## Practical Rule

If a proposed Codex change makes the system more generic but does not directly improve the research value of the Codex path, it should be deferred until after issue `#100` is satisfied.
