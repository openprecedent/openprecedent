# HarnessHub Real-Project Observation Log

Use this file during issue `#131` to record concrete observations while HarnessHub development runs in a parallel Codex session. Earlier entries refer to the project's ClawPack phase when that was still the active product name.

## Active Validation Task

Add manifest-level harness metadata so a `.clawpack` package describes a reusable agent runtime environment rather than only a file bundle.

## What To Watch

- whether lineage changes the wording or scope of the task
- whether lineage changes schema shape or naming decisions
- whether lineage helps reject over-broad abstraction
- whether harness transfer improves session continuity
- whether the HarnessHub product framing becomes clearer through implementation

## Observation Entries

### Entry Template

- Timestamp:
- HarnessHub task step:
- Query reason:
- Brief summary returned:
- Decision affected:
- Observed effect:
- Confidence change:

### Entries

- Timestamp: 2026-03-11T15:27:14Z to 2026-03-11T15:27:39Z
- HarnessHub task step: initial planning and first write-scope commitment for manifest-level harness metadata during the ClawPack phase
- Query reason: `initial_planning`, then `before_file_write`
- Brief summary returned: the active task was framed narrowly as adding harness-level manifest metadata so a `.clawpack` package describes a reusable agent runtime environment rather than only bundled files; the planned implementation stayed limited to existing schema, export/import flow, verify checks, and tests
- Decision affected: the implementation was explicitly constrained to a minimal `manifest.harness` shape instead of broad runtime abstraction
- Observed effect: the resulting worktree changed only the expected files: `src/core/types.ts`, `src/core/packer.ts`, `src/core/verifier.ts`, and `test/e2e.test.ts`; the diff shows a concrete `harness` manifest object, derived component metadata, verifier coverage, and regression tests for both new and legacy manifests
- Confidence change: positive initial support for the hypothesis that runtime lineage can help preserve scope discipline and convert product framing into a narrow implementation plan in a different repository

- Timestamp: 2026-03-11T23:57:22+08:00 to 2026-03-12T00:23:23+08:00
- HarnessHub task step: manifest-level harness metadata implementation completed, committed, and regression-tested during the ClawPack phase
- Query reason: the earlier `initial_planning` and `before_file_write` decisions remained the operative guidance for the completed implementation round
- Brief summary returned: no matched precedent case was surfaced, but the recorded plan kept the work issue-scoped and explicitly rejected generic platform abstraction
- Decision affected: the project shipped a concrete manifest schema change rather than drifting into broader harness-platform design work
- Observed effect: branch `codex/manifest-harness-metadata` now contains commit `b43b505` (`feat: add harness metadata to manifest`); the commit adds `Manifest.harness`, derived harness component extraction, verifier coverage for `manifest_harness`, and one additional end-to-end test path for legacy-manifest warning behavior; `npm test` passed with `22` tests and the worktree was clean afterward
- Confidence change: stronger support that OpenPrecedent can help carry a precise product framing into a finished, tested feature increment in HarnessHub's earlier ClawPack phase, though the result still does not demonstrate precedent-hit quality because `matched_case_ids` remained empty during this round

- Timestamp: 2026-03-12T00:30+08:00
- HarnessHub task step: new Codex session restart and early-session planning check
- Query reason: `initial_planning` on session restart, focused first on preserving shared runtime continuity and then on re-analyzing the project roadmap against implemented modules and tests
- Brief summary returned: the new session continued to use the shared `OPENPRECEDENT_HOME` and explicitly treated lineage or local state updates as required for cross-session researchability; no matched precedent case was surfaced
- Decision affected: the session restarted in a controlled way instead of immediately changing code, preserving research continuity and re-establishing project understanding before the next implementation step
- Observed effect: new runtime invocations were recorded, but no new code diff or commit appeared yet; the repository remained at commit `b43b505` with a clean worktree
- Confidence change: moderate additional support that OpenPrecedent is already useful as cross-session process instrumentation and scope control, even before stronger precedent-hit evidence appears in later development rounds

- Timestamp: 2026-03-11T16:49:25Z to 2026-03-12T00:24:43Z
- HarnessHub task step: harness transfer moved from exploratory analysis into issue-scoped execution, including bootstrap, failure recovery, decomposition into follow-up issues, and rebased continuation on issue `#6`
- Query reason: repeated `before_file_write` and one `after_failure` query across harness bootstrap, GitHub issue/PR alignment, guardrail hardening, issue decomposition, and rebase/conflict resolution work
- Brief summary returned: the session repeatedly framed work as narrow harness increments rather than broad platform redesign, used issue/task/state metadata as the execution backbone, and explicitly recorded one failure-recovery loop when preflight tests inherited an outer recursion-guard environment variable
- Decision affected: the work evolved from a single feature experiment into a real transfer of OpenPrecedent harness practice, including local PM workflow, preflight/hook guardrails, CLI validation, issue-scoped branches, and merge-following rebase behavior
- Observed effect: the project progressed through issue-scoped branches and merged PRs (`issue-3`, `issue-5`, `issue-7` visible in history) and is currently on branch `issue-6-expand-cli-integration-validation`; the latest visible commit is merge commit `c1b671d`; `npm test` passed with `38` tests across `6` test files, including CLI integration, smoke, preflight, pre-push, e2e, and codex-pm coverage
- Confidence change: strong support that OpenPrecedent is already effective as a transferable harness methodology and research instrumentation layer in HarnessHub's earlier ClawPack phase; precedent-hit quality is still unproven, but cross-session continuity, scope discipline, and failure-recovery observability are now demonstrated on a more realistic development loop

- Timestamp: 2026-03-12T11:35+08:00
- HarnessHub task step: repository renamed and repositioned as `HarnessHub`, with active format-layer migration work on issue `#19`
- Query reason: none newly recorded after the last visible invocation at `2026-03-12T00:24:43Z`; the new session left code and test evidence but no fresh runtime decision-lineage invocation
- Brief summary returned: not applicable for this round because no new lineage brief was captured in the shared runtime log
- Decision affected: the product direction has clearly advanced from an OpenClaw-first packaging CLI toward a harness image standard, but the migration currently breaks multiple engineering surfaces at once
- Observed effect: the active repository path changed to `/workspace/02-projects/active/HarnessHub`; current branch is `issue-19-format-layer-migration`; docs, package metadata, CLI copy, and architecture files now use the `HarnessHub` name, while tests and scripts still contain many hard-coded `clawpack` paths and assumptions; `npm test` now fails in CLI smoke, preflight, pre-push hook, and CLI integration coverage
- Confidence change: positive support that the product has moved into a more ambitious and more revealing validation stage, but negative evidence that research observability dropped at the same time because the renamed repository no longer appears to trigger the old ClawPack-specific OpenPrecedent skill path automatically

- Timestamp: 2026-03-12T11:36+08:00
- HarnessHub task step: root-cause analysis for the missing lineage records after the HarnessHub rename
- Query reason: repository-local inspection of the installed validation skill and reference files
- Brief summary returned: the hidden skill still identifies itself as `openprecedent-clawpack-validation`, says to use it only inside `/workspace/02-projects/active/clawpack`, and its reference file still describes the experiment strictly as ClawPack validation
- Decision affected: after the repository rename, a new session can plausibly continue engineering work without ever matching the old skill trigger or path assumptions, which would explain why no new invocation was written even though the shared runtime remained available
- Observed effect: the hidden skill exists under `.codex/skills/openprecedent-clawpack-validation/`, but both the skill body and reference file are stale with respect to the new `HarnessHub` path and name; this likely severed the automatic prompt-to-lineage path while leaving the rest of the development harness intact
- Confidence change: strong support for a concrete harness gap diagnosis: the lineage workflow did not disappear because OpenPrecedent failed technically, but because the trigger surface was not updated after the repository rename

- Timestamp: 2026-03-12T03:44:51Z
- HarnessHub task step: repair the hidden OpenPrecedent validation skill after the repository rename so lineage invocations resume under the HarnessHub name
- Query reason: `initial_planning`
- Brief summary returned: the active task was framed narrowly as repairing the local validation trigger surface after the rename, not as changing product behavior or making OpenPrecedent a visible HarnessHub dependency
- Decision affected: the hidden validation skill was renamed and repointed from the old ClawPack path and name to a HarnessHub-specific local skill while preserving the same shared runtime and narrow invocation policy
- Observed effect: a new invocation `rtinv_b171a0586155` was written to the shared runtime at `2026-03-12T03:44:51Z`; the hidden skill now lives under `.codex/skills/openprecedent-harnesshub-validation/` inside the external repository, restoring research observability after the rename with only minor wording residue left in the skill text
- Confidence change: strong support that OpenPrecedent's research continuity depends on maintaining the local trigger surface across product renames, and that a small harness repair can restore observability without reintroducing OpenPrecedent as a visible product dependency

- Timestamp: 2026-03-12T07:02:46Z to 2026-03-12T07:11:42Z
- HarnessHub task step: issue-scoped contract hardening across template-versus-instance packaging, structural-versus-runtime-ready verification, and manifest-level rebinding or placement rules
- Query reason: one `initial_planning` query followed by three `before_file_write` queries for issues `#47`, `#45`, and `#46`
- Brief summary returned: the session framed the next round as three explicit contract questions, then narrowed each write step to one concrete schema or behavior change: enforce pack-type component policy in export and verify, split runtime readiness from structural validity without breaking the existing `valid` field, and promote placement or rebinding rules into explicit manifest contracts consumed by import, export, and verify
- Decision affected: HarnessHub continued evolving as an explicit image-contract product rather than drifting into ad hoc runtime heuristics; each issue was reduced to a narrow contract change with a matching implementation surface
- Observed effect: the shared runtime now contains invocations `rtinv_12f435402f51`, `rtinv_bc9b3cf24533`, `rtinv_037dd2b021cf`, and `rtinv_d8b68eab3ba3`; the external repository advanced cleanly to commits `67ba42e` (`Define explicit pack type contract (#48)`), `024d9e8` (`Separate structural and runtime-ready verification (#49)`), and `c1e85b1` (`Codify rebinding and placement contract (#50)`), with no remaining worktree diff at observation time
- Confidence change: stronger support that OpenPrecedent is now participating in real HarnessHub design convergence at the issue level, not only in session continuity; precedent-hit quality is still unproven because `matched_case_ids` remained empty, but the lineage-to-commit chain is now materially clearer than in earlier rounds

- Timestamp: 2026-03-12T07:35:16Z to 2026-03-12T07:51:11Z
- HarnessHub task step: next-wave issue decomposition and implementation across export policy, readiness classes, formal image specification, and OpenClaw regression baseline hardening
- Query reason: one `initial_planning` query followed by four `before_file_write` queries for issues `#51`, `#53`, `#52`, and `#54`
- Brief summary returned: the session first grouped the next wave into four explicit follow-up concerns, then narrowed each write step to a single concrete change: add an explicit export override policy for risky template downgrades, refine verification into explicit readiness classes, publish a formal MVP Harness image specification tied to implemented semantics, and turn the OpenClaw e2e validation record into a stable regression baseline
- Decision affected: the product continued moving from implicit CLI behavior toward an explicit harness-image contract with user-facing policy, layered verification semantics, durable documentation, and artifact-backed regression evidence
- Observed effect: the shared runtime now includes invocations `rtinv_613cd988a449`, `rtinv_6fa386aae969`, `rtinv_f5c75b28e325`, `rtinv_aa30e2043a6b`, and `rtinv_b4fe9a40885d`; the external repository is clean on `main-codex-sync` and has already merged the corresponding work as commits `8441399` (`Define export policy overrides and warnings`), `ae90c76` (`Add explicit verification readiness classes`), `7cbc154` (`Publish MVP harness image specification`), and `4484474` (`Add OpenClaw baseline regression assertions`)
- Confidence change: stronger support that OpenPrecedent is helping sustain issue-scoped architectural convergence across multiple successive HarnessHub waves, not just isolated fixes; matched precedent reuse is still not evidenced because `matched_case_ids` remained empty, but the runtime lineage log now consistently mirrors merged issue-level design decisions

- Timestamp: 2026-03-12T08:03+08:00
- HarnessHub task step: systematic diagnosis of why `matched_case_ids` remains empty across repeated HarnessHub runtime invocations
- Query reason: research inspection of the shared runtime database, runtime workflow scripts, and decision-lineage retrieval implementation
- Brief summary returned: the primary bottleneck is not merely low sample count; the shared runtime database currently contains zero searchable runtime history (`cases=0`, `decisions=0`, `events=0`), while the active Codex runtime workflow explicitly records invocation logs but does not automatically ingest external-project Codex history into searchable cases and decisions
- Decision affected: current HarnessHub runtime use can function as observation instrumentation and session discipline, but it cannot yet produce precedent matches unless searchable prior cases are seeded or imported into the shared runtime database
- Observed effect: `matched_case_ids` stays empty because `build_decision_lineage_brief()` only ranks over `self.store.list_cases()` with extracted decisions, and the current shared runtime store has no cases at all; even after that is fixed, the present matcher is still a lexical overlap scorer over `task_summary/current_plan/candidate_action/known_files` versus extracted case and decision keywords, so semantically related but differently worded HarnessHub cases would remain easy to miss
- Confidence change: strong support for a more specific diagnosis than “sample size may be low”: the present limitation is a pipeline gap first, retrieval quality gap second, and raw sample volume only third
