# Tooling Setup

## Repository-Local Setup

The repository already includes:

- `markdownlint` GitHub Actions workflow for Markdown review
- `python-ci` GitHub Actions workflow for dependency install and tests
- `feishu-pr-notify` GitHub Actions workflow for pull request review notifications
- a local Git pre-push hook that requires a Codex review note
- `scripts/run-codex-review-checkpoint.sh` as the preferred local checkpoint for invoking native Codex `/review`
- `scripts/run-agent-preflight.sh` for the standard local pre-push confidence checks
- `scripts/triage_pr_checks.py` for local CI failure classification against current PR checks
- `scripts/run-e2e.sh` for the standard local fixture-backed end-to-end runtime validation path
- `scripts/run-openclaw-live-validation.sh` for preparing a reusable live OpenClaw validation workspace and summarizing runtime evidence
- `python3 -m openprecedent.codex_pm issue-state-init <task-path>` for preserving issue-scoped working state across longer agent work

To enable the local hook:

```bash
./scripts/install-hooks.sh
```

After that, each push requires a `.codex-review` file in the repository root unless you explicitly bypass the hook.
The local hook also expects your branch to contain the latest `upstream/main` by default, so stale branches are caught before push.
When `gh` can resolve the current PR body, the hook also performs a local issue/task closure sync check before push.

## Codex Review Hook

Before pushing, run:

```bash
./scripts/run-codex-review-checkpoint.sh
```

This is the preferred local checkpoint for invoking native Codex `/review`.
The script creates a `.codex-review` template if one does not exist and reminds you to run `/review` before push.

Then update `.codex-review` with a short review note.

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

For a normal local readiness pass before push, run:

```bash
./scripts/run-agent-preflight.sh
```

This checks the local review note, blocks reused merged branches, runs `pytest`, runs `markdownlint` when available locally, and performs a local PR closure sync check when a PR body is available through `gh`.
It also checks that your branch contains the configured base ref, which defaults to `upstream/main`.
For issue-scoped branches, it also runs a lightweight issue-state check. By default this only warns if an `in_progress` issue is missing a state document.

Set `OPENPRECEDENT_PREFLIGHT_RUN_E2E=1` if you also want the standard E2E path included in the same pass.
Set `OPENPRECEDENT_PREFLIGHT_ENFORCE_ISSUE_STATE=1` if you want preflight to fail until the issue state document exists.

## Issue-Scoped Development State

For longer-running issues, initialize a local state document from the matching task twin:

```bash
python3 -m openprecedent.codex_pm issue-state-init .codex/pm/tasks/<epic>/<task>.md
```

This creates a repository-local issue state document under `.codex/pm/issue-state/` and records its path back into the task metadata.
Use it to keep validated facts, open questions, next steps, and key artifacts in one stable place as the work evolves across sessions.

For runtime-affecting pull requests, run:

```bash
OPENPRECEDENT_PREFLIGHT_RUN_E2E=1 ./scripts/run-agent-preflight.sh
```

or run the E2E script directly:

```bash
./scripts/run-e2e.sh
```

The detailed merge checklist lives in
[`docs/engineering/merge-validation.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/merge-validation.md).

## Live OpenClaw Validation Harness

For runtime integration work that must exercise the real OpenClaw loop rather than fixture-only replay, use:

```bash
./scripts/run-openclaw-live-validation.sh
```

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
