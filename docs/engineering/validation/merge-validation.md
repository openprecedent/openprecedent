# Merge Validation

## Goal

Define the repository-local validation baseline contributors should use before merging changes that affect the shipped OpenPrecedent runtime path.

## Standard E2E Script

Run the standard local end-to-end validation flow with:

```bash
./scripts/run-e2e.sh
```

By default this script uses:

- E2E root: `/tmp/openprecedent-openclaw-journey`
- fixture sessions: `tests/fixtures/openclaw_sessions/`
- runtime binary: `.venv/bin/openprecedent` when available, otherwise `openprecedent` on `PATH`

You can override those defaults with:

- `OPENPRECEDENT_E2E_ROOT`
- `OPENPRECEDENT_E2E_FIXTURE_ROOT`
- `OPENPRECEDENT_BIN`

The script writes step-by-step JSON outputs under:

- `$OPENPRECEDENT_E2E_ROOT/output/`

This path is intentionally inspectable so a reviewer can spot which stage failed without re-running commands by hand.

## When To Run It

Run `./scripts/run-e2e.sh` before merge when a PR changes any of these areas:

- `src/openprecedent/`
- runtime CLI behavior
- collector behavior or state handling
- replay, decision extraction, or precedent retrieval behavior
- evaluation flows or fixture-backed local runtime paths

For docs-only or narrow PM-governance changes, the smaller relevant checks are enough.

## Merge Checklist

- run `./scripts/run-e2e.sh` for runtime-affecting PRs
- confirm the script exits successfully
- inspect `10-eval-fixtures.json` and verify `failed_cases` is `0`
- inspect `11-eval-collected-openclaw-sessions.json` and verify collected-session evaluation completed
- include the exact validation commands in the PR body when the E2E script was part of merge validation

## Baseline Source

The script mirrors the documented baseline in
[`openclaw-full-user-journey-validation.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-full-user-journey-validation.md)
rather than introducing a separate E2E path.
