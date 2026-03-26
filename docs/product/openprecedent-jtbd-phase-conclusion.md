# OpenPrecedent JTBD Phase Conclusion

Date: 2026-03-26
Status: phase conclusion
Chinese companion: [docs/zh/product/openprecedent-jtbd-phase-conclusion.md](/root/.config/superpowers/worktrees/openprecedent/codex-jtbd-product-wedge/docs/zh/product/openprecedent-jtbd-phase-conclusion.md)

## Why This Conclusion Exists

This note closes the current JTBD discussion round for OpenPrecedent.
The earlier working note explored the problem space broadly and iteratively.
This document consolidates the conclusions that now appear directionally stable enough to guide later product work.

The reference frame comes from *Competing Against Luck*.
The important question is not simply who the user is.
The more important questions are:

- in what situation the user hires the product
- what progress the user is actually trying to make
- what substitute solutions the user already uses instead

Using that frame, this conclusion captures what now appears answered, what remains unresolved, and how the current MVP aligns or diverges.

## Core Conclusion

OpenPrecedent should not be understood primarily as a decision archive, an agent trace viewer, or a generalized memory store.
The strongest current conclusion is that users hire OpenPrecedent to recover historically relevant judgment before a new meaningful decision is made.

The product is most valuable when it helps an operator or agent retrieve the constraints, exceptions, rejected paths, and prior trade-offs that still matter now.
The immediate value is not "more history."
The immediate value is reducing wrong default decisions.

In short:

OpenPrecedent should become a decision-precedent layer that helps later execution inherit prior judgment under real constraints.

## What This Discussion Has Now Answered

### What the user is really "buying"

Users are not buying a decision-recording system for its own sake.
They are not buying an agent log viewer for its own sake either.

They are hiring OpenPrecedent when a new consequential decision is about to happen and they do not want to rediscover the same judgment from scratch.
What they want back is not raw history, but the parts of prior history that still matter now:

- which constraints were decisive
- which exceptions overrode the default path
- which options were considered and rejected
- which boundaries or approvals mattered
- which judgment should still influence the current decision

That is the most important conclusion from this round.

### Who the real competitors are

The competitive set is not limited to observability tools, tracing products, or memory systems.
The real substitute set is a combined workflow that already helps users complete parts of the same job:

- non-consumption, where the user simply lets the agent continue and relies on intuition or later review
- human recall and expert consultation
- code search and repository history
- documents, meeting notes, Slack threads, chat systems, and email
- observability and tracing tools
- memory, RAG, and note-retrieval systems
- templates, policy documents, and checklists

The strongest substitute is usually not another software product.
It is human recall and expert consultation.

That matters because it clarifies the actual bar for adoption.
If OpenPrecedent cannot outperform the practical combination of search plus expert reconstruction, it will not become a durable habit.

### Why existing approaches are insufficient

The problem is not that current systems record nothing.
The problem is that they usually fail to preserve and reuse the judgment structure future decisions actually need.

Existing approaches often retain adjacent information, but not the most reusable semantic unit.
What tends to be lost includes:

- why the default path stopped being valid
- which constraints mattered enough to force a deviation
- which options were seriously rejected and why
- which exceptions were only locally valid
- which decisions later expired, were replaced, or should no longer be trusted

So the gap is not "missing records" in a generic sense.
The gap is the absence of reusable, context-bound judgment at the moment a new decision must be made.

### Why the agent era intensifies the problem

This discussion also clarified that the agent era does not create decisions from nothing.
It changes their density, visibility, and downstream consequences.

The agent era raises the stakes because:

- decision density is higher inside a single unit of work
- many decisions are now co-produced through human-agent interaction
- some intermediate decisions are made by agents without direct human review of every step
- agents are more likely to drift toward mainstream or default solutions
- future execution is increasingly performed by agents rather than by humans who can reconstruct context ad hoc

This changes the role of precedent.
Precedent is no longer only for post-hoc explanation.
It becomes something that should be consumed directly by later execution.

### What should be captured first

This round also converged on a narrower answer about what kinds of decisions matter most.

OpenPrecedent should not start by capturing all "important decisions."
It should prioritize exception-shaped decisions that are hard to reconstruct from final artifacts but highly consequential for later maintenance and future judgment.

The highest-value examples identified so far are:

- customer-specific exceptions
- historical compatibility constraints
- defect-repair trade-offs
- temporary or transitional fixes
- version cuts made under time pressure
- architecture details that never fully made it into code or documentation

The common pattern is more important than the examples themselves:

The best initial precedents are decisions where a default path would normally have been taken, but a real constraint forced a different path.

### What the product really is

One major correction from this round is that OpenPrecedent should not be framed as a developer-only project precedent tool.

Its long-term product category is broader:

OpenPrecedent should be treated as a general decision-precedent infrastructure for agent-assisted execution.

That general category can apply across:

- coding and software delivery agents
- sales agents
- operations and organizational workflow agents
- personal assistant agents
- industrial or operational agents

At the same time, the current high-signal validation environment remains narrow:

- the current wedge is coding-agent and software-delivery work

So the correct framing is not "developer tool" versus "universal platform" as a binary.
The correct framing is:

- general product category
- narrow initial wedge

## Direct Answers To The Core Questions

### Who is the customer

The customer should not be reduced to the generic label "developer."
The more accurate customer model has three layers.

Direct users are people who work with agents frequently and need to make decisions under project-specific constraints.
This includes engineers, tech leads, delivery leads, and other operators in agent-assisted workflows.

Organizational customers are teams or product groups whose systems evolve over time while accumulating exceptions, legacy baggage, and hidden judgment that is hard to preserve.

Economic buyers are the people accountable for downstream cost.
They are usually leaders who own some combination of maintenance burden, rework, delivery risk, or organizational dependence on expert memory.

### What they hire OpenPrecedent to do

They are not hiring it to own an archive.
They are hiring it so that when a new meaningful decision has to be made, they do not need to guess why a similar situation was judged a certain way before.

That can be stated as:

When a new consequential decision is needed under real trade-offs, I want a compact recovery of the historically relevant judgment from similar prior cases, so I can move forward with less guesswork and less risk of repeating a wrong or already rejected default path.

### What outcome they expect

The expected outcome is not "more knowledge" in the abstract.
The expected outcome is operational:

- fewer wrong default paths
- less rework
- less dependence on finding the right expert at the right time
- less loss of exception-specific judgment as teams change
- more agent behavior that feels like inherited experience rather than generic averaging

### What the product's value is

The shortest defensible value statement from this round is:

OpenPrecedent reduces wrong default decisions.

That is intentionally simpler than the product internals.
It captures the external value without collapsing into implementation detail.

### Why not rely on manual logging

High-value decisions often happen under pressure, in exceptions, or in moments that look temporary at the time.
That is exactly when manual entry is least reliable as the primary capture mechanism.

Manual recording can still help as a supplement.
It is a weak default for the main capture path because the most important decisions are often the least likely to be deliberately documented in a structured way while they are happening.

### Whether precedent can become dangerous

Yes.
This discussion now clearly treats precedent as a potentially dangerous object if it is mistaken for timeless truth.

Precedent may be:

- wrong when first recorded
- only valid in a narrow local context
- later invalidated by product, customer, architectural, organizational, or policy change

So precedent must be treated as a contextual historical judgment sample.
That is why the current thesis now emphasizes:

- applicability
- invalidation and supersession
- candidate precedent rather than silent enforcement

### Why the product must be both general and specific

The current conclusion is:

- the ambition must be general
- the validation path must be specific

So OpenPrecedent should be described as general agent precedent infrastructure, while the current wedge remains coding-agent and software-delivery validation.

That split is necessary.
Without the general layer, the product collapses into a narrow vertical tool.
Without the specific wedge, the product becomes too abstract to validate.

## What Is Not Fully Resolved Yet

The discussion can now be considered converged enough for this phase, but some questions remain open at the product-design level.

### Minimum target customer remains incomplete

The analysis no longer treats "developers" as the final answer, but it still has not fully locked the narrowest initial buying team.
The next round will still need to define which exact first team profile should feel the pain most urgently and adopt first.

### Core fields versus enrichment fields remain incomplete

The note now records a much clearer candidate semantic core for cases, decisions, precedents, applicability, and related fields.
However, it still does not fully separate:

- the fields required for the MVP semantic core
- the fields that can remain optional or be added as later enrichment

### Runtime use remains incomplete

The analysis is now clear that precedent should not be obeyed blindly.
But the exact runtime behavior is still unresolved.
For example, the product has not fully specified when the system should:

- suggest a precedent
- require clarification
- block a default action
- escalate to a human
- only annotate a decision after the fact

### Commercial packaging remains incomplete

The open-source foundation versus enterprise private-cloud direction is clearer now.
But the actual packaging is not complete yet.
The discussion has clarified the boundary, but not yet translated it into a final product packaging model.

These are no longer "directional confusion" questions.
They are later product-definition questions.

## Alignment With The Current MVP

The current MVP and this phase conclusion are directionally aligned in several important ways.

### Where the MVP already matches

The MVP already shares the core structural logic of this conclusion.
It is aligned in the following ways:

- it already works through the chain of case, event, decision, and precedent
- it does not define itself as a generic graph, generic memory platform, or generic trace viewer
- it already treats replay, explanation, and precedent retrieval as core capabilities
- it is already validating the idea that precedent can be retrieved from prior history
- it already emphasizes local-first, single-agent, and concrete validation over abstract platform claims
- it already follows the right order of proof: validate one concrete loop before expanding

For that reason, the MVP should not be judged as directionally wrong.
It already contains the skeleton of the broader product thesis.

### Where the MVP still differs

The main difference is not that the MVP chose the wrong direction.
The main difference is that the current conclusion operates at a higher level of product definition than the current implementation.

The current MVP still behaves more like:

- a foundation for capture, replay, extraction, and retrieval over existing history

The stronger target described in this phase conclusion is:

- decision-time judgment inheritance before the next meaningful action

The main differences are:

- the MVP is still more focused on explaining past runs, while the conclusion emphasizes helping the next decision before it happens
- the MVP is mostly validating a local single-agent coding environment, while the conclusion defines a broader product category for agent-assisted execution in many domains
- the MVP is still weak on off-path human context such as meetings, chat systems, email, and explicit expert supplementation
- the MVP does not yet center applicability, invalidation, supersession, and temporality strongly enough, even though the current conclusion treats them as crucial for preventing precedent misuse
- the MVP is still more oriented toward semantic retrieval plus replay, while the stronger product thesis requires constraint-matching, exception-awareness, and historical validity checks
- the MVP does not yet explicitly present the architecture as a core precedent layer, a domain adaptation layer, and a runtime usage layer

So the most accurate summary is:

The MVP has already shown that a precedent loop can run.
It has not yet fully become the general decision-precedent infrastructure described by this phase conclusion.

## Phase Summary

Using the language of *Competing Against Luck*, the discussion is now much clearer than it was at the start.
OpenPrecedent is no longer being treated as a feature-rich but loosely defined system.
The analysis now gives coherent answers to these questions:

- what job the user is hiring it to do
- what substitute set it must beat
- why the job becomes more important in the agent era
- which kinds of decisions matter most
- what the product's long-term category is
- what its first validation wedge is

The current MVP and this conclusion therefore stand in a complementary relationship:

- the MVP proves the loop may be viable
- this conclusion defines what the loop should ultimately become

## Relation To The Earlier Note

The earlier note [openprecedent-jtbd-and-competitive-wedge.md](/root/.config/superpowers/worktrees/openprecedent/codex-jtbd-product-wedge/docs/product/openprecedent-jtbd-and-competitive-wedge.md) should now be treated as the completed working note for this discussion round.
It remains useful as the detailed exploration record.
This phase-conclusion document is the shorter normative reference for what the discussion has converged on.
