---
type: issue_state
issue: 131
task: .codex/pm/tasks/codex-runtime-research/validate-codex-real-project-decision-lineage-reuse.md
title: Validate Codex real-project decision-lineage reuse across HarnessHub development
status: done
---

## Summary

Archive the first-phase HarnessHub real-project validation as completed research evidence showing that OpenPrecedent's external-project precedent loop became usable in live development after the searchable-history chain was closed.

## Validated Facts

- OpenPrecedent MVP v1 was complete before this study closed and the repository had already moved into post-MVP research validation.
- HarnessHub became the first real external Codex project used to test whether OpenPrecedent lineage and harness practice transfer across repositories during live development.
- Early HarnessHub rounds demonstrated useful session continuity and scope discipline, but `matched_case_ids` remained empty.
- The empty-match result was diagnosed as a concrete chain of gaps rather than a generic product failure:
  - the shared runtime held no searchable imported HarnessHub history
  - retrieval quality still relied too heavily on lexical overlap
  - sample volume was still too small for robust matching
- That chain was closed through issue `#152`, `#153`, `#154`, `#155`, and `#161`.
- Later live HarnessHub invocations returned non-empty `matched_case_ids` from imported prior HarnessHub history.
- The strongest positive reuse evidence came during HarnessHub issue `#67`, where matched prior cases influenced a later product-positioning decision in live work.
- The historical ClawPack-to-HarnessHub rename temporarily broke the hidden validation skill trigger surface; repairing that private skill restored research observability without making OpenPrecedent a visible HarnessHub product dependency.
- Later Rust CLI and skill refactors changed the public interface and harness shape after this study, but they do not invalidate the first-phase conclusion recorded here; any post-cutover reliability study should be tracked separately.

## Open Questions

- How should OpenPrecedent reduce contamination from only partly related precedent now that live matching works?
- How many more real HarnessHub rounds are needed before retrieval quality claims move from “validated usable loop” to “stable operating expectation”?

## Next Steps

- Close issue `#131` as archived first-phase validation evidence rather than leave it open as an active implementation thread.
- Keep contamination control and further retrieval-quality work under `#163` and later follow-up studies instead of reopening this issue.
- Treat any post-Rust-CLI reliability check as a new research issue rather than additional scope on `#131`.

## Artifacts

- `docs/engineering/validation/harnesshub-real-project-validation-plan.md`
- `docs/engineering/validation/harnesshub-real-project-observation-log.md`
- `docs/engineering/validation/harnesshub-real-project-validation-report.md`
- `docs/engineering/validation/harnesshub-real-project-validation-archive.md`
- `docs/engineering/validation/research-archive-workflow.md`
- `/workspace/02-projects/active/HarnessHub/AGENTS.md`
- `/workspace/02-projects/active/HarnessHub/.codex/skills/openprecedent-harnesshub-validation/`
- `research-artifacts/harnesshub/`
