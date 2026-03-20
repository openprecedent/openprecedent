# Tooling Setup

## Repository-Local Setup

The repository already includes:

- `markdownlint` GitHub Actions workflow for Markdown review
- `python-ci` GitHub Actions workflow for dependency install and tests
- `coverage` GitHub Actions workflow for Python and Rust coverage summaries plus uploaded reports
- `feishu-pr-notify` GitHub Actions workflow for pull request review notifications
- a local Git pre-push hook that requires a Codex review note
- `scripts/run-codex-review-checkpoint.sh` as the preferred local checkpoint for invoking native Codex `/review`
- `scripts/run-agent-preflight.sh` for the standard local pre-push confidence checks
- `scripts/run-coverage.sh` for repository-local Python and Rust coverage generation plus a combined markdown summary
- `scripts/check_mvp_coverage_gate.py` for enforcing the scoped `90%` MVP release coverage gate
- `scripts/run-pytest.sh` for repository-local pytest resolution before falling back to global commands
- `scripts/run-codex-session-start.sh` for restoring branch, issue, task, issue-state, and PR context at the start of a Codex session
- `scripts/triage_pr_checks.py` for local CI failure classification against current PR checks
- `scripts/run-e2e.sh` for the standard local fixture-backed end-to-end runtime validation path
- `scripts/run-openclaw-live-validation.sh` for preparing a reusable live OpenClaw validation workspace and summarizing runtime evidence
- `python3 -m openprecedent.codex_pm issue-state-init <task-path>` for preserving issue-scoped working state across longer agent work

To enable the local hook:

```bash
./scripts/install-hooks.sh
```

After that, each push requires both a `.codex-review` file and a current `.codex-review-proof` file in the repository root unless you explicitly bypass the hook.
The local hook also expects your branch to contain the latest `upstream/main` by default, so stale branches are caught before push.
When `gh` can resolve the current PR body, the hook also performs a local issue/task closure sync check before push.

For PR creation, prefer the repository-local command:

```bash
python3 -m openprecedent.codex_pm pr-create .codex/pm/tasks/<epic>/<task>.md --tests "<cmd>"
```

This command forces the upstream target repo and explicit fork head reference instead of relying on whatever repository context `gh` infers from the local clone.
It now also fails fast if the matching task twin is not already marked `done` before PR creation.
Fresh task twins created through `python3 -m openprecedent.codex_pm task-new ...` now also use markdownlint-clean placeholder section bodies by default, so new PM documents do not require manual spacing cleanup before review.

To diagnose or reconcile local task drift against remote GitHub issue state, use:

```bash
python3 -m openprecedent.codex_pm reconcile-task-statuses
python3 -m openprecedent.codex_pm reconcile-task-statuses --issue <number> --apply
```

Use `--apply` only for the safe reconciliation path that marks local tasks `done` when the linked remote issue is already closed.

## Codex Review Hook

Before pushing, run:

```bash
./scripts/run-codex-review-checkpoint.sh
```

This is the preferred local checkpoint for invoking native Codex `/review`.
The script creates or refreshes a `.codex-review-proof` file for the current `HEAD`, creates a `.codex-review` template if one does not exist, and reminds you to run `/review` before push.

Then update `.codex-review` with a short review note.
Pushes now fail if the proof does not match the current `HEAD`, if the note still contains the placeholder review text, or if the note was not updated after the latest checkpoint refresh.

Recommended format:

```text
scope reviewed: docs/engineering + schema changes
findings: no findings
remaining risks: dependencies not installed locally, tests not executed
```

This hook does not replace human judgment. It creates a minimal review checkpoint before code leaves the local branch.
It also acts as a branch-freshness guardrail: if your branch no longer contains the latest `upstream/main`, rebase before pushing.
If the current PR body includes `Closes #<issue>`, the hook now tries to verify that the matching local task file is also updated consistently before allowing the push.

## Merge Validation

## Codex Session Start

When starting or resuming a Codex session in this repository, run:

```bash
./scripts/run-codex-session-start.sh
```

The command surfaces the current branch, issue number, matching local task twin, issue-state availability, and open PR context when available.
It also restates the repository's default execution policy:

- when the user reports a concrete problem, directly diagnose, implement, verify, and close the loop unless the work is destructive, high-risk, or blocked
- prefer repository-local execution paths such as `./scripts/run-pytest.sh`
- keep issue, task twin, issue-state, and PR closure state synchronized

Use this startup entrypoint before substantive work so a fresh session does not rely on prior chat memory alone.

## Merge Validation

For a normal local readiness pass before push, run:

```bash
./scripts/run-agent-preflight.sh
```

This checks the local review note, blocks reused merged branches, runs `pytest`, runs `markdownlint` when available locally, and performs a local PR closure sync check when a PR body is available through `gh`.
It also checks that your branch contains the configured base ref, which defaults to `upstream/main`.
For issue-scoped branches, it also runs a lightweight issue-state check. By default this only warns if an `in_progress` issue is missing a state document.
When the current diff includes Rust-affecting files such as `Cargo.toml`, `Cargo.lock`, or files under `rust/`, preflight also runs `cargo test`.
The intended workflow is to correct task status before PR creation rather than relying on push-time or CI-time closure sync failures.

For direct local test runs, prefer:

```bash
./scripts/run-pytest.sh -q tests/test_preflight_script.py
```

The wrapper resolves `OPENPRECEDENT_PYTHON_BIN`, repository-local `.venv` entrypoints, and only then falls back to global Python or `pytest` binaries.
Do not treat a missing global `pytest` as a blocker until that local resolution path has been exhausted.

## Coverage Reporting

For a local MVP release-readiness coverage pass, run:

```bash
./scripts/run-coverage.sh
```

That command writes standard coverage outputs under `coverage/`, including:

- `coverage/python/coverage.json`
- `coverage/python/coverage.xml`
- `coverage/python/html/`
- `coverage/rust/coverage-summary.json`
- `coverage/rust/lcov.info`
- `coverage/rust/html/`
- `coverage/coverage-summary.md`

On GitHub, `.github/workflows/coverage.yml` runs the same coverage flow, publishes the markdown summary into the workflow run, uploads the `coverage/` directory as the `coverage-report` artifact, and updates a sticky pull-request comment when possible.

Use that workflow output as the standard source of truth for MVP release readiness. The workflow now also runs:

```bash
python3 scripts/check_mvp_coverage_gate.py coverage/python/coverage.json coverage/rust/coverage-summary.json
```

That gate measures the scoped MVP release surface rather than every repository-local support path:

- Python: `src/openprecedent/**/*.py`, excluding `src/openprecedent/codex_pm.py`
- Rust: release implementation library crates under `rust/**/src/lib.rs`, excluding `rust/openprecedent-cli/src/main.rs`

The Rust CLI shell remains covered through command-level contract tests and the later release validation checklist rather than this line-coverage threshold.

For the full release-blocking checklist that combines preflight, coverage, CLI smoke, and the minimal end-to-end MVP loop, see:

- [mvp-release-validation-checklist.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-validation-checklist.md)

Set `OPENPRECEDENT_PREFLIGHT_RUN_E2E=1` if you also want the standard E2E path included in the same pass.
Set `OPENPRECEDENT_PREFLIGHT_ENFORCE_ISSUE_STATE=1` if you want preflight to fail until the issue state document exists.

## Issue-Scoped Development State

For longer-running issues, initialize a local state document from the matching task twin:

```bash
python3 -m openprecedent.codex_pm issue-state-init .codex/pm/tasks/<epic>/<task>.md
```

This creates a repository-local issue state document under `.codex/pm/issue-state/` and records its path back into the task metadata.
Use it to keep validated facts, open questions, next steps, and key artifacts in one stable place as the work evolves across sessions.
The standard session-start command will warn if an in-progress issue branch is missing this state document.

For runtime-affecting pull requests, run:

```bash
OPENPRECEDENT_PREFLIGHT_RUN_E2E=1 ./scripts/run-agent-preflight.sh
```

or run the E2E script directly:

```bash
./scripts/run-e2e.sh
```

The detailed merge checklist lives in
[`docs/engineering/validation/merge-validation.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/merge-validation.md).

## Live OpenClaw Validation Harness

For runtime integration work that must exercise the real OpenClaw loop rather than fixture-only replay, use:

```bash
./scripts/run-openclaw-live-validation.sh
```

Treat this script as a repository-local harness entrypoint, not as part of the supported public product interface.

The harness prepares a stable local workspace, shared `OPENPRECEDENT_HOME`, prompt file, gateway launcher, and structured artifact directory under `/tmp/openprecedent-openclaw-live` by default.
It also synchronizes the installed OpenClaw skill bundle in the target profile workspace so the skill points at that same shared runtime home instead of falling back to a different default path.

For issue-driven runtime integration work, pair that script with the local workflow skill:

- [.codex/skills/openclaw-live-validation/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/openclaw-live-validation/SKILL.md)

To seed shared prior history before a live run, point it at an existing OpenClaw session transcript:

```bash
OPENPRECEDENT_LIVE_SEED_SESSION_FILE=/path/to/session.jsonl \
OPENPRECEDENT_LIVE_SEED_SESSION_ID=my-session \
OPENPRECEDENT_LIVE_SEED_CASE_ID=case_live_seed \
./scripts/run-openclaw-live-validation.sh
```

After the live OpenClaw turn, re-run the harness to refresh `output/03-invocation-summary.json` from the shared runtime invocation log.

## CI Failure Triage

When a PR check fails and you want a faster local summary than manually opening each run, use:

```bash
python3 ./scripts/triage_pr_checks.py --pr <number>
```

If you are already on the PR branch, you can usually omit `--pr` and let `gh` resolve the current PR.

The script classifies the repository's current checks into a few higher-level categories such as:

- test regression
- docs lint
- workflow policy
- notification-only

It is intended as a diagnosis helper, not an auto-fix tool.

## GitHub App Recommendations

These still require manual installation from GitHub by a repository admin:

- CodeFactor
- CodeAnt AI

Recommended rollout:

1. enable repository-local Markdown checks
2. enable Python CI checks on pull requests
3. configure `FEISHU_WEBHOOK_URL` for review notifications
4. enable Codex pre-push review hook
5. install CodeFactor
6. install CodeAnt AI
