---
type: issue_state
issue: 265
task: .codex/pm/tasks/real-history-quality/establish-repository-wide-doc-chronology-and-entrypoints.md
title: Establish repository-wide documentation chronology and canonical entrypoint conventions
status: in_progress
---

## Summary

Define a lightweight repository-wide convention for documentation chronology and canonical entrypoints, then demonstrate it with minimal `README` and governance updates across the current `docs/` tree.

## Validated Facts

- `docs/README.md` already worked as the top-level English entrypoint, but `docs/product/` and `docs/architecture/` had no local directory index.
- `docs/research/README.md` and `docs/zh/research/README.md` already used dated directory indexes, so the repository already had one strong chronology pattern worth generalizing.
- `docs/zh/README.md` described the top-level Chinese tree, but `docs/zh/product/` and `docs/zh/architecture/` had no local entrypoint or explicit canonical-versus-historical guidance.
- Date and status metadata already existed in parts of the tree, but not yet as a documented repository-wide convention.

## Open Questions

- Whether `docs/engineering/` also needs a dedicated chronology rule beyond the existing concern-based split.
- Whether more legacy documents should be explicitly reclassified as historical drafts in follow-up issues instead of this minimal entrypoint pass.

## Next Steps

- Verify the new governance doc and directory indexes are sufficient as a first repository-wide convention.
- Stage the new task twin, issue-state, governance doc, and directory `README` files together in one docs-only commit.
- Run lightweight validation (`git diff --check` and direct README review) before commit.

## Artifacts

- `docs/README.md`
- `docs/engineering/governance/documentation-governance.md`
- `docs/product/README.md`
- `docs/architecture/README.md`
- `docs/zh/README.md`
- `docs/zh/product/README.md`
- `docs/zh/architecture/README.md`
