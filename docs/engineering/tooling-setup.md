# Tooling Setup

## Repository-Local Setup

The repository already includes:

- `markdownlint` GitHub Actions workflow for Markdown review
- a local Git pre-push hook that requires a Codex review note

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

## GitHub App Recommendations

These still require manual installation from GitHub by a repository admin:

- CodeFactor
- CodeAnt AI

Recommended rollout:

1. enable repository-local Markdown checks
2. enable Codex pre-push review hook
3. install CodeFactor
4. install CodeAnt AI
