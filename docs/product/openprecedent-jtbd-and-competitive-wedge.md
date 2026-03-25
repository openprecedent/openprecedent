# OpenPrecedent JTBD And Competitive Wedge

Date: 2026-03-25
Status: draft living note
Chinese companion: [docs/zh/product/openprecedent-jtbd-and-competitive-wedge.md](/root/.config/superpowers/worktrees/openprecedent/codex-jtbd-product-wedge/docs/zh/product/openprecedent-jtbd-and-competitive-wedge.md)

## Why This Note Exists

This note captures an ongoing product discussion about what job OpenPrecedent should truly serve for users.

The central concern is not whether agents can produce logs, traces, or retrieved memories.
The central concern is that important decision context is often lost during project evolution and agent-assisted delivery.

That missing context may live in:

- meeting notes
- Slack or other IM threads
- repository discussion outside the final code change
- customer-specific exceptions
- expert recall that is never written down cleanly

When those decision signals disappear, later work can drift toward generic but wrong solutions, repeat already rejected directions, or miss repository-specific and customer-specific exceptions.

OpenPrecedent should be evaluated against that problem rather than against a generic "agent observability" category.

## Problem Framing

Users do not want a decision database for its own sake.
They want a reliable way to recover and reuse the judgment structure behind earlier work.

In practical terms, the risk is not only that an agent forgets facts.
The deeper risk is that an agent or later human operator forgets:

- why a direction was chosen
- what constraints mattered at the time
- which options were considered and rejected
- which approvals or authority boundaries mattered
- where a customer or project required a non-standard exception

If those signals are absent, later iterations may still look competent while moving in the wrong direction.

## Which Decisions Matter Most

The highest-value precedents are usually not standard choices that are already well reflected in code, docs, or common best practice.
The highest-value precedents are the decisions that drift away from the default path and become hard to reconstruct later.

Current working hypothesis:

- deviations from the original design direction
- trade-offs made during defect repair
- customer-specific exceptions or requirements
- version-specific scope cuts made under time pressure
- architecture-selection details that never fully made it into docs or code
- temporary solution choices made during incident response or bug fixing

These are especially valuable because they tend to be:

- expensive to rediscover
- weakly represented in code or final documentation
- highly consequential for later maintenance
- easy to lose when people change roles or leave

The broader pattern is portable beyond development work.
The same logic likely applies to:

- product planning decisions that changed roadmap or scope direction
- sales or customer-delivery decisions that shaped what could or could not be promised

So the generalized rule is:

OpenPrecedent should prioritize the decisions that are least recoverable from the final artifact but most important for later judgment.

## Candidate Jobs-To-Be-Done

### Candidate Primary Job: Decision-time judgment inheritance

When a user or agent needs to make a meaningful new decision in a real project, they need a compact view of what prior similar situations already taught them about the right framing, constraints, trade-offs, authority boundaries, and success criteria.

JTBD form:

When I need to make a new project decision with real trade-offs such as solution choice, cost, speed, maintenance burden, approval cost, or customer-specific exceptions, I want a compact brief of the judgment structure from similar prior cases, so I can move forward with less guesswork, less rework, and less risk of repeating a previously rejected path.

Planning, writing, recovery, and approval-boundary moments are important trigger points for this job, but they are not the whole job.
The deeper job is to support new decisions under real project trade-offs, not only to guard execution steps.

This is the strongest current candidate for the product wedge because it targets the moment when users are most willing to pay attention, change behavior, and consult prior judgment before creating new downstream cost.

### Secondary Job: Post-hoc decision explanation

When an agent run looks questionable, a user needs to reconstruct why a decision happened and where the reasoning went wrong.

This is valuable, but it is probably not the best wedge by itself because many observability tools already partially serve adjacent post-hoc review needs.

### Longer-Horizon Job: Durable precedent accumulation

Over time, a team may want project-specific and customer-specific decision patterns to become reusable precedent rather than scattered tribal memory.
The important point is that this does not require instant replacement of expert judgment.
The product can begin by supporting professionals during real work, then gradually accumulate the decision precedents that later reduce dependence on fragile human recall.

This matters, but it is more of a long-term compounding benefit than the narrowest initial wedge.

## What The User Is Really Hiring

OpenPrecedent should not think of itself as selling replay, storage, or retrieval in isolation.

The user is hiring it to:

- reduce decision risk before the next meaningful action
- avoid repeating already rejected reasoning
- surface repository-specific and customer-specific exceptions
- shorten the path from "we solved something like this before" to "here is the part that still matters now"

The product becomes more valuable when it behaves like a judgment inheritance layer, not just a history viewer.

## Substitute Solutions

Users already have many ways to solve parts of this job.
Those substitutes are the real competition.

### 1. Non-consumption

The user does nothing special.
They let the agent continue and rely on intuition, luck, or later review.

This is often the default competitor because it has zero workflow cost.

### 2. Human recall and expert consultation

The user asks the maintainer, the product owner, the customer-facing operator, or the expert who remembers why something was decided.

This is often the strongest substitute because humans can reconstruct intent and exceptions better than current tools.
It is also the substitute OpenPrecedent most needs to displace over time.

The reason is structural, not tactical:

- important decision context often survives only in expert memory
- expert recall is expensive and slow to access
- staff turnover and organizational change make this memory base fragile
- the longer a project runs, the harder it becomes to keep this human-only dependency maintainable

OpenPrecedent should not assume it can replace expert judgment in one step.
It should instead turn repeated expert-agent interaction into explicit precedent over time, so dependence on expert recall decreases as the corpus matures.

### 3. Code search and repository history

The user searches code, PRs, issues, commits, comments, and docs to infer what happened before.

This works reasonably well for explicit written decisions, but it is weak for tacit reasoning and off-transcript context.

### 4. Observability and tracing tools

These tools are good at showing what the agent did.
They are less naturally aligned with the narrower question of which judgment structure should be reused in the current situation.

### 5. Memory, RAG, and note retrieval systems

These systems can surface related facts, snippets, and documents.
They are useful substitutes, especially when the missing signal lives in Slack, notes, or customer documents.

Their weakness is that they often return content rather than a distilled decision lineage.

### 6. Process templates, policy docs, and checklists

Some teams encode past learning into playbooks or review checklists.

This can handle stable and repeatable constraints well, but it usually loses the situational nuance that made an exception valid in a particular customer or repository context.

## Why A User Would Choose OpenPrecedent

A user is more likely to hire OpenPrecedent when it does all of the following better than the substitute set:

- returns the relevant judgment faster than searching PRs, notes, and chat threads
- expresses the result as decision structure, not just related text
- appears at the moment of planning, writing, or recovery rather than only after the fact
- preserves repository-specific and customer-specific exceptions instead of flattening everything into generic best practice
- explains why a prior case is relevant so the result is auditable and trustworthy

If OpenPrecedent cannot beat the combined workflow of search plus human recall, it will not become a durable habit.
The more important long-term bar is whether it can progressively absorb enough reusable expert judgment that the organization becomes less dependent on remembering the right person to ask.

## Why A User Might Not Choose OpenPrecedent

Users may choose substitutes instead when:

- the task is too small or low-risk to justify another step
- there is little or no prior history worth consulting
- the product returns too much raw history and not enough distilled guidance
- the best decision context still lives outside the captured corpus
- the user trusts a human expert more than the retrieved precedent
- the tool feels like another observability dashboard rather than an action-time aid

This means that "better replay" alone is unlikely to be enough.

## Current Product Versus Future Target

## Current validated value

The current OpenPrecedent MVP is strongest at:

- capturing local case history
- extracting decision records
- replaying and explaining a case
- retrieving semantically related precedent from prior history

That is an important base, but it is still best understood as infrastructure that proves the loop is viable.

## Future target value

The stronger future product target is narrower and more opinionated:

- surface decision lineage before the next critical action
- integrate decision-relevant signals from more than the raw runtime transcript
- preserve customer-specific and repository-specific exceptions as first-class precedent
- help agents inherit proven judgment structure instead of only retrieving adjacent text or operational similarity
- accumulate reusable precedent from expert-agent interaction so organizations get compounding returns instead of resetting to tribal memory each time people change

The future product should not become a generic graph, generic memory platform, or generic trace viewer.
Its distinctive value is decision inheritance under real project constraints.
It should also not claim immediate replacement of professional judgment.
The stronger claim is gradual externalization of reusable expert decisions into a durable precedent layer.

## Working Product Thesis

OpenPrecedent should aim to become the layer that helps agents and operators make better new decisions by inheriting the right prior judgment, especially when the most important context is fragmented across runtime history, human discussion, and project-specific exceptions.

Its strategic path is not instant expert replacement.
Its strategic path is to capture precedent during real expert-agent work, so the system compounds reusable decision history and reduces long-term dependence on fragile human recall.

## Open Questions

- How much off-transcript context should OpenPrecedent ingest directly versus reference indirectly?
- What is the smallest high-frequency trigger moment where decision-time lineage is clearly worth the workflow cost?
- How should the product distinguish stable precedent from one-off local exceptions?
- How should customer-specific exceptions be modeled without collapsing into a generic CRM or knowledge base product?
- What evidence would prove that decision-time lineage changes downstream decisions rather than merely explaining them better afterward?
- Which parts of expert judgment can realistically be externalized into precedent first, and which parts will remain expert-only for longer?
