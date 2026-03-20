# OpenPrecedent MVP Status Note

## Status

As of `2026-03-10`, OpenPrecedent `0.1.0` MVP release is complete.

The core loop is no longer just specified in design docs. It is implemented and validated in the repository's local OpenClaw-first runtime path.

## Current Phase

OpenPrecedent is now in a post-MVP research validation phase.

At this stage, the repository should be read as a local-first validation platform for the product's core hypotheses around:

- decision-lineage usefulness
- precedent reuse in real agent workflows
- retrieval and extraction quality on growing real history
- downstream task impact when lineage is actually surfaced at runtime

This is no longer primarily a core-loop plumbing effort.
The current platform role is to make those hypotheses fast to test against a real OpenClaw-first environment without reopening MVP foundation work each time.

For the current release-facing scope and positioning baseline, see:

- [MVP release scope](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-scope.md)
- [MVP release closeout](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-closeout.md)

As of `2026-03-11`, the next planned research runtime after OpenClaw is Codex.
That work is intentionally scoped as a research-only second runtime rather than a generalized multi-runtime abstraction effort.

## Research Governance

The long-lived umbrella for this phase is GitHub issue `#100`, `Define the post-MVP research evolution framework for OpenPrecedent`.

That issue should remain open as the parent framing artifact for later hypothesis-driven child issues.
Repository docs should point to it, but should not duplicate the full research program each time.

For repository-local execution of those child issues, use the project skill:

- [.codex/skills/research-harness/SKILL.md](/workspace/02-projects/incubation/openprecedent/.codex/skills/research-harness/SKILL.md)

## Completed Core Loop

The shipped MVP now covers:

1. capture a case
2. store the ordered event timeline
3. extract decision records
4. replay and explain decisions
5. retrieve similar precedent

In practical repository terms, that means:

- local SQLite-backed case, event, decision, and artifact persistence
- CLI flows for ingestion, replay, extraction, and precedent retrieval
- OpenClaw session import and silent local collection
- fixture-based and real-session evaluation flows
- real local runtime validation for decision-lineage retrieval through the OpenClaw path

## What Counts As Done

The MVP should now be considered engineering-complete because:

- the end-to-end loop works on real local runtime history, not only synthetic fixtures
- the repository has a standard E2E validation path and merge validation guidance
- OpenClaw-facing runtime lineage retrieval has a stable shared persistence path and a documented trigger policy
- no current repository doc needs to treat the core loop as still blocked on foundational implementation work

## What Is Not Done

Completion of the MVP core loop does not mean the product is finished.

The next stage is post-MVP validation and quality work, including:

- measuring whether lineage retrieval improves downstream task behavior
- expanding real-history evaluation coverage
- improving decision extraction quality where real history shows repeated gaps
- improving precedent ranking quality as the corpus grows

These are product-effectiveness and research-quality questions, not missing core-loop plumbing.

## Reference Docs

- [MVP release scope](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-scope.md)
- [MVP release closeout](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-closeout.md)
- [MVP roadmap](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-roadmap.md)
- [MVP PRD](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-prd.md)
- [MVP architecture](/workspace/02-projects/incubation/openprecedent/docs/architecture/mvp-design.md)
- [Codex runtime research boundary](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-boundary.md)
- [OpenClaw full user journey validation](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-full-user-journey-validation.md)
- [OpenClaw real runtime decision-lineage validation](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-real-runtime-decision-lineage-validation.md)
- [Merge validation guidance](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/merge-validation.md)
