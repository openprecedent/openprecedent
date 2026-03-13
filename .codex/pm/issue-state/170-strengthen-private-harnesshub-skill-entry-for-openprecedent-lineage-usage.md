---
type: issue_state
issue: 170
task: .codex/pm/tasks/codex-runtime-research/strengthen-private-harnesshub-skill-entry-for-openprecedent-lineage-usage.md
title: Strengthen private HarnessHub skill entry for OpenPrecedent lineage usage
status: done
---

## Summary

Maintain the HarnessHub validation skill in OpenPrecedent as the canonical source, then install that source into HarnessHub so the private trial skill stays aligned while the repository itself remains publicly decoupled from OpenPrecedent.

## Validated Facts

- OpenPrecedent already has a maintained installable skill pattern under `skills/openprecedent-decision-lineage/`
- HarnessHub currently relies on a copied private skill under `.codex/skills/openprecedent-harnesshub-validation/`
- issue `#73` showed that the current copied skill is too easy to skip because its entry choreography is weaker than HarnessHub's main issue-delivery path
- a canonical source plus install step keeps the external trial surface consistent without moving OpenPrecedent into HarnessHub's public workflow

## Open Questions

- whether the current trial should later grow a dedicated sync wrapper beyond the initial install script

## Next Steps

- add the canonical skill source under `skills/openprecedent-harnesshub-validation/`
- add the installer that writes into a local HarnessHub checkout
- verify the installed bundle rewrites OpenPrecedent repo-root placeholders correctly
- update OpenPrecedent docs to point maintainers at the canonical source and install path

## Artifacts

- `skills/openprecedent-harnesshub-validation/`
- `scripts/install_harnesshub_skill.py`
