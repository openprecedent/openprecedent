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

### 1. Start from the repository-local workflow

Use:

```bash
./scripts/run-codex-decision-lineage-workflow.sh \
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
./scripts/run-codex-decision-lineage-workflow.sh \
  --query-reason before_file_write \
  --task-summary "Stay within docs-only scope while updating the first project README." \
  --current-plan "Draft the project README before any broader implementation." \
  --candidate-action "Edit README.md"
```

```bash
./scripts/run-codex-decision-lineage-workflow.sh \
  --query-reason after_failure \
  --task-summary "Recover from a broader implementation attempt and stay within the approved docs-only scope." \
  --current-plan "Narrow back to documentation guidance." \
  --candidate-action "Retry broad implementation changes"
```

### 3. Verify that recording is happening

List recorded invocations:

```bash
openprecedent runtime list-decision-lineage-invocations
```

Inspect one invocation:

```bash
openprecedent runtime inspect-decision-lineage-invocation \
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

## End-To-End Startup Harness

For a repeatable startup-and-recording validation flow, use:

```bash
./scripts/run-codex-live-validation.sh
```

By default this prepares a workspace under `/tmp/openprecedent-codex-live` with:

- `runtime-home/` for the shared Codex runtime home
- `prompts/` with three round prompts
- `output/manifest.json`
- `output/20-invocation-list.json`
- `output/21-latest-invocation-summary.json`
- `next-steps.txt`

If you want the harness to execute a three-round repository-local validation automatically, run:

```bash
OPENPRECEDENT_CODEX_LIVE_RESET=1 \
OPENPRECEDENT_CODEX_LIVE_AUTO_RUN=1 \
./scripts/run-codex-live-validation.sh
```

That path is useful for validating that startup, runtime recording, listing, and inspection are all wired correctly before using the workflow in a different project.

## Read Next

- [codex-runtime-decision-lineage-workflow.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/codex-runtime-decision-lineage-workflow.md)
- [codex-runtime-boundary.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/codex-runtime-boundary.md)
- [codex-runtime-startup-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/codex-runtime-startup-validation.md)
