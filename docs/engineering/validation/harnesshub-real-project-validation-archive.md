# HarnessHub Real-Project Validation Archive

## Purpose

This document archives issue `#131` as the first completed external-project validation study for OpenPrecedent.

It is not the original experiment plan and it is not the raw observation log.
Its job is to explain, in one place, what the study was trying to prove, what went wrong in the early rounds, how those failures were diagnosed, which follow-up changes closed the gap, and why the issue can now be closed as validated first-phase research.

## Question Under Test

Could OpenPrecedent do more than replay or explain prior work inside its own repository?

The specific research question for `#131` was whether OpenPrecedent lineage and harness practice could materially improve real Codex development in a different repository, using HarnessHub as the first target.

## Initial Study Shape

The study began during HarnessHub's earlier ClawPack phase.
At that point the target repository was small enough to iterate quickly, close enough to the agent-runtime domain to make lineage relevant, and different enough from OpenPrecedent to make cross-project reuse a meaningful test.

The intended proof chain was:

1. run real HarnessHub development under OpenPrecedent-backed lineage retrieval
2. record whether lineage affected scope, constraints, or design choices
3. determine whether any imported prior HarnessHub history could later be matched back into new live work

## What Worked Early

Even before precedent hits were working, the study produced useful positive evidence:

- session restarts could recover active research context
- lineage helped keep implementation scope narrow
- issue-scoped execution and harness transfer improved continuity across rounds
- OpenPrecedent functioned as a research instrumentation layer and decision externalization layer in a real external project

That early evidence mattered, but it did not yet prove the full hypothesis.
The missing proof was precedent reuse during a later live HarnessHub round.

## Early Problems

### 1. Empty `matched_case_ids`

The main visible failure during the early live rounds was simple:

- runtime invocations existed
- lineage briefs could still frame tasks
- but `matched_case_ids` remained empty

That meant the system was helping with continuity and discipline, but it had not yet demonstrated that prior external-project history could be retrieved back into later real work.

### 2. Rename-trigger gap

During the target repository's rename from ClawPack to HarnessHub, the hidden validation skill and its reference files still pointed at the old repository path and name.

The effect was subtle but important:

- real engineering work continued
- the shared runtime still existed
- but the old trigger surface no longer matched the renamed repository
- so research observability temporarily dropped

This was not a failure of the precedent engine itself.
It was a harness continuity failure caused by stale trigger assumptions.

### 3. Searchable-history gap

The more important technical diagnosis came from inspecting the shared runtime database and retrieval flow.
The study found that the system was not merely suffering from weak match quality.
The shared runtime actually had no searchable imported HarnessHub history.

That meant the live runtime loop was missing the first prerequisite for precedent hits:

- prior HarnessHub rounds had to become stored cases, events, and decisions before later sessions could retrieve them

### 4. Retrieval-quality gap

Even after solving the missing-history pipeline, the study identified a second limitation:

- the matching approach still depended too much on lexical overlap
- semantically related but differently worded HarnessHub rounds would remain easy to miss

### 5. Sample-volume gap

The study also found a third-order limitation:

- more imported HarnessHub rounds would improve confidence and robustness
- but low sample volume was not the primary reason live matching initially failed

The gaps were therefore ordered like this:

1. pipeline gap
2. retrieval-quality gap
3. sample-volume gap

That diagnosis was one of the most important outputs of `#131`.

## How The Problems Were Solved

The first-phase study closed the missing chain through a concrete follow-up issue sequence.

### `#152`

Export completed HarnessHub Codex rounds as importable searchable-history artifacts.

This solved the first half of the pipeline problem by turning completed external-project rounds into durable inputs for the shared runtime.

### `#153`

Import exported HarnessHub rounds into the shared runtime and extract decisions.

This turned the exported history into actual searchable runtime state.

### `#154`

Validate non-empty `matched_case_ids` for a later HarnessHub runtime query.

This was the key checkpoint that proved the pipeline was no longer empty in principle.

### `#155`

Improve HarnessHub decision-lineage matching beyond lexical overlap.

This addressed the second gap by improving the matcher so it could survive more wording drift across related issues.

### `#161`

Auto-seed shared runtime from completed HarnessHub rounds.

This closed the operational loop by reducing the risk that live sessions would once again query an empty or stale shared runtime.

## What Refactoring Happened Around The Study

Issue `#131` did not live in isolation.
Several kinds of surrounding refactor work affected the study and clarified its meaning.

### Harness transfer refactor

HarnessHub gradually adopted issue-scoped OpenPrecedent-style execution patterns:

- issue/task/state discipline
- local guardrails
- explicit startup context
- validation-driven workflow structure

This made it possible to evaluate not only precedent retrieval, but also whether harness practice itself transferred across repositories.

### Rename repair refactor

The ClawPack-to-HarnessHub rename forced a repair of the hidden validation skill.
That work restored the private trigger path without making OpenPrecedent a visible dependency in the target product.

This solved an observability and workflow-composition problem, not a retrieval algorithm problem.

### Rust CLI and skill refactor

Later in the repository history, OpenPrecedent replaced the public Python CLI with the Rust CLI and reworked several skill and workflow surfaces around that interface.

That refactor is important context, but it happened after the first-phase result recorded here.
It does not invalidate the evidence archived by `#131`.
It does mean that any future reliability check after the Rust CLI cutover should be tracked as a new study rather than folded back into this issue.

## Final Positive Result

The first-phase study crossed its key threshold during later live HarnessHub work, especially around issue `#67`.

At that point:

- the shared runtime contained imported HarnessHub history
- live runtime invocations returned non-empty `matched_case_ids`
- the retrieved prior cases grounded a later product-positioning decision
- the current session did not have to reframe the problem from scratch

This was the first strong proof that OpenPrecedent was doing more than session discipline or post-hoc explanation.
It was reusing imported prior external-project history strongly enough to shape a later live development decision.

## What `#131` Proved

Issue `#131` now supports these conclusions:

- OpenPrecedent can help real development in an external repository, not only in OpenPrecedent itself
- harness practice and decision-lineage retrieval can both transfer across repositories
- empty-match failures can be turned into useful product diagnosis instead of being treated as generic failure
- the external-project precedent loop is viable once capture, import, extract, seed, and retrieval are all closed

## What `#131` Did Not Prove

This study did not prove:

- that retrieval quality is already stable under long-term real-project use
- that contamination risk is solved
- that the post-Rust-CLI interface still produces the same reliability profile without additional study

Those are follow-up questions, not reasons to keep `#131` open.

## Why The Issue Can Close

`#131` should close because its first-phase research question has been answered:

- early failures were explained
- the missing retrieval chain was closed
- later live external-project reuse was observed
- the remaining concerns are follow-up quality questions, not unresolved first-phase proof questions

In other words, the study moved from:

- "can this work at all in a real external project?"

to:

- "how do we improve retrieval hygiene and reliability now that it does work?"

That is the correct boundary for closing this issue and archiving it.

## Reading Order

For future sessions, use this order:

1. [HarnessHub Real-Project Validation Plan](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/harnesshub-real-project-validation-plan.md)
2. [HarnessHub Real-Project Observation Log](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/harnesshub-real-project-observation-log.md)
3. [HarnessHub Real-Project Validation Report](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/harnesshub-real-project-validation-report.md)
4. this archive document
5. [Research Archive Workflow](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/research-archive-workflow.md)
