# AgentHarnessKit External Validation Observation Log

Date: 2026-03-20

Use this file during issue `#261` to record OpenPrecedent observations from AgentHarnessKit development as a distinct external-project validation track.

The goal is not to reopen the completed HarnessHub studies.
The goal is to understand how precedent retrieval behaves when the external target is a harness scaffold repository rather than a product repository.

## Observation Entries

### Entry Template

- Timestamp:
- AgentHarnessKit issue:
- Development step:
- Query reasons observed:
- Runtime evidence:
- Interpretation:
- Research effect:

## Entries

- Timestamp: 2026-03-20, observed from merged issues `#4`, `#5`, `#6`, `#7`, `#8`, and `#15`
- AgentHarnessKit issue: `#4` Migrate reusable PM and issue-state core into AgentHarnessKit; `#5` Harden review checkpoints and pre-push guardrails; `#6` Introduce a unified local preflight entrypoint; `#7` Define OpenSpec as the planning source of truth; `#8` Define Superpowers integration boundaries for AgentHarnessKit; `#15` Clarify agent-driven workflow entrypoint in AGENTS.md
- Development step: complete the first substantive migration wave in AgentHarnessKit through merged PRs `#10`, `#11`, `#12`, `#13`, `#14`, and `#16`, covering PM migration, local guardrails, preflight, planning-source rules, integration boundaries, and workflow-entry guidance
- Query reasons observed: `initial_planning` on the first private-overlay issue, the reusable PM migration wave, and the later completeness/entrypoint audit; `after_failure` on the branch-rebuild and sequential-delivery recovery step; no `before_file_write` evidence yet
- Runtime evidence: `~/.openprecedent/runtime/openprecedent-runtime-invocations.jsonl` currently contains four AgentHarnessKit-tagged records at `2026-03-20T13:37:24Z`, `2026-03-20T13:48:32Z`, `2026-03-20T14:33:48Z`, and `2026-03-20T14:43:57Z`; all four return non-empty `matched_case_ids`, grounded mainly in HarnessHub guardrail, governance, validation-baseline, and integration-boundary cases
- Interpretation: this is a clear positive start for `#261`; OpenPrecedent is not silent in AgentHarnessKit, and the retrieved precedent remains semantically plausible for a harness-scaffold repository. The strongest recurring signal is not product delivery precedent but repository-harness precedent: guardrails, review sequencing, workflow governance, and local validation boundaries. The current data also show a real `after_failure` recovery use, which matters because this repository is likely to spend more time on workflow corrections than product-style feature branching.
- Research effect: positive evidence that OpenPrecedent can transfer into a second external repository category beyond HarnessHub; not yet enough evidence to claim stable reliability for AgentHarnessKit because the sample is still small and currently lacks `before_file_write` coverage
