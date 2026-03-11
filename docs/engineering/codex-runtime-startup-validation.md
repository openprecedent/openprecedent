# Codex Runtime Startup Validation

## Goal

Record one durable end-to-end validation of the current Codex startup flow for OpenPrecedent.

The question under test was:

Can a new Codex project start from the documented runtime setup, run several decision-lineage requests, and verify that those requests are recorded and inspectable?

## Method

The validation used the repository-local harness:

```bash
OPENPRECEDENT_CODEX_LIVE_RESET=1 \
OPENPRECEDENT_CODEX_LIVE_AUTO_RUN=1 \
./scripts/run-codex-live-validation.sh
```

This run:

- prepared a fresh shared runtime home
- seeded prior Codex precedent fixtures into that runtime home
- executed three runtime workflow rounds
- listed the resulting runtime invocations
- inspected the latest invocation

## Round Coverage

The run covered three Codex runtime interaction points:

1. `initial_planning`
2. `before_file_write`
3. `after_failure`

This is enough to prove the current startup-and-recording loop, even though it is still narrower than a full long-running real project study.

## Observed Result

The current flow worked end to end.

Observed outcomes:

- the shared runtime home was created successfully
- prior Codex precedent history was seeded successfully
- three runtime invocations were recorded
- `list-decision-lineage-invocations` returned those records
- `inspect-decision-lineage-invocation` returned the latest invocation as an inspectable artifact
- the latest invocation still contained semantic matched case ids rather than empty output

The recorded query-reason sequence for the validation run was:

1. `initial_planning`
2. `before_file_write`
3. `after_failure`

The latest invocation summary reported:

- `invocation_count = 3`
- `latest_query_reason = after_failure`
- non-empty matched case ids:
  - `case_codex_live_semantic`
  - `case_codex_live_current`
  - `case_codex_live_operational`

## Why This Matters

This validation proves that a new project can start from:

- one shared runtime home
- one repository-local Codex workflow entrypoint
- one inspection path for verifying records

That is the minimum startup loop needed before `#131` can be executed in a later real project.

## Current Limits

This validation does not prove:

- natural long-running Codex behavior in a second real project
- cross-project portability of semantic decision lineage
- continuous automatic Codex history capture

Those remain part of `#131` and `#100`.

## Artifacts Produced By The Harness

The validation harness writes:

- `output/manifest.json`
- `output/20-invocation-list.json`
- `output/21-latest-invocation-summary.json`
- `output/22-latest-invocation-inspection.json`

These are the files a human or agent should inspect first when verifying a new Codex runtime setup.
