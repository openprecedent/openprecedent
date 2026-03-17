# Using OpenPrecedent

## Purpose

This guide explains how to use the current OpenPrecedent MVP in practice.

For the planned long-term public-interface replacement, see:

- [rust-public-cli-design.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/rust-public-cli-design.md)
- [rust-public-cli-implementation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/rust-public-cli-implementation.md)

It is written for two audiences:

- humans who want to run the current local workflow themselves
- agent developers who want to connect a local agent workflow to OpenPrecedent

This is a usage guide for the shipped MVP, not a future platform manual.

## What OpenPrecedent Is Today

OpenPrecedent is currently a local-first decision replay and precedent layer with:

- a stable Rust public CLI
- a Python service layer retained for repository internals
- SQLite persistence
- OpenClaw transcript import and collection
- rule-based decision extraction
- replay, explanation, and precedent lookup over stored case history

The current MVP is strongest in one environment:

- a local single-agent workflow
- OpenClaw as the first integrated runtime
- import-based capture rather than live runtime hooks

## Before You Start

Build or install the Rust `openprecedent` CLI first.

Example:

```bash
cargo build -q -p openprecedent-cli
export PATH="$(pwd)/target/debug:$PATH"
```

After that, the main entry point is:

```bash
openprecedent --help
```

If you prefer not to update `PATH`, use the binary directly:

```bash
./target/debug/openprecedent --help
```

## The Two Practical Usage Modes

There are currently two good ways to use OpenPrecedent:

1. import or collect OpenClaw history
2. write cases and events explicitly through the CLI or Python service layer

Choose the first mode if your runtime is already OpenClaw.
Choose the second mode if you are prototyping another local agent flow and want to emit structured events directly.

## For Humans

### 1. Inspect available OpenClaw sessions

If you are using the OpenClaw-first workflow, start by listing sessions:

```bash
openprecedent capture openclaw list-sessions
```

This reads `~/.openclaw/agents/main/sessions/sessions.json` and shows the latest discoverable sessions.

### 2. Import one session into OpenPrecedent

Import the latest session:

```bash
openprecedent capture openclaw import-session --latest --case-id case_openclaw_latest
```

Or import a specific session by id:

```bash
openprecedent capture openclaw import-session \
  --session-id <session_id> \
  --case-id case_openclaw_target
```

Or import a specific transcript file directly:

```bash
openprecedent capture openclaw import-session \
  --session-file /path/to/session.jsonl \
  --case-id case_openclaw_file
```

### 3. Extract decisions

After import, derive the current rule-based decisions:

```bash
openprecedent decision extract case_openclaw_latest
```

### 4. Replay the case

Use replay when you want to understand what happened and why:

```bash
openprecedent replay case case_openclaw_latest
```

This returns:

- case metadata
- ordered events
- extracted decisions
- derived artifacts
- a short summary

### 5. Inspect stored decisions

If you care more about the key decision points than the whole timeline:

```bash
openprecedent decision list case_openclaw_latest
```

### 6. Look up precedent

Once you have more than one stored case, look for similar history:

```bash
openprecedent precedent find case_openclaw_latest --limit 3
```

This is useful when you want to answer questions like:

- have we seen a similar task before
- did a similar case involve file changes
- did a similar case require recovery
- what historical pattern looks reusable

### 7. Run unattended collection

If you want OpenPrecedent to keep importing new OpenClaw sessions over time:

```bash
openprecedent capture openclaw collect-sessions --limit 1
```

This command:

- discovers sessions from `sessions.json`
- imports only unseen sessions
- writes a local collector state file
- avoids duplicate imports

For scheduled local collection, see:

- [openclaw-collector-operations.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/openclaw-collector-operations.md)

### 8. Evaluate quality

There are two practical evaluation paths.

Curated fixture evaluation:

```bash
openprecedent eval fixtures tests/fixtures/evaluation/suite.json
```

Collected-session evaluation:

```bash
openprecedent eval captured-openclaw-sessions
```

Use these when you want to check whether replay, extraction, and precedent behavior still look correct.

## For Agents

An agent should not think of OpenPrecedent as a chat surface.
It is better thought of as a local evidence and precedent layer.

As of 2026-03-10, the intended long-term value is semantic decision lineage, not operational imitation.
In other words, OpenPrecedent should help later agents inherit task framing, constraints, approvals, and success criteria from earlier work, not blindly reuse old tool choices or file-write patterns.

The current MVP supports two agent-facing integration patterns.

### Pattern 1: Let OpenClaw produce history, then import it

This is the default and most validated path today.

Use this pattern when:

- the runtime is already OpenClaw
- you want minimal workflow disruption
- import after the task is acceptable

The agent workflow is:

1. OpenClaw runs normally and writes session history
2. OpenPrecedent imports that history later
3. decisions, replay, and precedent are derived from the imported case

Why this is the preferred MVP path:

- it requires no internal OpenClaw hook
- it preserves structured message and tool activity
- it is already validated in real local collection

### Pattern 2: Emit cases and events directly

This is the better pattern for another local agent runtime or an orchestrator that already has structured event data.

You can:

- create a case
- append events
- extract decisions
- replay the case
- look up precedent

CLI example:

```bash
openprecedent case create --case-id case_manual_1 --title "Manual agent task"
openprecedent event append case_manual_1 case.started system --payload '{}'
openprecedent event append case_manual_1 message.user user --payload '{"message":"Summarize the rollout doc"}'
openprecedent event append case_manual_1 message.agent agent --payload '{"message":"I will inspect the rollout documentation."}'
openprecedent decision extract case_manual_1
openprecedent replay case case_manual_1
```

Python service-layer pattern:

- instantiate `OpenPrecedentService`
- create a case with `CreateCaseInput`
- append ordered `AppendEventInput` events
- call `extract_decisions`, `replay_case`, or `find_precedents`

Use this path when your runtime already knows its own events and does not need transcript import.

### Post-MVP research path: Codex minimal integration

OpenPrecedent is also beginning a Codex-specific research path.
This is not part of the shipped MVP runtime surface.
It is the next post-MVP validation path because current real usage density is higher in Codex-driven repository development than in OpenClaw.

The controlling boundary document is:

- [codex-runtime-boundary.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-boundary.md)

That path is intentionally narrow:

- Codex is being added as a second research runtime
- the goal is denser real semantic decision data
- the goal is later cross-project validation of decision-lineage reuse
- it is explicitly not a generic adapter framework for arbitrary agents

The first Codex-facing import command is:

```bash
openprecedent capture codex import-rollout \
  /path/to/rollout.jsonl \
  --case-id case_codex_example \
  --title "Imported Codex rollout"
```

This command is intentionally minimal.
It imports one Codex rollout JSONL file into replayable `case` and `event` records so later extraction and precedent work can build on real Codex development history.
The importer also strips low-value Codex runtime wrapper noise such as transport metadata, duplicated prompt mirrors, token-count records, and command-output wrapper lines that do not help replay or semantic interpretation.
Imported Codex rollout history now also flows through the same semantic decision taxonomy as the rest of the repository, including task framing, constraints, clarifications, success criteria, rejected options, and explicit approval signals found in user guidance.
The current precedent-quality validation for Codex-derived history is recorded in [codex-precedent-retrieval-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/codex-precedent-retrieval-validation.md).

For Codex-driven development work, call the Rust CLI directly:

```bash
openprecedent --home "$HOME/.openprecedent/runtime" --format json lineage brief \
  --query-reason initial_planning \
  --task-summary "Do not edit code. Provide a short written recommendation only and keep it consistent with earlier Codex runtime decisions."
```

That workflow is documented here:

- [codex-runtime-decision-lineage-workflow.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-decision-lineage-workflow.md)
- [codex-runtime-startup-guide.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-startup-guide.md)
- [codex-runtime-startup-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-startup-validation.md)
- [SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/codex-runtime-decision-lineage/SKILL.md)

### Runtime decision-lineage brief

For OpenClaw-facing runtime use, OpenPrecedent now exposes a dedicated semantic briefing surface:

```bash
openprecedent --format json lineage brief \
  --query-reason initial_planning \
  --task-summary "Do not edit code. Provide a short written recommendation only."
```

This command is intentionally narrow.
It returns a semantic brief built from prior cases, including task framing, accepted constraints, success criteria, rejected options, and authority signals.
It does not prescribe tools, commands, or file writes directly.
Each successful call also appends a runtime invocation record to the local decision-lineage invocation log so later validation can inspect when the brief was requested and with what semantic context.

For live OpenClaw integrations, configure a stable shared runtime home instead of letting the current workspace choose the database and log paths implicitly:

```bash
export OPENPRECEDENT_HOME="$HOME/.openprecedent/runtime"
```

With that single setting, runtime commands will read and write:

- `$OPENPRECEDENT_HOME/openprecedent.db`
- `$OPENPRECEDENT_HOME/openprecedent-runtime-invocations.jsonl`

If you need independent locations, override them explicitly:

```bash
export OPENPRECEDENT_DB="$HOME/.openprecedent/runtime/openprecedent.db"
export OPENPRECEDENT_RUNTIME_INVOCATION_LOG="$HOME/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl"
```

This is the supported way to make an OpenClaw-installed skill use the same persisted decision lineage and runtime log across isolated workspaces.

If you want to inspect those records directly:

```bash
openprecedent --format json lineage invocation list
```

If you want to inspect one invocation together with its recorded brief summary and the nearby downstream case signals:

```bash
openprecedent --format json lineage invocation inspect \
  --invocation-id <invocation_id>
```

An installable OpenClaw skill is also included in this repository:

- [SKILL.md](/workspace/02-projects/incubation/openprecedent/skills/openprecedent-decision-lineage/SKILL.md)

That skill is designed for progressive disclosure.
It teaches OpenClaw when to call `openprecedent --format json lineage brief`, how to choose `query_reason`, and how to use the returned brief as judgment context rather than operational instructions.

A separate OpenPrecedent-maintained HarnessHub private skill bundle is also included for the current real-project study:

- [openprecedent-harnesshub-composition/SKILL.md](/workspace/02-projects/incubation/openprecedent/skills/openprecedent-harnesshub-composition/SKILL.md)
- [openprecedent-harnesshub-validation/SKILL.md](/workspace/02-projects/incubation/openprecedent/skills/openprecedent-harnesshub-validation/SKILL.md)

That HarnessHub bundle is maintained here in OpenPrecedent, then installed into a local HarnessHub workspace as a private `.codex/skills/` bundle so the study can keep one canonical skill source without making HarnessHub publicly depend on OpenPrecedent.

The bundle installs two private skills:

- a composition skill that tells local HarnessHub sessions to compose the private validation layer with `harness-issue-execution` or `harness-multi-issue-delivery` when available
- the validation skill that performs the OpenPrecedent availability probe and the lineage queries themselves

To install or refresh it into a local HarnessHub checkout:

```bash
python3 scripts/install_harnesshub_skill.py \
  --target-repo-root /workspace/02-projects/active/HarnessHub
```

### Runtime decision-lineage validation baseline

The current trigger-policy baseline for the OpenClaw-facing decision-lineage skill is documented here:

- [openclaw-runtime-decision-lineage-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-runtime-decision-lineage-validation.md)

That document defines which trigger points are currently recommended:

- `initial_planning`
- `before_file_write`
- `after_failure` only when the failure is semantic rather than merely operational

It also now treats prompts like "keep it consistent with earlier repository decisions" as implicit `initial_planning` lineage triggers, even when the user does not explicitly mention OpenPrecedent.

The first live isolated-profile runtime findings are documented here:

- [openclaw-real-runtime-decision-lineage-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-real-runtime-decision-lineage-validation.md)

A follow-up live rerun after shared-path wiring is documented here:

- [openclaw-runtime-decision-lineage-trigger-rerun.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-runtime-decision-lineage-trigger-rerun.md)

The reusable harness entrypoint for repeating this style of live validation is documented here:

- [openclaw-live-validation-harness.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-live-validation-harness.md)

That live validation records three important realities:

- a discoverable skill is not automatically used for every constrained task
- OpenClaw may prefer built-in memory before OpenPrecedent unless the prompt or future policy pushes lineage retrieval more explicitly
- the current runtime path needs explicit shared DB wiring if the skill should see repository-captured history instead of an empty workspace-local database

## What Humans Usually Need

Human users usually care about:

- how to capture a real task without changing workflow too much
- how to replay and understand a task after the fact
- how to see the important decisions instead of only raw logs
- how to compare the current case to prior work
- how to monitor collection quality over time

That is why the human workflow above centers on:

- import or collect
- extract
- replay
- precedent find
- evaluate

## What Agents Usually Need

Agent developers usually care about:

- where OpenPrecedent fits in the execution loop
- whether integration is online or offline
- what minimal data contract they must provide
- when decisions and precedents are available
- what the current system does not support yet

For the current MVP, the practical answers are:

- integration is local-first
- the best-supported path is offline import from OpenClaw session history
- direct event emission is available for structured runtimes
- decisions are derived after event ingestion
- precedents are available after a case and its decisions are stored

The decision-model direction is also important:

- raw events should retain operational evidence such as tool calls and file activity
- decision records should converge on reusable judgment rather than operational moves
- future runtime retrieval should return semantic decision-lineage context, not operational instructions

## Current Limitations You Should Design Around

When using OpenPrecedent today, assume the following constraints:

- OpenClaw integration is import-based, not a live runtime callback path
- decision extraction is intentionally narrow and rule-based
- precedent retrieval is fingerprint-based, not embedding-first
- the current system is local and single-operator oriented
- there is no hosted API or multi-user coordination layer in the current MVP

If you design around those constraints, the current MVP is predictable and easy to audit.

## Recommended MVP Usage Pattern

If you only want one recommended pattern, use this:

1. let OpenClaw run normally
2. collect or import sessions into OpenPrecedent
3. extract decisions
4. replay important cases
5. query precedent against the growing local history
6. run evaluation periodically to catch quality regressions

That is the cleanest way to use the system today.
