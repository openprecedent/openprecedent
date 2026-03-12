# Scripts

Utility scripts for local development, setup, migration, and tooling live here.

Notable operational entrypoints:

- `run-collector.sh` runs one collector pass with local-first defaults
- `run-e2e.sh` runs the standard local fixture-backed end-to-end validation flow
- `run-openclaw-live-validation.sh` prepares a reusable live OpenClaw validation workspace and summarizes runtime evidence
- `run-agent-preflight.sh` runs the standard local pre-push confidence checks for agent-driven work
- `run-codex-review-checkpoint.sh` creates or refreshes the local review note and the current-HEAD review proof before invoking native Codex `/review`
- `export_harnesshub_codex_round.py` exports one completed HarnessHub Codex development round as a minimal importable searchable-history bundle
- `import_harnesshub_codex_round.py` imports one exported HarnessHub round bundle into the shared runtime and extracts decisions
- `triage_pr_checks.py` summarizes and classifies current PR check results for faster CI diagnosis
- `install-collector-assets.sh` renders `systemd` / `cron` assets against the current repo path
