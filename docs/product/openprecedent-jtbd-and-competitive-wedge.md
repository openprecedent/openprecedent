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

## Why Existing Infrastructure Is Not Enough

OpenPrecedent should not be justified by claiming that existing systems record nothing.
They do record many adjacent things, but they usually do not preserve reusable judgment structure in the right place or form.

Existing infrastructure tends to record one of the following:

- code, configuration, pull requests, and issues that show what changed
- documents and meeting notes that show what was discussed
- tracing, logs, and observability data that show what executed
- wikis, knowledge bases, or CRM systems that show what was explicitly stored

The gap is that OpenPrecedent is trying to preserve a different unit:

- why the default path stopped being valid in this situation
- which constraints made the team or agent choose a different path
- which rejected options still matter for future judgment

That unit is hard for existing infrastructure to preserve because it is usually:

- spread across multiple surfaces
- only partially visible in final artifacts
- too situational to justify a full formal document
- most legible at decision time rather than afterward

So the problem is not absence of storage.
The problem is absence of a durable, reusable decision unit.

## Why This Is Not Just A Manual Recording System

A manual decision-entry system is an obvious alternative, but it usually breaks down in practice.

The core failure modes are:

- the extra workflow cost appears exactly when teams are busy, under pressure, or handling exceptions
- people rarely know in the moment which temporary-looking choice will become historically important later
- manually written summaries drift away from the actual execution path, evidence, and decision timing

Manual systems can still be useful as a supplement.
They are much weaker as the primary capture mechanism for high-value exception decisions.

OpenPrecedent matters when decision capture is tied closely enough to real execution that later users and agents can recover not just a polished summary, but the surrounding constraints and why they mattered.

## Why Agent-Era Capture Must Sit On The Execution Path

The strongest reason OpenPrecedent becomes more necessary in the agent era is that decision-making moves from a relatively low-frequency organizational activity into a high-frequency execution activity.

Compared with mostly human-driven work, agent-assisted work changes several fundamentals:

- decision density increases sharply during one task
- many decisions are now co-produced through human-agent interaction rather than only through human-human discussion
- some intermediate decisions are made by the agent during task execution without direct human review at each step
- default-path behavior becomes more dangerous because agents naturally gravitate toward generic and mainstream solutions
- execution speed rises, so human recall becomes harder to insert at the right moment
- captured precedent can now be consumed directly by later execution rather than only by later readers

This creates a qualitative shift.
In a mostly human era, many decisions could remain in the heads of a few experts because later humans could often reconstruct or ask around before acting.
In an agent era, the number and speed of decisions make that human-only recovery loop increasingly fragile and expensive.

That is why execution-path capture matters.
The point is not just to preserve history for later explanation.
The point is to make prior judgment available to the next comparable decision while execution is still happening.

## Decision Precedents Are Not Truth

One critical risk is to confuse recorded decisions with timeless correct answers.
That would make the system actively dangerous.

A precedent may be:

- wrong even at the time it was made
- only valid under narrow local constraints
- later invalidated by product, customer, architecture, or organizational change

So OpenPrecedent should not treat precedent as policy or ground truth.
It should treat precedent as contextualized historical judgment.

The key analytical point is that these three failure modes are different:

- a wrong decision means the original judgment itself was bad
- a locally valid decision means the judgment was acceptable only under narrow constraints
- a later-invalid decision means the judgment may have been good once but has aged out

Those differences matter because they create different risks for future agents:

- wrong precedents can amplify historical mistakes
- locally valid precedents can be over-generalized into places where they do not belong
- expired precedents can anchor future work on assumptions that no longer hold

So the danger is not just "bad data."
The deeper danger is misplaced authority.
If a system presents precedent as if it carries timeless normative force, future agents may stop asking whether the surrounding constraints still match.

The practical implication is that future agents should inherit more than the decision content itself.
They should also inherit:

- the constraints under which the decision was made
- the alternatives that were considered or rejected
- the evidence that was available at the time
- the outcome or later evaluation when that is known
- any indication that the decision was temporary, exceptional, or later superseded

The product is most useful when it helps future execution ask "is this prior judgment still relevant here?" rather than silently assuming "do this because it happened before."

This also implies a boundary for the product:

- OpenPrecedent should surface candidate precedent, not silently enforce historical imitation
- retrieval quality depends on matching constraints and applicability, not only semantic similarity of topic or wording
- the system becomes stronger when it can preserve later correction, supersession, or invalidation rather than only the original choice

## Early Rollout Requires Hybrid Capture

Another practical limit is that many important decisions still happen outside agent visibility.
They may appear in:

- meetings
- email
- Slack or other chat systems
- ad hoc spoken discussion

So an early OpenPrecedent deployment should not assume full automatic capture.
That assumption would be false in most real organizations.

The more realistic early model is hybrid capture:

- automatic or near-automatic capture from agent-visible execution paths
- structured capture of human-agent interaction
- low-friction human supplementation for off-path decisions that agents could not observe directly

This means the early goal is not omniscience.
The early goal is to capture the highest-value, hardest-to-reconstruct decisions with enough context that later agents and operators can reuse them.

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

For the first phase, the strongest priority is narrower still:

OpenPrecedent should first capture exception-driven decisions under real constraints, especially the places where a default or mainstream path would normally have been chosen but had to be changed because of customer requirements, historical baggage, defect-repair trade-offs, time-cut release pressure, undocumented architecture details, or temporary recovery needs.

That makes these decisions stronger initial precedent candidates than generic architecture discussion or broad strategy commentary, because they are both harder to reconstruct later and more likely to mislead later agents into confident but wrong default choices.

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
