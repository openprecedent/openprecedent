---
type: issue_state
issue: 233
task: .codex/pm/tasks/real-history-quality/strengthen-harnesshub-workflow-composition-for-private-openprecedent-validation-skill.md
title: Strengthen HarnessHub workflow composition for private OpenPrecedent validation skill
status: in_progress
---

## Summary

Improve HarnessHub's private OpenPrecedent skill composition so local issue-delivery sessions are more likely to include the validation layer after the Rust CLI cutover, without changing HarnessHub's public workflow contract.

## Validated Facts

- The installed `openprecedent-harnesshub-validation` skill in HarnessHub is already Rust-CLI-based.
- HarnessHub's public `AGENTS.md` and `harness-issue-execution` skill do not mention or compose the private OpenPrecedent skill.
- Later HarnessHub rounds on `2026-03-15` and `2026-03-17` completed without new invocation records, which points to workflow-composition drift rather than retrieval degradation.
- The fix now installs a second private skill, `openprecedent-harnesshub-composition`, so the local HarnessHub bundle exposes an explicit session-composition surface in addition to the validation skill.
- `./scripts/run-pytest.sh -q tests/test_harnesshub_skill_install_script.py` passed.
- `./scripts/run-agent-preflight.sh` passed.
- Refreshing the local HarnessHub bundle now produces both `openprecedent-harnesshub-composition` and `openprecedent-harnesshub-validation` under `.codex/skills/`.

## Open Questions

- Whether later post-fix HarnessHub rounds actually restore more reliable `initial_planning` and `before_file_write` lineage invocation under issue `#220`.

## Next Steps

- Open the issue PR for `#233`.
- Merge the bundle-composition fix.
- Continue observing later HarnessHub rounds under `#220` to measure whether invocation adherence improves.

## Artifacts

- `skills/openprecedent-harnesshub-composition/SKILL.md`
- `skills/openprecedent-harnesshub-validation/SKILL.md`
- `scripts/install_harnesshub_skill.py`
