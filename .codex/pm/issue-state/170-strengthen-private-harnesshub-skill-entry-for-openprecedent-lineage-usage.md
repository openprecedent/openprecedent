---
type: issue_state
issue: 170
task: .codex/pm/tasks/codex-runtime-research/strengthen-private-harnesshub-skill-entry-for-openprecedent-lineage-usage.md
title: Strengthen private HarnessHub skill entry for OpenPrecedent lineage usage
status: done
delivery_stage: pr_opened
pr_url: https://github.com/openprecedent/openprecedent/pull/171
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

- wait for PR `#171` review and merge
- if the trial later needs stronger automation than install-time sync, evaluate a follow-up sync wrapper rather than reintroducing direct HarnessHub-side edits to the copied skill bundle

## Artifacts

- `skills/openprecedent-harnesshub-validation/`
- `scripts/install_harnesshub_skill.py`
