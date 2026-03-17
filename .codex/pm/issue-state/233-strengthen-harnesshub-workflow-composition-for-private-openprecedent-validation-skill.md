---
type: issue_state
issue: 233
task: .codex/pm/tasks/real-history-quality/strengthen-harnesshub-workflow-composition-for-private-openprecedent-validation-skill.md
title: Strengthen HarnessHub workflow composition for private OpenPrecedent validation skill
status: done
---

## Summary

Improve HarnessHub's private OpenPrecedent validation skill so it offers a clearer one-skill entry surface for session composition plus lineage retrieval after the Rust CLI cutover, without changing HarnessHub's public workflow contract.

## Validated Facts

- The installed `openprecedent-harnesshub-validation` skill in HarnessHub is already Rust-CLI-based.
- HarnessHub's public `AGENTS.md` and `harness-issue-execution` skill do not mention or compose the private OpenPrecedent skill.
- Later HarnessHub rounds on `2026-03-15` and `2026-03-17` completed without new invocation records, which points to workflow-composition drift rather than retrieval degradation.
- The strengthened `openprecedent-harnesshub-validation` skill now carries both the default session-composition rule and the lineage-query workflow in one private skill.
- `./scripts/run-pytest.sh -q tests/test_harnesshub_skill_install_script.py` passed.
- `./scripts/run-agent-preflight.sh` passed.
- Refreshing the local HarnessHub installation now updates the single `openprecedent-harnesshub-validation` skill with the strengthened one-skill entry guidance.
- Later positive evidence under issue `#220` cannot yet be attributed solely to this issue because the user also introduced an additional locally maintained hidden AGENTS indirection to load the private skill more aggressively.

## Open Questions

- Whether later post-fix HarnessHub rounds would still restore more reliable `initial_planning` and `before_file_write` lineage invocation without the user's extra hidden local AGENTS indirection.

## Next Steps

- Merge the strengthened one-skill skill-surface fix.
- Continue observing later HarnessHub rounds under `#220` to measure whether invocation adherence improves.
- Avoid over-attributing later positive evidence to `#233` unless the hidden local-entry factor is isolated.

## Artifacts

- `skills/openprecedent-harnesshub-validation/SKILL.md`
- `scripts/install_harnesshub_skill.py`
