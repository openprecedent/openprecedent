# Tooling Setup

## Repository-Local Setup

The repository already includes:

- `markdownlint` GitHub Actions workflow for Markdown review
- `python-ci` GitHub Actions workflow for dependency install and tests
- `feishu-pr-notify` GitHub Actions workflow for pull request review notifications
- a local Git pre-push hook that requires a Codex review note
- `scripts/run-agent-preflight.sh` for the standard local pre-push confidence checks
- `scripts/run-e2e.sh` for the standard local fixture-backed end-to-end runtime validation path

To enable the local hook:

```bash
./scripts/install-hooks.sh
```

After that, each push requires a `.codex-review` file in the repository root unless you explicitly bypass the hook.

## Codex Review Hook

Before pushing, create a short review note in `.codex-review`.

Recommended format:

```text
scope reviewed: docs/engineering + schema changes
findings: no findings
remaining risks: dependencies not installed locally, tests not executed
```

This hook does not replace human judgment. It creates a minimal review checkpoint before code leaves the local branch.

## Merge Validation

For a normal local readiness pass before push, run:

```bash
./scripts/run-agent-preflight.sh
```

This checks the local review note, blocks reused merged branches, runs `pytest`, runs `markdownlint` when available locally, and performs a local PR closure sync check when a PR body is available through `gh`.

Set `OPENPRECEDENT_PREFLIGHT_RUN_E2E=1` if you also want the standard E2E path included in the same pass.

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
