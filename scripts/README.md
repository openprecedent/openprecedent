# Scripts

Utility scripts for local development, setup, migration, and tooling live here.
The supported public product interface is the Rust `openprecedent` CLI.
Scripts in this directory are repository-local helpers around that CLI or around repository workflow tooling.

Notable repository-local helper entrypoints:

- `run-collector.sh` runs one collector pass with local-first defaults as an internal wrapper around `openprecedent capture openclaw collect-sessions`
- `run-e2e.sh` runs the standard local fixture-backed end-to-end validation flow
- `run-openclaw-live-validation.sh` prepares a reusable live OpenClaw validation workspace and summarizes runtime evidence as a repository-local live harness
- `run-agent-preflight.sh` runs the standard local pre-push confidence checks for agent-driven work
- `run-pytest.sh` resolves the repository-local pytest runner before falling back to global Python or `pytest`
- `run-codex-session-start.sh` restores active issue and PR context and restates the repository's default direct-fix workflow at session start
- `run-codex-review-checkpoint.sh` creates or refreshes the local review note and the current-HEAD review proof before invoking native Codex `/review`
- `python3 -m openprecedent.codex_pm reconcile-task-statuses` diagnoses local task drift against remote issue state before PR creation
- `lib/openprecedent-rust-cli.sh` resolves the repository-local Rust `openprecedent` binary for internal harness scripts
- `export_harnesshub_codex_round.py` exports one completed HarnessHub Codex development round as a minimal importable searchable-history bundle
- `import_harnesshub_codex_round.py` imports one exported HarnessHub round bundle into the shared runtime and extracts decisions
- `sync_harnesshub_shared_runtime.py` backfills and incrementally auto-seeds the shared runtime from completed HarnessHub rounds
- `run-codex-decision-lineage-workflow.sh` wraps a repo-local Rust CLI lineage query plus optional latest-invocation inspection for Codex development validation
- `run-harnesshub-decision-lineage-workflow.sh` auto-syncs completed HarnessHub rounds into the shared runtime before calling the Rust CLI lineage brief surface
- `run-harnesshub-matched-case-validation.sh` imports one prior HarnessHub round bundle, runs a later semantically related Rust CLI lineage query, and writes matched-case summary artifacts
- `run-codex-live-validation.sh` runs the repository's Codex live validation harness against the Rust CLI
- `install_harnesshub_skill.py` installs the OpenPrecedent-maintained private HarnessHub skill bundle into a local HarnessHub workspace, including the workflow-composition companion skill and the validation skill
- `triage_pr_checks.py` summarizes and classifies current PR check results for faster CI diagnosis
- `install-collector-assets.sh` renders `systemd` / `cron` assets against the current repo path
