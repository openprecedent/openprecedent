# OpenClaw Collector Operations

## Goal

This document is the operational landing path for the MVP collector.

It covers:

- the local wrapper used by automation
- the recommended `systemd` timer setup
- the fallback `cron` setup
- the evaluation/report command for real collected sessions

## Wrapper Script

Use [`scripts/run-collector.sh`](/workspace/02-projects/incubation/openprecedent/scripts/run-collector.sh) as the single entrypoint for scheduled collection.

Default environment variables:

- `OPENPRECEDENT_DB`
- `OPENPRECEDENT_COLLECTOR_STATE`
- `OPENCLAW_SESSIONS_ROOT`
- `OPENPRECEDENT_COLLECT_LIMIT`
- `OPENPRECEDENT_AGENT_ID`

The script runs:

```bash
openprecedent runtime collect-openclaw-sessions --limit 1
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

## cron

If `systemd --user` is unavailable, use the template at
[`deploy/cron/openprecedent-collector.cron`](/workspace/02-projects/incubation/openprecedent/deploy/cron/openprecedent-collector.cron).

Render a repo-path-aware crontab file with:

```bash
./scripts/install-collector-assets.sh cron
crontab runtime/openprecedent-collector.cron
crontab -l
```

## Real Session Evaluation

After the collector has imported a few sessions, generate a real-session report with:

```bash
openprecedent eval collected-openclaw-sessions \
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

Use `--json` for machine-readable output to stdout.
