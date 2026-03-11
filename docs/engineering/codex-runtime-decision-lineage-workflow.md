# Codex Runtime Decision-Lineage Workflow

## Goal

Record the minimal Codex-facing runtime workflow introduced for issue `#130`.

This workflow is intentionally narrow.
It does not introduce a generic runtime abstraction layer.
It gives Codex development work a stable way to:

- request a semantic decision-lineage brief
- keep runtime persistence on a shared OpenPrecedent home
- inspect the resulting invocation later

## Workflow Surface

Repository-local entrypoint:

```bash
./scripts/run-codex-decision-lineage-workflow.sh \
  --query-reason initial_planning \
  --task-summary "Do not edit code. Provide a short written recommendation only and keep it consistent with earlier Codex runtime decisions."
```

The script defaults `OPENPRECEDENT_HOME` to:

```bash
$HOME/.openprecedent/runtime
```

and then calls the existing runtime brief surface through the repository-local Python entrypoint.

## Inspectable Follow-Up

To inspect the newest invocation directly:

```bash
./scripts/run-codex-decision-lineage-workflow.sh \
  --inspect-latest \
  --query-reason initial_planning \
  --task-summary "..."
```

Or inspect invocations manually:

```bash
openprecedent runtime list-decision-lineage-invocations
openprecedent runtime inspect-decision-lineage-invocation --invocation-id <id>
```

## Validation Scenario

This issue validated the workflow against a representative Codex development scenario:

- current task asks for a docs-only recommendation
- prior Codex history contains a semantically similar docs-only recommendation case
- prior Codex history also contains an operationally similar but semantically different summary case

Observed result:

- the workflow returned a non-empty brief
- the matched cases included semantic Codex precedent instead of returning an empty brief
- the invocation was recorded in the runtime log and could be inspected afterwards

That is enough for the current research phase.

## Current Boundary

This workflow proves:

- Codex now has a runnable runtime path for consuming decision-lineage context
- the resulting invocation is inspectable with existing observability commands

It does not yet prove:

- long-run natural invocation behavior in a second real project
- cross-project portability
- when Codex should call the workflow automatically without prompt shaping

Those remain for:

- `#131` Validate Codex real-project decision-lineage reuse across project development
