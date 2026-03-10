# OpenClaw Real Runtime Decision-Lineage Validation

## Goal

Record the first live OpenClaw validation pass for the OpenPrecedent decision-lineage skill in a real runtime loop.

This document is intentionally different from the repository-local trigger-policy baseline.
It focuses on natural OpenClaw behavior in an isolated live profile, including whether the skill is called at all, what it returns, and what limits currently block stronger runtime benefit.

## Validation Baseline

- validation date: `2026-03-10`
- repository baseline: `upstream/main` at `eb43fea`
- OpenClaw runtime mode: live local agent execution with an isolated profile
- OpenClaw profile: `opv80`
- OpenClaw workspace: `/root/.openclaw-opv80/workspace`
- OpenClaw gateway port: `19080`
- OpenPrecedent runtime surfaces under test:
  - `skills/openprecedent-decision-lineage/SKILL.md`
  - `openprecedent runtime decision-lineage-brief`
  - `openprecedent runtime list-decision-lineage-invocations`

Why this setup was used:

- it exercises real OpenClaw skill discovery and tool use rather than fixture-only simulation
- it avoids contaminating the default OpenClaw profile and workspace
- it validates the actual runtime invocation path that a later user or agent would depend on

## Validation Setup

The live validation used an isolated OpenClaw profile instead of the default `~/.openclaw` environment.

Setup highlights:

- OpenClaw was run with `--profile opv80`
- the profile config was updated to use workspace `/root/.openclaw-opv80/workspace`
- the profile gateway port was changed to `19080` so requests would not reuse the default profile gateway
- the OpenPrecedent skill bundle was copied into `/root/.openclaw-opv80/workspace/skills/openprecedent-decision-lineage`
- the `openprecedent` CLI was exposed on `PATH`
- OpenClaw auth state was copied into the isolated profile so the agent could run normally

One previously completed no-code OpenClaw session from this same isolated profile was imported into the repository working database and semantic decisions were extracted before later runtime tests.

That imported case produced these semantic decisions:

- `constraint_adopted`
- `success_criteria_set`
- `option_rejected`

This gave the runtime validation at least one relevant prior case, but only in the repository working database.

## Task Set

The live validation used three short recommendation tasks.
All three were intentionally no-code tasks so the signal stayed on semantic framing rather than execution mechanics.

### Task A: direct recommendation only

Prompt:

`Do not edit code. Provide a short written recommendation only for how to improve README navigation in this repository.`

### Task B: recommendation plus consistency with prior decisions

Prompt:

`Do not edit code. Provide a short written recommendation only for improving repository navigation, and keep it consistent with earlier repository decisions if relevant.`

### Task C: explicit request to use OpenPrecedent

Prompt:

`Do not edit code. Before answering, use any relevant prior decision-lineage from OpenPrecedent if available, then provide a short written recommendation only for improving repository navigation.`

## Findings

### 1. The skill was available, but OpenClaw did not call it by default

In Task A, OpenClaw did not call the OpenPrecedent skill.
It stayed on local task inspection behavior and produced a direct recommendation without precedent lookup.

Observed behavior:

- attempted local `read` on `README.md`
- fell back to local `find`
- returned a short README-navigation recommendation
- no `openprecedent` command was executed

Interpretation:

- merely installing the skill does not make OpenClaw use it for simple constrained recommendation tasks
- this is a valid negative result, not a failure of the logging path

### 2. When asked for consistency with prior decisions, OpenClaw preferred built-in memory search

In Task B, OpenClaw still did not call the OpenPrecedent skill.
Instead, it used built-in `memory_search`.

Observed behavior:

- invoked `memory_search`
- queried for earlier repository decisions and conventions
- received no memory results
- returned a lightweight navigation recommendation

Interpretation:

- the current skill wording is not yet strong enough to outrank OpenClaw's native memory route when the prompt only says "if relevant"
- real runtime usage currently competes with native memory behaviors rather than automatically replacing them

### 3. An explicit prompt caused real OpenClaw skill usage

In Task C, OpenClaw read the installed skill and executed the OpenPrecedent CLI.

Observed behavior:

- OpenClaw read the `openprecedent-decision-lineage` skill file
- OpenClaw executed:

```bash
openprecedent runtime decision-lineage-brief \
  --query-reason initial_planning \
  --task-summary "Do not edit code. Before answering, use any relevant prior decision-lineage from OpenPrecedent if available, then provide a short written recommendation only for improving repository navigation."
```

- the tool result returned successfully
- OpenPrecedent also wrote a runtime invocation record

Stored runtime invocation record:

- location: `/root/.openclaw-opv80/workspace/openprecedent-runtime-invocations.jsonl`
- count observed during validation: `1`

Interpretation:

- the live invocation path is real and working
- `#81` style invocation logging is sufficient to prove that OpenClaw called OpenPrecedent in the live loop

### 4. The live invocation returned an empty brief because it queried the isolated workspace database

Task C did call OpenPrecedent, but the returned brief had no matched cases and no semantic lineage fields.

Observed behavior:

- `matched_cases` was empty
- `task_frame` was `null`
- `accepted_constraints`, `success_criteria`, `rejected_options`, and `authority_signals` were empty

The key environmental fact is:

- OpenClaw executed the command from workdir `/root/.openclaw-opv80/workspace`
- OpenPrecedent therefore used `/root/.openclaw-opv80/workspace/openprecedent.db`
- that isolated workspace database had `0` cases, `0` events, and `0` decisions at validation time

Meanwhile, the repository working database did contain the imported prior case used earlier in validation.

Interpretation:

- the current runtime skill can be invoked successfully
- but its default database target is the OpenClaw workspace-local database, not the repository working database where the imported history existed
- this prevents the live skill from seeing the already captured history unless the environment explicitly wires a shared `OPENPRECEDENT_DB`

This is the main functional limit uncovered by the live validation.

### 5. The validation currently proves observability more strongly than quality gain

Task C proves that:

- OpenClaw can call the skill in a real runtime loop
- the invocation is logged
- the returned brief is inspectable

What it does not yet prove:

- that live semantic quality improved materially
- that prior task framing or constraints were actually inherited from a non-empty brief

The blocking reason is not lack of runtime invocation.
The blocking reason is that the live invocation queried an empty workspace-local database.

## What This Validation Establishes

This live pass establishes five concrete points:

1. The OpenClaw skill bundle is installable and discoverable in a real isolated profile.
2. OpenClaw does not naturally call the skill for every eligible constrained task.
3. OpenClaw may prefer built-in `memory_search` over the OpenPrecedent skill unless the prompt or future policy pushes more strongly toward lineage retrieval.
4. OpenClaw can successfully call `openprecedent runtime decision-lineage-brief` in a real loop.
5. Stable runtime value now depends on wiring the skill to the intended shared OpenPrecedent database and invocation-log paths.

## Current Limits

- this validation used only three short no-code tasks
- only one task triggered live OpenPrecedent usage
- the triggered call returned an empty brief because the runtime database was empty
- no automatic trigger policy was added to OpenClaw itself
- no quantitative claim about improved decision quality is justified yet

## Practical Conclusion

The current OpenClaw-facing runtime path is live but not yet fully product-effective.

What is proven:

- OpenClaw can install and call the OpenPrecedent decision-lineage skill
- OpenPrecedent can log the invocation in the live runtime workspace

What still needs work before stronger impact validation:

- OpenClaw runtime invocations must be wired to the intended shared OpenPrecedent database
- the skill or runtime policy may need stronger guidance so OpenClaw prefers it over built-in memory when semantic lineage is the right source

## Next Steps

- add a stable way for the OpenClaw skill to target a shared `OPENPRECEDENT_DB` and invocation log path
  - tracked in `#85` Wire the OpenClaw decision-lineage skill to a stable shared OpenPrecedent DB and invocation log
- repeat this live validation once the runtime can see non-empty prior lineage
- then evaluate whether returned lineage changes later task framing, constraint handling, authority handling, or success-criteria alignment in a measurable way
