# Codex Runtime Startup Guide

## Goal

Show both a human operator and a Codex-driven workflow how to start OpenPrecedent for a new Codex project, request decision-lineage context during work, and verify that runtime records are actually being written.

This is a practical startup guide.
It is not a generic multi-agent integration manual.

## What This Enables Today

Today, Codex runtime support can do three concrete things:

- use a shared `OPENPRECEDENT_HOME` for Codex runtime state
- request semantic decision-lineage briefs during work
- record each runtime invocation so it can be listed and inspected later

It does not yet automatically ingest an entire new project's Codex transcript history continuously.
The current runtime recording loop is centered on inspectable lineage requests.

## Shared Runtime Setup

Use a stable shared runtime home instead of letting each repository choose its own runtime database and log:

```bash
export OPENPRECEDENT_HOME="$HOME/.openprecedent/runtime"
```

With that one setting, Codex runtime use will share:

- `$OPENPRECEDENT_HOME/openprecedent.db`
- `$OPENPRECEDENT_HOME/openprecedent-runtime-invocations.jsonl`

This is the recommended starting point for both humans and agents.

## For Humans

### 1. Start from the Rust CLI

Use:

```bash
openprecedent --home "$HOME/.openprecedent/runtime" --format json lineage brief \
  --query-reason initial_planning \
  --task-summary "Describe the new project task here."
```

This will:

- build a semantic decision-lineage brief from the shared runtime home
- append a runtime invocation record to the shared invocation log

### 2. Use the workflow at the right moments

The current supported `query_reason` values are:

- `initial_planning`
- `before_file_write`
- `after_failure`

Typical examples:

```bash
openprecedent --home "$HOME/.openprecedent/runtime" --format json lineage brief \
  --query-reason before_file_write \
  --task-summary "Stay within docs-only scope while updating the first project README." \
  --current-plan "Draft the project README before any broader implementation." \
  --candidate-action "Edit README.md"
```

```bash
openprecedent --home "$HOME/.openprecedent/runtime" --format json lineage brief \
  --query-reason after_failure \
  --task-summary "Recover from a broader implementation attempt and stay within the approved docs-only scope." \
  --current-plan "Narrow back to documentation guidance." \
  --candidate-action "Retry broad implementation changes"
```

### 3. Verify that recording is happening

List recorded invocations:

```bash
openprecedent --home "$HOME/.openprecedent/runtime" --format json lineage invocation list
```

Inspect one invocation:

```bash
openprecedent --home "$HOME/.openprecedent/runtime" --format json lineage invocation inspect \
  --invocation-id <invocation_id>
```

You should see:

- `query_reason`
- `task_summary`
- matched case ids
- semantic brief content such as constraints and authority signals

## For Agents

Treat OpenPrecedent as a semantic judgment layer, not as a tool-selection engine.

An agent should:

- use `initial_planning` when it needs prior framing before work starts
- use `before_file_write` when a risky change should be checked against prior approvals or scope limits
- use `after_failure` when the failure is directional or semantic, not just transient execution noise
- continue normally if the returned brief is empty

An agent should not:

- use OpenPrecedent to imitate old tool choices mechanically
- call the workflow on every turn
- treat the brief as a replacement for current local context

## End-To-End Startup Validation

For a repeatable startup-and-recording validation flow, execute the same Rust CLI surface directly:

```bash
openprecedent --home "$HOME/.openprecedent/runtime" --format json capture codex import-rollout tests/fixtures/codex_rollout_precedent_current.jsonl --case-id case_codex_live_current --title "Codex live seed current"
openprecedent --home "$HOME/.openprecedent/runtime" --format json decision extract case_codex_live_current
openprecedent --home "$HOME/.openprecedent/runtime" --format json lineage brief --query-reason initial_planning --task-summary "Do not edit code. Provide a short written recommendation only and keep it consistent with earlier Codex runtime decisions."
openprecedent --home "$HOME/.openprecedent/runtime" --format json lineage invocation list
```

That path validates that startup, runtime recording, listing, and inspection are all wired correctly before using the workflow in a different project.

## Read Next

- [codex-runtime-decision-lineage-workflow.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-decision-lineage-workflow.md)
- [codex-runtime-boundary.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-boundary.md)
- [codex-runtime-startup-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-startup-validation.md)
