---
name: research-harness
description: Use for post-MVP hypothesis-driven work in OpenPrecedent. Provides a lightweight workflow for framing research issues, experiments, evidence, and success or failure interpretation without leaving the existing issue-task-PR process.
---

# Research Harness

Use this skill when the task is primarily about product learning rather than core-loop plumbing.

Typical triggers:

- retrieval quality evaluation
- runtime impact validation
- extraction quality analysis
- experiment design
- evidence capture for post-MVP product hypotheses

Do not use this skill for straightforward implementation-only tasks unless the user explicitly wants a hypothesis-driven framing.

## Goal

Keep research work structured enough that later sessions can answer:

- what hypothesis was being tested
- how it was tested
- what artifact should count as evidence
- how success, failure, or ambiguity should be interpreted

The skill should strengthen the existing issue-task-PR workflow rather than creating a parallel planning system.

Parent framework: #100

## Workflow

1. Anchor the work in the current research phase.
   - Treat GitHub issue `#100` as the long-lived umbrella for post-MVP research evolution.
   - Use a child issue for the concrete question under test.

2. Create or update the local task twin as `task_type: research`.
   - Reuse `.codex/skills/ccpm-codex/` for issue/task/PR mechanics.
   - Prefer one issue per hypothesis, not one issue per broad theme.

3. Initialize issue-scoped state if the work will span multiple sessions.
   - Run:
   - `python3 -m openprecedent.codex_pm issue-state-init <task-path>`

4. Copy the research experiment template into the issue state or the task notes.
   - Use `templates/research-experiment-template.md` for the main structure.
   - Use `templates/research-issue-template.md` when drafting a new issue body.
   - Use `templates/research-result-template.md` when recording outcomes.

5. Make the hypothesis explicit before implementation.
   - State one research question.
   - State one method.
   - State the expected artifact.
   - State how success, failure, and ambiguity will be interpreted.

6. Prefer narrow evidence-producing work over broad speculative refactors.
   - Good outputs:
   - validation docs
   - fixture or eval additions
   - quality reports
   - observability improvements
   - narrow policy or algorithm changes justified by evidence

7. Close only the concrete child issue.
   - Do not close umbrella issue `#100`.
   - Keep parent framing in docs and issue links, not in PR closing clauses.

## Recommended Structure

For a research issue, aim to fill these fields:

- hypothesis
- method
- expected artifact
- success signal
- failure signal
- ambiguity signal

For a research result, always record:

- what was run
- what was observed
- what changed in confidence
- what follow-up issue, if any, should come next

## Read Next

- `templates/research-experiment-template.md`
- `templates/research-issue-template.md`
- `templates/research-result-template.md`
- [`docs/product/mvp-status.md`](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-status.md)
- [`docs/engineering/harness-capability-analysis.md`](/workspace/02-projects/incubation/openprecedent/docs/engineering/harness-capability-analysis.md)
