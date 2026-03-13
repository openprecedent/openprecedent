---
type: issue_state
issue: 186
task: .codex/pm/tasks/public-cli-foundation/migrate-skills-and-validation-workflows-from-scripts-to-rust-cli.md
title: Migrate skills and validation workflows from scripts to the Rust CLI
status: in_progress
---

## Summary

Skill-driven usage and the main Codex/HarnessHub validation harnesses now call the Rust `openprecedent` CLI directly instead of treating repository-local workflow scripts or the Python CLI as the public automation surface.

## Validated Facts

- `scripts/run-codex-decision-lineage-workflow.sh` now resolves the Rust CLI and uses `lineage brief` plus `lineage invocation inspect` instead of shelling out to the Python CLI
- `scripts/run-codex-live-validation.sh`, `scripts/run-harnesshub-decision-lineage-workflow.sh`, and `scripts/run-harnesshub-matched-case-validation.sh` now execute Rust CLI lineage, capture, decision, and inspection commands directly for their runtime query paths
- the local Codex lineage skill, the installable HarnessHub validation skill, and the OpenClaw lineage skill now document direct Rust CLI usage rather than script-path invocation
- key public validation docs and regression tests now reference the Rust command tree (`capture`, `lineage`, `decision`) rather than the old `runtime` command bucket or repository-local script entrypoints
- targeted local regression coverage passed for the updated scripts, skills, docs assertions, and Rust workspace contracts

## Open Questions

- broader documentation cleanup outside the direct skill and validation workflow surfaces still remains for the final public cutover issue

## Next Steps

- mark the task twin `done`
- open the child PR against `codex/issue-172-rust-public-cli`
- merge this slice, then continue with `#187` for the public cutover and Python/script removal phase

## Artifacts

- `scripts/lib/openprecedent-rust-cli.sh`
- `scripts/run-codex-decision-lineage-workflow.sh`
- `scripts/run-codex-live-validation.sh`
- `scripts/run-harnesshub-decision-lineage-workflow.sh`
- `scripts/run-harnesshub-matched-case-validation.sh`
- `.codex/skills/codex-runtime-decision-lineage/SKILL.md`
- `skills/openprecedent-decision-lineage/SKILL.md`
- `skills/openprecedent-harnesshub-validation/SKILL.md`
- `docs/engineering/codex-runtime-decision-lineage-workflow.md`
- `docs/engineering/codex-runtime-startup-guide.md`
- `docs/engineering/using-openprecedent.md`
