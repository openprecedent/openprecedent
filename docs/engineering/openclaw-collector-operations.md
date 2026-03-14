# OpenClaw Collector Operations

## Goal

This document is the operational landing path for the MVP collector.

It covers:

- the local wrapper used by automation
- the recommended `systemd` timer setup
- the fallback `cron` setup
- the evaluation/report command for real collected sessions

For the first validated live rollout and its observed caveats, see
[`docs/engineering/openclaw-collector-rollout-validation.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-collector-rollout-validation.md).

## Wrapper Script

Use the Rust CLI as the supported collection surface. [`scripts/run-collector.sh`](/workspace/02-projects/incubation/openprecedent/scripts/run-collector.sh) remains only as an internal repository-local convenience wrapper for scheduled jobs.

The wrapper prefers the repository-local `.venv/bin/openprecedent` binary when it exists, then falls back to `openprecedent` on `PATH`. This keeps scheduled runs aligned with the checked-out repository environment without requiring a separate global install.

Default environment variables:

- `OPENPRECEDENT_DB`
- `OPENPRECEDENT_COLLECTOR_STATE`
- `OPENCLAW_SESSIONS_ROOT`
- `OPENPRECEDENT_COLLECT_LIMIT`
- `OPENPRECEDENT_AGENT_ID`

The script runs:

```bash
openprecedent capture openclaw collect-sessions --limit 1
```

against the configured session root and collector state file.

## systemd

Render and install the user units with:

```bash
./scripts/install-collector-assets.sh systemd
```

This writes path-resolved unit files into `~/.config/systemd/user/` using the current repository root.

The source templates live at:

- [`deploy/systemd/openprecedent-collector.service`](/workspace/02-projects/incubation/openprecedent/deploy/systemd/openprecedent-collector.service)
- [`deploy/systemd/openprecedent-collector.timer`](/workspace/02-projects/incubation/openprecedent/deploy/systemd/openprecedent-collector.timer)

Then enable the timer:

```bash
systemctl --user daemon-reload
systemctl --user enable --now openprecedent-collector.timer
systemctl --user list-timers openprecedent-collector.timer
```

Useful checks:

```bash
systemctl --user status openprecedent-collector.timer
journalctl --user -u openprecedent-collector.service -n 50 --no-pager
```

If `systemctl --user` cannot reach the user bus in the target environment, use the documented `cron` path instead of trying to force a partially working user-service setup.

## cron

If `systemd --user` is unavailable, use the template at
[`deploy/cron/openprecedent-collector.cron`](/workspace/02-projects/incubation/openprecedent/deploy/cron/openprecedent-collector.cron).

Render a repo-path-aware crontab file with:

```bash
./scripts/install-collector-assets.sh cron
crontab runtime/openprecedent-collector.cron
crontab -l
```

The rendered crontab writes the absolute home-directory session path directly into `OPENCLAW_SESSIONS_ROOT` because cron variable assignments do not expand `$HOME` reliably.

## Real Session Evaluation

After the collector has imported a few sessions, generate a real-session report with:

```bash
openprecedent eval captured-openclaw-sessions \
  --sessions-root "$HOME/.openclaw/agents/main/sessions" \
  --state-file "$(pwd)/runtime/openprecedent-collector-state.json" \
  --report-file "$(pwd)/runtime/collected-eval-report.json"
```

Run this from the repository root so the report reads the same collector state written by the installed wrapper.

This report summarizes:

- how many collected sessions were evaluated
- completion/failure mix
- average event and decision counts
- decision-type distribution
- unsupported OpenClaw session record types that were skipped
- whether each case produced file writes, recovery decisions, and usable precedents

Use `--format json` for machine-readable output to stdout.
