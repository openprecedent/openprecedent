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

## Open Questions

- Which private workflow surface can improve composition without making HarnessHub publicly depend on OpenPrecedent?

## Next Steps

- Add a private composition companion skill to the installed HarnessHub bundle.
- Extend the installer and docs to treat the HarnessHub integration as a private skill bundle rather than one isolated validation skill.
- Verify the installed local HarnessHub checkout now contains both private skills.

## Artifacts

- `skills/openprecedent-harnesshub-composition/SKILL.md`
- `skills/openprecedent-harnesshub-validation/SKILL.md`
- `scripts/install_harnesshub_skill.py`
