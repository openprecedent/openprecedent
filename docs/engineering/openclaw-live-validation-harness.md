# OpenClaw Live Validation Harness

## Goal

Provide a reusable local harness entrypoint for real OpenClaw runtime validation work so integration debugging no longer depends on remembering ad hoc shell sequences.

This harness is intentionally narrower than deployment automation.
It focuses on preparing a validation workspace, seeding shared prior history when needed, and collecting inspectable runtime artifacts after a live OpenClaw turn.

## Entry Point

Run:

```bash
./scripts/run-openclaw-live-validation.sh
```

By default this prepares a workspace under `/tmp/openprecedent-openclaw-live` with:

- `runtime-home/` for the shared `OPENPRECEDENT_HOME`
- a synchronized installed OpenClaw skill bundle under the target profile workspace that points at that same runtime home
- `output/manifest.json` for the validation manifest
- `output/03-invocation-summary.json` for the latest runtime invocation summary
- `prompt.txt` for the current prompt under test
- `launch-openclaw-gateway.sh` for the isolated gateway launch command
- `next-steps.txt` for the remaining live run steps

## Seeding Shared Prior History

If the live validation needs shared prior lineage, set:

```bash
OPENPRECEDENT_LIVE_SEED_SESSION_FILE=/path/to/session.jsonl
OPENPRECEDENT_LIVE_SEED_SESSION_ID=my-session
OPENPRECEDENT_LIVE_SEED_CASE_ID=case_live_seed
```

Then rerun the harness.
It will:

- create a minimal temporary `sessions.json`
- import the named session into the shared runtime home
- extract decisions for the seeded case
- synchronize the installed `openprecedent-decision-lineage` skill bundle so its `OPENPRECEDENT_HOME` matches the harness runtime home
- write the import and extract results into `output/01-seed-import.json` and `output/02-seed-extract.json`

The harness preserves seeded state across reruns unless `OPENPRECEDENT_LIVE_RESET=1` is set.

## Evidence Collection

After a live OpenClaw turn, rerun the harness.
It refreshes `output/03-invocation-summary.json` from the shared runtime invocation log and records:

- invocation count
- latest invocation id
- latest `recorded_at`
- latest `query_reason`
- latest matched case ids
- latest task summary

This keeps the most important runtime evidence in one stable local location even when the OpenClaw session itself lives elsewhere.

## Recommended Workflow

1. Prepare the live workspace with `./scripts/run-openclaw-live-validation.sh`.
2. If needed, seed prior history into the shared runtime home.
3. Start the isolated OpenClaw gateway with `./launch-openclaw-gateway.sh`.
4. Run the target prompt from `prompt.txt`.
5. Rerun the harness to refresh the invocation summary.
6. Inspect `output/manifest.json`, `output/03-invocation-summary.json`, and any seeded import artifacts.

## Notes

- This harness does not try to drive the OpenClaw UI or gateway automatically.
- It standardizes the workspace, shared runtime home, installed skill bundle, and artifact capture around the live validation.
- It is meant for runtime integration debugging and later research validation, not for merge-gating CI.
