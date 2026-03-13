---
name: openprecedent-harnesshub-validation
description: Use for HarnessHub development so local decision lineage and precedent reuse are consulted by default without making the repository appear to depend on OpenPrecedent.
user-invocable: false
---

# OpenPrecedent HarnessHub Validation

Use this skill inside `/workspace/02-projects/active/HarnessHub` for local HarnessHub development.

This is a private validation layer for development sessions that already have local access to OpenPrecedent.
It should improve decision continuity, but it must not make HarnessHub look publicly coupled to OpenPrecedent.

## Composition

Use this skill together with HarnessHub's main issue-execution workflow.

- For normal single-issue work, compose it with `harness-issue-execution`.
- For multi-issue delivery sessions, compose it with `harness-multi-issue-delivery`.

This skill handles semantic lineage retrieval.
HarnessHub's own workflow skills still handle branch, task, review, preflight, PR, and merge sequencing.

## Step 0: Probe Availability

Before trying to retrieve lineage, verify that local OpenPrecedent is available:

```bash
OPENPRECEDENT_REPO_ROOT="{{OPENPRECEDENT_REPO_ROOT}}"
OPENPRECEDENT_WORKFLOW="$OPENPRECEDENT_REPO_ROOT/scripts/run-codex-decision-lineage-workflow.sh"
test -x "$OPENPRECEDENT_WORKFLOW"
```

If that probe fails:

- treat OpenPrecedent as unavailable for this session
- continue normal HarnessHub development without lineage retrieval
- do not treat the missing local setup as a HarnessHub repository error

## Minimum Default Flow

When OpenPrecedent is available, use the minimum lineage flow below:

1. Run one `initial_planning` query before implementation starts.
2. Run one `before_file_write` query when the concrete change shape is known.
3. Run one `after_failure` query only when a failure is semantic, directional, or recovery-shaping rather than a transient command problem.

If the returned brief is empty, continue normally.

## Step 1: Minimal Entry Query

Start with the lowest-cost query first:

```bash
OPENPRECEDENT_REPO_ROOT="{{OPENPRECEDENT_REPO_ROOT}}"
export OPENPRECEDENT_HOME="$HOME/.openprecedent/runtime"
"$OPENPRECEDENT_REPO_ROOT/scripts/run-codex-decision-lineage-workflow.sh" \
  --query-reason initial_planning \
  --task-summary "<one-line HarnessHub issue summary>"
```

Do not load deeper OpenPrecedent-side research context unless the task actually needs it.

## Step 2: Narrow When The Change Is Concrete

When the write path is clearer, tighten the query:

```bash
OPENPRECEDENT_REPO_ROOT="{{OPENPRECEDENT_REPO_ROOT}}"
export OPENPRECEDENT_HOME="$HOME/.openprecedent/runtime"
"$OPENPRECEDENT_REPO_ROOT/scripts/run-codex-decision-lineage-workflow.sh" \
  --query-reason before_file_write \
  --task-summary "<current task summary>" \
  --current-plan "<current plan>" \
  --candidate-action "<planned change>" \
  --known-file "<candidate file>"
```

Add more `--known-file` flags only when the relevant file set is already concrete.

## Step 3: Recovery Query

Use `after_failure` only when the failure should change task framing or recovery direction:

```bash
OPENPRECEDENT_REPO_ROOT="{{OPENPRECEDENT_REPO_ROOT}}"
export OPENPRECEDENT_HOME="$HOME/.openprecedent/runtime"
"$OPENPRECEDENT_REPO_ROOT/scripts/run-codex-decision-lineage-workflow.sh" \
  --query-reason after_failure \
  --task-summary "<current task summary>" \
  --current-plan "<failed or current plan>" \
  --candidate-action "<next recovery idea>"
```

## Fallback Rules

- If the OpenPrecedent repository path is absent, skip lineage and continue the HarnessHub task normally.
- If the workflow script is absent, skip lineage and continue normally.
- If the lineage query fails, treat it as a local tooling gap and continue the HarnessHub task normally.
- If the lineage brief is empty, continue normally without forcing precedent use.

## Progressive Disclosure

1. Read [`references/harnesshub-validation.md`](references/harnesshub-validation.md) first.
2. Use the minimum default query flow before loading deeper context.
3. Read OpenPrecedent-side research files only when the current task needs more validation context or historical interpretation.

## Read Next

- [`references/harnesshub-validation.md`](references/harnesshub-validation.md)
