# HarnessHub Second-Phase Observation Log

Use this file during issue `#220` to record post-cutover HarnessHub observations after the second-phase reliability plan from issue `#217` was defined.

The goal is not to reopen the first-phase study from issue `#131`.
The goal is to classify later rounds as positive, negative, or ambiguous evidence for post-Rust-CLI invocation reliability and retrieval usefulness.

## Observation Entries

### Entry Template

- Timestamp:
- HarnessHub issue:
- Development step:
- Query reasons observed:
- Runtime evidence:
- Interpretation:
- Reliability effect:

## Entries

- Timestamp: 2026-03-19 to 2026-03-20, observed from merged issues `#106`, `#107`, `#105`, `#109`, and `#108`
- HarnessHub issue: `#106` Define the harness definition file model and add harness init; `#107` Make parent image references operational for local `v0.2.0` definitions; `#105` Add harness compose for one local parent-plus-child materialization path; `#109` Make export and verify lineage-aware for composed `v0.2.0` images; `#108` Refactor builder and materialization boundaries for definition-driven `v0.2.0` flows
- Development step: complete the first implementation-heavy `v0.2.0` wave through merged PRs `#113`, `#114`, `#115`, `#116`, and `#117`, covering definition modeling, parent references, compose flows, lineage-aware export/verify behavior, and builder/materialization refactoring
- Query reasons observed: `initial_planning` and `before_file_write` on `#106`, `#107`, `#105`, and `#109`; `initial_planning` on `#108`
- Runtime evidence: `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` contains new HarnessHub records at `2026-03-19T03:21:05Z`, `2026-03-19T03:23:04Z`, `2026-03-19T03:36:32Z`, `2026-03-19T03:38:34Z`, `2026-03-19T03:47:58Z`, `2026-03-20T02:12:58Z`, `2026-03-20T02:24:19Z`, `2026-03-20T02:25:49Z`, and `2026-03-20T02:35:26Z`; all of those records return non-empty `matched_case_ids` grounded in prior governance, architecture, guardrail, validation, and image-model precedent, and they cover the core implementation wave that the earlier `#220` open questions explicitly called out as still missing
- Interpretation: this is the decisive positive evidence that the second-phase study needed; the current local private-entry setup is not only surviving release, governance, and PRD work, but is also being exercised across a real implementation sequence with repeated planning and write-time invocation on core `v0.2.0` feature work
- Reliability effect: satisfies the remaining closure criterion for `#220`'s main research question; the study can now close with a defensible claim that the current local activation mechanism supports repeated, useful lineage invocation across multiple task classes, while still leaving narrower causal-isolation questions as follow-up work rather than blockers to closeout

- Timestamp: 2026-03-19, observed from merged issues `#110` and `#104`
- HarnessHub issue: `#110` Document branching and release-line governance for stable versions; `#104` Draft the `v0.2.0` PRD for define-and-local-compose scope
- Development step: complete one governance-documentation task through merged PR `#111`, then complete one product-direction PRD task through merged PR `#112` as the repository shifts from release closeout work into `0.2.0` planning
- Query reasons observed: `initial_planning` and `before_file_write` on `#110`; `initial_planning` on `#104`
- Runtime evidence: `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` contains new HarnessHub records at `2026-03-19T02:00:56.592334351Z`, `2026-03-19T02:01:10.700022450Z`, and `2026-03-19T02:21:25.736428233Z`; the `#110` records show both planning and write-time invocation with non-empty `matched_case_ids` grounded in prior governance, architecture, and release-checklist cases, while the `#104` record shows planning-stage invocation with non-empty `matched_case_ids` during the first `v0.2.0` PRD-definition step
- Interpretation: this is the first positive evidence in the second-phase study that clearly extends beyond the tightly coupled RC-to-GA release sequence; the current local private-entry setup is now leaving useful lineage traces on governance and product-direction work, not just release execution
- Reliability effect: materially increases confidence that the current mechanism generalizes beyond release tasks, but it is still early for `v0.2.0` work because the current evidence only covers one documentation task end-to-end and one PRD task at planning time; implementation-heavy `0.2.0` issues still need to show the same behavior before the study should be closed

- Timestamp: 2026-03-18, observed from merged issues `#98`, `#99`, and `#102`
- HarnessHub issue: `#98` Validate published `0.1.0-rc.1` from a fresh external-user install path; `#99` Define the `0.1.0` GA go/no-go gate after `0.1.0-rc.1`; `#102` Prepare the final HarnessHub `0.1.0` GA release
- Development step: complete a contiguous post-RC release sequence that validated the published RC, wrote the GA go/no-go gate, decided to proceed, and then closed the final GA publication flow through merged PRs `#100`, `#101`, and `#103`
- Query reasons observed: repeated `initial_planning`, repeated `before_file_write`, and `after_failure` on both `#98` and `#102`
- Runtime evidence: `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` contains a dense series of new `2026-03-18` HarnessHub records at `06:25:39Z`, `06:26:56Z`, `06:32:43Z`, `06:33:45Z`, `06:34:39Z`, `08:51:10Z`, `08:52:22Z`, `09:04:51Z`, `09:13:22Z`, `09:15:29Z`, `09:18:26Z`, `09:20:16Z`, `09:21:01Z`, and `09:28:09Z`; these cover release follow-up planning waves, issue `#98` external-user validation, issue `#99` gate definition, issue `#97` release-decision planning, and issue `#102` final GA execution; the records repeatedly return non-empty `matched_case_ids` grounded in prior release-checklist, release-candidate, CLI-validation, repository-governance, validation-baseline, and documentation-alignment cases
- Interpretation: this is the strongest positive evidence in the second-phase study so far because the current local private-entry setup did not just restore isolated invocation on one issue; it remained active across a whole release sequence with multiple planning waves, multiple write-time narrowing steps, and repeated `after_failure` recovery lookups on real operator-facing release work
- Reliability effect: materially upgrades the current reliability assessment from "recovered but still fragile" to "showing sustained positive signals under the present local activation mechanism"; the study should still avoid claiming that the repository-side skill text alone is sufficient, but it can now say that the combined local setup is repeatedly supporting real HarnessHub work rather than producing one-off success

- Timestamp: 2026-03-18, observed from merged issue `#95`
- HarnessHub issue: `#95` Run release gate and publish HarnessHub `v0.1.0-rc.1`
- Development step: complete the release-candidate closeout round through merged PR `#96`, including release-gate execution, a fresh-operator validation pass, a release runbook, and release-note finalization
- Query reasons observed: `initial_planning`, `before_file_write`, and `after_failure`
- Runtime evidence: `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` now contains new HarnessHub records at `2026-03-18T02:00:35.337593875Z`, `2026-03-18T02:03:00.729168447Z`, and `2026-03-18T02:06:55.611987971Z`; those records cover release planning, write-time narrowing for the `#95` implementation surface, and an `after_failure` recovery step for a broken fresh-operator validation path; all three records return non-empty `matched_case_ids` grounded in prior HarnessHub release-checklist, release-candidate, CLI-validation, guardrail, and documentation-alignment cases
- Interpretation: this is stronger positive evidence than the `#89/#93` round because the current local activation path did not only restore `initial_planning` and `before_file_write`; it also produced an `after_failure` invocation during a real release-execution problem, showing that the current local hidden-entry mechanism plus the Rust-CLI-based private skill can support planning, implementation narrowing, and recovery guidance within one end-to-end round
- Reliability effect: materially strengthens the second-phase reliability picture by showing a full three-stage trigger pattern on a consequential release round; however, the evidence should still be interpreted as validating the current local private-entry setup rather than proving that the repository-side skill text alone is sufficient for stable loading

- Timestamp: 2026-03-17, observed from issue `#89` and follow-up issue `#93`
- HarnessHub issue: `#89` Unify repository versioning on `0.1.0-rc.1`; `#93` Tighten unreleased RC wording after issue `#89` without changing repository version strings
- Development step: complete issue `#89` through merged PR `#92`, then open and merge follow-up PR `#94` for issue `#93`
- Query reasons observed: `initial_planning` and `before_file_write`
- Runtime evidence: `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` now contains new HarnessHub records at `2026-03-17T16:37:55.201561721Z`, `2026-03-17T16:38:46.481830732Z`, `2026-03-17T16:39:26.421751074Z`, `2026-03-17T16:46:55.619085166Z`, and `2026-03-17T16:47:38.263035756Z`; those records cover issue `#89` and follow-up issue `#93`, include both `initial_planning` and `before_file_write`, and return non-empty `matched_case_ids` grounded in prior HarnessHub release-candidate, versioning, and repository-evolution cases
- Interpretation: this is strong new positive evidence that post-cutover HarnessHub rounds can again invoke lineage at the intended stages and retrieve semantically relevant precedent; however, the positive result cannot be attributed solely to the `#233` single-skill refinement because the user reports that the session also relied on an additional locally maintained hidden file referenced from HarnessHub's `AGENTS.md` to force that private skill into the session
- Reliability effect: materially improves the second-phase reliability picture relative to the `#79`, `#81`, `#83`, and `#85` misses, but the result should currently be interpreted as evidence that a stronger local private-entry mechanism works rather than as proof that the repository-level `#233` skill text alone is sufficient for stable loading

- Timestamp: 2026-03-17, observed from merged issues `#81`, `#83`, and `#85`
- HarnessHub issue: `#81` Document how to interpret harness CLI artifact outputs; `#83` Raise coverage on CLI entrypoints and command/output surfaces; `#85` Raise overall branch coverage to 80 percent
- Development step: complete three consecutive issue rounds through PRs `#82`, `#84`, and `#86`, with a fourth follow-up issue `#87` already opened afterward
- Query reasons observed: none on `2026-03-17`; the shared runtime still contains no records newer than the `2026-03-14` issue `#77` round
- Runtime evidence: HarnessHub completed issue `#81` at `2026-03-17T11:50:04Z`, issue `#83` at `2026-03-17T12:21:40Z`, and issue `#85` at `2026-03-17T12:48:06Z`, with matching merged PRs `#82`, `#84`, and `#86`; a new issue `#87` was opened at `2026-03-17T12:54:54Z`; however, `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` still ends its HarnessHub evidence at `2026-03-14T16:58:22.426163810Z`
- Interpretation: this is stronger negative evidence than the single `#79` miss because it shows multiple later HarnessHub rounds and a new follow-up planning wave all proceeded without entering the lineage path at all; the current post-cutover weakness is still best classified as invocation-adherence or workflow-composition failure, not retrieval degradation
- Reliability effect: materially weakens the current reliability claim for stage-based invocation after the Rust CLI cutover; the evidence now suggests that later HarnessHub work can continue successfully across multiple rounds without triggering the private OpenPrecedent skill

- Timestamp: 2026-03-15, observed from merged issue `#79`
- HarnessHub issue: `#79` Stabilize coverage workflow dependency installation
- Development step: complete issue execution through PR `#80` merge without any newly recorded OpenPrecedent invocation during the same day
- Query reasons observed: none on `2026-03-15`; the shared runtime contains no new `initial_planning`, `before_file_write`, or `after_failure` records for this round
- Runtime evidence: HarnessHub development clearly occurred on `2026-03-15` with commits `19c5c10`, `fb37b74`, `1af6de1`, `bc0190d`, `2205916`, and `086d7c9`, and PR `#80` merged at `2026-03-15T05:45:39Z`; however, `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` contains no `2026-03-15` records even though the Rust-CLI-based private skill had already been installed into HarnessHub on `2026-03-14`
- Interpretation: this round is best classified as an invocation-adherence miss rather than a retrieval-quality regression or a Rust CLI execution failure; the development loop ran and closed successfully, but it did not enter the lineage path at all
- Reliability effect: negative evidence for reliable stage-triggered invocation after the Rust CLI cutover; it suggests the current main HarnessHub workflow still does not consistently compose or execute the private OpenPrecedent skill during every issue round

## Cross-Round Synthesis

### Worked Example: HarnessHub Issue `#106`

This example shows how OpenPrecedent's recorded lineage context influenced a later implementation task instead of merely logging that a query happened.

#### Planning-stage input and retrieval

Original runtime record:
- `query_reason: "initial_planning"`
- `task_summary: "HarnessHub issue #106: define harness definition file model and add harness init command"`
- `matched_case_ids:`
  - `case_harnesshub_issue_13_define-clawpack-product-foundation-and-architect`
  - `case_harnesshub_issue_52_publish-a-formal-mvp-harness-image-specification`
  - `case_harnesshub_issue_53_refine-verification-into-explicit-readiness-clas`

中文解释：
- 这一步记录的原始输入是“为 `v0.2.0` 引入 definition file 模型，并新增 `harness init` 命令”。
- 返回的历史案例不是随机命中，而是分别落在：
  - 产品基础定义
  - 形式化 image/spec 契约
  - verify / readiness 语义收敛
- 这意味着系统给当前任务施加的历史约束是：
  - 新 definition file 不能脱离已有产品基础定义
  - 不能发明一套与既有 image contract 断裂的新模型
  - 不能绕开现有 verify / readiness 语义

#### Write-stage input and retrieval

Original runtime record:
- `query_reason: "before_file_write"`
- `task_summary: "HarnessHub issue #106: define harness definition file model and add harness init"`
- `matched_case_ids:`
  - `case_harnesshub_issue_3_bootstrap-local-ccpm-codex-and-harness-guardrail`
  - `case_harnesshub_issue_6_expand-cli-integration-validation-for-the-pack-l`
  - `case_harnesshub_issue_13_define-clawpack-product-foundation-and-architect`

中文解释：
- 到真正写文件前，返回的 precedent 从“产品定义”进一步收窄到了“实现路径”。
- 这轮命中的重点已经变成：
  - 本地 harness / guardrail
  - CLI integration validation
  - 产品基础定义
- 它对实现的隐含影响是：
  - 这不是一个只改内部数据结构的任务
  - `harness init` 应按 CLI-first 的方式实现和验证
  - 新模型仍要服从既有产品基础定义，而不是另起炉灶

#### Decision influence

Recorded facts:
- issue `#106` 在 `initial_planning` 与 `before_file_write` 两个阶段都触发了 lineage
- 两次 retrieval 都返回了非空 precedent
- 对应 PR `#113` 已 merged

中文解释：
- 当前系统已经不只是“记录发生了查询”，而是已经能在两个关键节点提供有约束力的历史上下文：
  - planning 阶段帮助任务定类
  - write 阶段帮助实现面收窄
- 在 `#106` 这个例子里，OpenPrecedent 的作用不是替开发者发明答案，而是把这轮工作持续拉回到：
  - 既有产品定义
  - 既有 image/spec 语义
  - 既有 CLI validation 路径
- 这就构成了一个完整的“记录输入 -> 提取 precedent -> 影响后续决策”的链条

### Current Assessment of the Three Trigger Stages

#### `initial_planning`

Assessment:
- clearly effective
- consistently useful for task framing and precedent-based boundary setting

中文解释：
- 这个阶段已经证明有效。
- 它最稳定的价值是帮助当前任务回到已有历史语境里，避免一开始就偏离到无 precedent 支持的新方向。

#### `before_file_write`

Assessment:
- currently the strongest stage
- repeatedly useful for narrowing implementation shape, likely files, and validation surface

中文解释：
- 这是当前最强的一环。
- 它不仅说明“该做什么”，还更具体地约束“该怎么做、该验证什么、该沿哪条既有实现路径收敛”。

#### `after_failure`

Assessment:
- less frequent than the first two stages
- already validated in real recovery loops such as `#95`, `#98`, and `#102`

中文解释：
- 这一步样本相对少，但已经证明有价值。
- 它的意义不在于高频，而在于开发偏航时，系统能够提供恢复方向，而不只是事后回放。

### What Is Proven and What Still Remains Open

Proven now:
- the current local hidden-entry setup plus the private skill and Rust CLI can repeatedly produce useful lineage invocation across release, governance, PRD, and implementation work
- the three-stage model is already useful enough to support real work rather than merely logging experiments

中文解释：
- `#220` 的主问题现在已经回答清楚：这套机制已经不是偶发成功，而是可重复支持真实开发。
- 这一点已经足以支撑 `#220` 收口。

Still open:
- the study does not isolate which factor is individually necessary or sufficient
- the system still records retrieved context more clearly than adopted context
- contamination and retrieval hygiene remain valid next-step research topics

中文解释：
- 还没解决的问题不是“它能不能工作”，而是：
  - 到底哪个因子最关键
  - 哪些 retrieval 真正被采纳
  - 如何进一步减少污染和噪音
- 这些都更适合变成后续研究 issue，而不是继续阻塞 `#220`
