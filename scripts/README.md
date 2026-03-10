# Scripts

Utility scripts for local development, setup, migration, and tooling live here.

Notable operational entrypoints:

- `run-collector.sh` runs one collector pass with local-first defaults
- `run-e2e.sh` runs the standard local fixture-backed end-to-end validation flow
- `run-agent-preflight.sh` runs the standard local pre-push confidence checks for agent-driven work
- `install-collector-assets.sh` renders `systemd` / `cron` assets against the current repo path
