# HarnessHub Validation Reference

This reference is for local HarnessHub development where OpenPrecedent should be available by default as a private precedent layer without becoming a public repository dependency.

## Purpose

HarnessHub is the current real-project validation target for OpenPrecedent.
OpenPrecedent should function as a local private development aid for normal HarnessHub work, while HarnessHub must remain usable without OpenPrecedent for normal contributors and runtime users.

## Core Rules

- Do not expose OpenPrecedent setup as a normal HarnessHub repository requirement.
- Do not add project docs or helper scripts that make HarnessHub appear to depend on OpenPrecedent.
- Use a shared runtime home:
  - `OPENPRECEDENT_HOME=$HOME/.openprecedent/runtime`
- Query lineage only at:
  - `initial_planning`
  - `before_file_write`
  - `after_failure`

## Entry Guidance

- Start with a local availability probe against the Rust `openprecedent` CLI or a local build under `{{OPENPRECEDENT_REPO_ROOT}}/target/`.
- If the probe fails, continue the task normally instead of redefining HarnessHub's public workflow.
- If the probe succeeds, run the minimum `initial_planning` query before implementation.
- Compose this skill with HarnessHub's issue-execution skill rather than replacing the main delivery path.

## Progressive Disclosure

Only load the following OpenPrecedent-side files when they materially affect the current task:

- `{{OPENPRECEDENT_REPO_ROOT}}/docs/engineering/validation/harnesshub-real-project-validation-report.md`
- `{{OPENPRECEDENT_REPO_ROOT}}/.codex/pm/issue-state/131-validate-codex-real-project-decision-lineage-reuse.md`
- `{{OPENPRECEDENT_REPO_ROOT}}/.codex/pm/tasks/codex-runtime-research/validate-codex-real-project-decision-lineage-reuse.md`

Use those files to shape validation timing, naming, scope control, and interpretation only when the current task needs deeper research context.
