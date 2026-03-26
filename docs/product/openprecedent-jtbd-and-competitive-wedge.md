# OpenPrecedent JTBD And Competitive Wedge

Date: 2026-03-25
Status: phase conclusion for the current JTBD round
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

## Current Product Thesis

OpenPrecedent should become a judgment-inheritance layer for agents and operators.
Its job is not to store more history for its own sake.
Its job is to preserve and retrieve the prior judgment that still matters when a new decision has to be made under real project constraints.

That matters most when critical context is fragmented across runtime history, human discussion, customer-specific exceptions, and expert memory.
The strategic path is not instant expert replacement.
The strategic path is to capture precedent during real expert-agent work, so reusable judgment compounds over time and dependence on fragile human recall gradually decreases.

## General Infrastructure Versus Initial Wedge

One recurring source of confusion is to collapse OpenPrecedent's long-term product category into its first validation environment.
That would be too narrow.

OpenPrecedent should not be understood as infrastructure only for software teams or only for developer project precedent management.
The broader product thesis is a general precedent layer for agents.
Wherever an agent participates in execution, there is usually some form of decision path, judgment loss, and later need for decision reuse.

That broader thesis plausibly applies across many domains, including:

- software delivery and coding agents
- sales and customer-facing agents
- operations and organizational workflow agents
- personal assistant agents
- industrial or operational control agents

The cross-domain commonality is not the surface workflow.
The commonality is the underlying job:

- an agent or human-agent pair makes decisions under local constraints
- some of the important judgment is temporary, fragmented, or weakly represented in final artifacts
- later execution benefits if that prior judgment can be retrieved as precedent rather than rediscovered from scratch

At the same time, the first wedge should still be much narrower than the eventual product category.
Different domains have very different decision taxonomies, capture surfaces, evidence models, risk profiles, and usefulness metrics.
So the product should not pretend that a single initial workflow proves all domains equally well.

The right framing is therefore layered:

- the product category is a general decision-precedent infrastructure for agents
- the current validation wedge is software delivery and coding-agent work because that is where the team can most concretely observe decision paths, capture artifacts, and downstream effects
- future expansion can target other agent-heavy domains once the core precedent model and retrieval logic are proven in one high-signal environment

This distinction matters strategically.
If OpenPrecedent is framed only as a developer tool, the ambition becomes artificially small.
If it is framed only as a universal agent platform without a narrow wedge, the validation path becomes vague and the product thesis becomes hard to test.
The product needs both: a general infrastructure ambition and a concrete first environment.

## What Must Stay General Versus Domain-Specific

If OpenPrecedent is meant to become infrastructure for many agent domains, the hardest design question is not whether many domains exist.
The harder question is which parts of the system should remain stable across domains and which parts must remain adaptable.

The wrong abstraction would be to generalize surface workflows.
Software delivery, sales, operations, personal assistance, and industrial control do not share one workflow.
What they can share is a common decision-precedent core.

### Cross-domain stable object model

The most plausible cross-domain stable objects are:

- `case`
  A bounded unit of work or situation where action is being taken.
  Examples vary by domain, but the role is stable: this is the container for one meaningful piece of work.

- `event`
  A timestamped unit of runtime or interaction history.
  Events are the raw material layer rather than the judgment layer.

- `decision`
  A derived record that captures where one path was chosen over another under real constraints.
  This is the core unit that distinguishes OpenPrecedent from a generic event store.

- `artifact`
  Any external evidence, record, or output linked to the decision, such as a code diff, PR thread, chat message, meeting note, contract clause, ticket, dashboard snapshot, or report.

- `precedent`
  A preserved historical decision sample that is worth reusing later.
  A precedent is not just "a decision that happened."
  It is a decision record retained with enough context to be relevant to later judgment.

- `applicability`
  The explicit or inferred boundary describing when a precedent is relevant, when it is not, and which constraints must still match.

- `invalidation` or `supersession`
  Signals that a precedent was later replaced, overruled, expired, or limited by newer information.

These objects should be more stable than any one domain taxonomy.
If the core model depends too heavily on repository, PR, ticket, or coding-specific language, it will not generalize cleanly.

### Cross-domain stable decision fields

For the core `decision` and `precedent` layer, the following fields are the most likely to remain useful across domains:

- `context`
  The local situation in which the decision happened.
  This should capture enough surrounding state to understand the pressure and scope of the choice.

- `candidate_options`
  The meaningful options that were available or considered at the time.

- `chosen_option`
  The path that was actually selected.

- `default_path`
  The standard, mainstream, or expected path that would usually have been taken if no special constraint had intervened.

- `deviation_reason`
  A concise explanation of why the chosen path differed from the default path.

- `constraints`
  The conditions that materially shaped the decision.
  These may include customer-specific requirements, approval boundaries, compatibility constraints, safety rules, cost ceilings, personal preferences, policy restrictions, or time pressure.

- `rejected_reasons`
  Why other meaningful options were not selected.
  This matters because future agent behavior often needs to avoid rediscovering the same rejected path.

- `decision_actor`
  Who primarily produced the judgment:
  human, agent, or a human-agent combination.

- `authority_boundary`
  Whether the decision touched approval, ownership, delegation, or responsibility boundaries.

- `evidence_refs`
  Which artifacts, records, or runtime observations were used as evidence at the time.

- `outcome`
  What later happened after the decision.
  This may remain unknown at first, but the model should allow it.

- `temporality`
  Whether the decision was intended as long-term, temporary, transitional, emergency-only, or explicitly local.

- `applicability`
  The circumstances under which this precedent should still be considered relevant in future situations.

- `superseded_by` or `invalidated_by`
  Later links that show the precedent should no longer be followed as originally recorded.

Not every field must be fully populated in early capture.
But these fields describe the semantic shape of a reusable precedent much better than domain-specific labels.

### What should remain domain-specific

Several important parts of the system should not be forced into one universal schema too early:

- decision taxonomy
  Software teams may talk about architecture choice, compatibility trade-offs, defect repair, and release cuts.
  Sales teams may talk about discounting, concession boundaries, and approval exceptions.
  Industrial teams may talk about safety overrides, degradation modes, and manual control transitions.

- trigger moments
  The right capture moment differs by domain.
  In coding it may be before writing, during planning, or after failure.
  In sales it may be before a quote or commitment.
  In operations it may be before escalation, rerouting, or manual intervention.

- evidence sources and connectors
  Repositories, chat systems, ticketing, CRM, ERP, sensor streams, dashboards, calendars, and email all differ materially.

- usefulness metrics
  A coding workflow may care about rework and wrong default implementations.
  A sales workflow may care about margin erosion, approval breaches, or bad commitments.
  An industrial workflow may care about downtime, safety incidents, or unstable overrides.

Trying to flatten these into one generic workflow model too early would make the system look universal while actually weakening it.

### Recommended product layering

The most defensible long-term shape is a three-layer system:

- `core precedent layer`
  The stable object model for case, event, decision, artifact, precedent, applicability, and invalidation.

- `domain adaptation layer`
  Domain-specific taxonomies, trigger points, connectors, and evaluation logic.

- `runtime usage layer`
  The place where precedent is surfaced during planning, approval, exception handling, recovery, or other decision moments.

Without the core layer, OpenPrecedent becomes a collection of unrelated vertical workflows.
Without the domain layer, it becomes an abstract shell that is too generic to be operationally useful.
Without the runtime layer, it degrades into a passive archive.

### Two failure modes to avoid

There are two opposite abstraction failures:

- over-generalization
  The model becomes elegantly abstract but operationally empty.
  It can describe many domains, but it does not tell any domain where to capture, what matters, or how to prove usefulness.

- over-specialization
  The model bakes in the language of one initial wedge so deeply that later domains cannot reuse the same core without schema distortion.

The design goal is not to prove that all agent domains are identical.
The goal is to identify the smallest stable semantic core of precedent and keep everything else adaptable.

### Working heuristic

The safest working heuristic is:

OpenPrecedent should not model domain workflows as its primary abstraction.
It should model historically grounded judgment under constraints.

That framing is more likely to survive expansion beyond coding agents while still supporting a narrow first wedge.

## The Product Problem

Users do not want a decision database for its own sake.
They want a reliable way to recover and reuse the judgment structure behind earlier work.

The risk is not only that an agent forgets facts.
The deeper risk is that an agent or later human operator forgets:

- why a direction was chosen
- what constraints mattered at the time
- which options were considered and rejected
- which approvals or authority boundaries mattered
- where a customer or project required a non-standard exception

If those signals are absent, later iterations may still look competent while moving in the wrong direction.

## Why Existing Approaches Break Down

OpenPrecedent should not be justified by claiming that existing systems record nothing.
They do record many adjacent things, but they usually do not preserve reusable judgment structure in the right place or form.

Existing infrastructure usually records one of the following:

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

Manual decision-entry systems are also an obvious substitute, but they usually fail as the primary capture mechanism for high-value exceptions.
The main reasons are:

- the extra workflow cost appears exactly when teams are busy, under pressure, or handling exceptions
- people rarely know in the moment which temporary-looking choice will become historically important later
- manually written summaries drift away from the actual execution path, evidence, and decision timing

Manual systems can still be useful as a supplement.
They are much weaker as the main way to preserve high-value exception decisions.

## Why The Agent Era Changes The Need

OpenPrecedent becomes more necessary in the agent era because decision-making moves from a relatively low-frequency organizational activity into a high-frequency execution activity.

Compared with mostly human-driven work, agent-assisted work changes several fundamentals:

- decision density increases sharply during one task
- many decisions are co-produced through human-agent interaction rather than only through human-human discussion
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

## What A Precedent Is And Is Not

One critical risk is to confuse recorded decisions with timeless correct answers.
That would make the system actively dangerous.

A precedent may be:

- wrong even at the time it was made
- only valid under narrow local constraints
- later invalidated by product, customer, architecture, or organizational change

So OpenPrecedent should not treat precedent as policy or ground truth.
It should treat precedent as contextualized historical judgment.

These failure modes are different:

- a wrong decision means the original judgment itself was bad
- a locally valid decision means the judgment was acceptable only under narrow constraints
- a later-invalid decision means the judgment may have been good once but has aged out

They also create different risks:

- wrong precedents can amplify historical mistakes
- locally valid precedents can be over-generalized into places where they do not belong
- expired precedents can anchor future work on assumptions that no longer hold

So the danger is not just bad data.
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

This implies a clear product boundary:

- OpenPrecedent should surface candidate precedent, not silently enforce historical imitation
- retrieval quality depends on matching constraints and applicability, not only semantic similarity of topic or wording
- the system becomes stronger when it can preserve later correction, supersession, or invalidation rather than only the original choice

Pollution control should therefore be layered rather than absolute.
An early product cannot wait for perfect governance before it captures anything useful.
The more realistic approach is:

- capture the decision with its surrounding constraints while the context is still fresh
- allow later enrichment with result, supersession, or invalidation signals when they become known
- present retrieved precedent as something to examine and test against the current situation, not something to obey automatically

## What Should Be Captured

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

The generalized rule is:

OpenPrecedent should prioritize the decisions that are least recoverable from the final artifact but most important for later judgment.

For the first phase, the priority should be narrower:

OpenPrecedent should first capture exception-driven decisions under real constraints, especially the places where a default or mainstream path would normally have been chosen but had to be changed because of customer requirements, historical baggage, defect-repair trade-offs, time-cut release pressure, undocumented architecture details, or temporary recovery needs.

Within that class, the most practical first real-capture slice is narrower still:

OpenPrecedent should start with implementation decisions where customer-specific constraints or historical compatibility constraints forced the team away from the default solution.

This slice is especially attractive because it combines:

- high consequence when repeated incorrectly
- strong tendency for future agents to revert to the mainstream answer
- weak recoverability from code alone
- natural traces across issues, PRs, runtime activity, support context, and expert clarification

A reasonable first ordering inside the initial slice is:

- customer-specific exceptions that overrode the standard product path
- compatibility or legacy constraints that overrode the preferred engineering path
- temporary or transitional fixes that were chosen knowingly under local pressure
- version-scope cuts that changed what "good enough for now" meant

## How Capture Should Work

An early OpenPrecedent deployment should not assume full automatic capture.
That assumption would be false in most real organizations because many important decisions still happen in meetings, email, chat systems, and ad hoc spoken discussion.

The more realistic early model is hybrid capture:

- automatic or near-automatic capture from agent-visible execution paths
- structured capture of human-agent interaction
- low-friction human supplementation for off-path decisions that agents could not observe directly

This means the early goal is not omniscience.
The early goal is to capture the highest-value, hardest-to-reconstruct decisions with enough context that later agents and operators can reuse them.

That boundary can be made more specific.

The product should strongly prefer automatic execution-path capture for decisions that are both high-frequency and hard to reconstruct later, such as:

- an agent proposing multiple solution paths and a human selecting one
- an agent abandoning a default path because of cost, authority, compatibility, or customer constraints
- intermediate execution decisions made by the agent that materially affect the final result even though a human never reviewed each one

The product should explicitly allow human supplementation for high-value decisions that happen outside direct agent visibility, such as:

- a meeting where a customer-specific exception is approved
- an email or chat thread where a delivery boundary is clarified
- an expert explaining why a mainstream fix is unsafe in this repository

The product does not need to force every surrounding artifact into a structured precedent record.
Many long discussions are better kept as linked evidence rather than over-modeled fields.
That is especially true for meeting notes, chat transcripts, design decks, and long email threads whose value is evidentiary more than structural.

## Candidate Jobs-To-Be-Done

OpenPrecedent should not think of itself as selling replay, storage, or retrieval in isolation.
The user is hiring it to reduce decision risk before the next meaningful action, avoid repeating already rejected reasoning, surface repository-specific and customer-specific exceptions, and shorten the path from "we solved something like this before" to "here is the part that still matters now."

Before narrowing the job itself, it helps to name the customer correctly.
The customer should not be framed too loosely as "developers" in general.
That would be as weak as describing the milkshake buyer only by age or commute demographics.

The more useful working customer model is layered:

- direct users are engineers, tech leads, delivery leads, and agent operators who repeatedly make project decisions under repository-specific or customer-specific constraints
- organizational customers are software teams and product organizations whose systems evolve over time while accumulating special cases, legacy baggage, and non-obvious exceptions
- economic buyers are usually engineering leaders, platform owners, AI workflow owners, delivery leaders, or product-line owners who are accountable for maintenance cost, rework, and operational dependence on expert memory

What these customers share is not a job title.
What they share is a recurring need to make new decisions in environments where the right answer depends on lost or fragmented prior judgment.

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

### Expected Outcome For The Customer

The customer is not hiring OpenPrecedent to own a decision archive.
The expected outcome is more operational:

- recover the constraints, exceptions, and rejected paths that still matter before making a new decision
- reduce confident-but-wrong default solutions
- reduce dependence on asking the same expert to reconstruct history again
- keep project-specific and customer-specific judgment from disappearing as teams, roles, and agent usage change

In short, the customer is hiring OpenPrecedent to reduce decision error under historical constraints, not merely to improve documentation quality.

## Substitute Solutions And Adoption Bar

Users already have many ways to solve parts of this job.
Those substitutes are the real competition.

The main substitutes are:

- non-consumption, where the user lets the agent continue and relies on intuition, luck, or later review
- human recall and expert consultation
- code search and repository history
- observability and tracing tools
- memory, RAG, and note retrieval systems
- process templates, policy docs, and checklists

The strongest substitute is usually human recall and expert consultation, because humans can reconstruct intent and exceptions better than current tools.
It is also the substitute OpenPrecedent most needs to displace over time.
That problem is structural:

- important decision context often survives only in expert memory
- expert recall is expensive and slow to access
- staff turnover and organizational change make this memory base fragile
- the longer a project runs, the harder it becomes to keep this human-only dependency maintainable

OpenPrecedent should not assume it can replace expert judgment in one step.
It should instead turn repeated expert-agent interaction into explicit precedent over time, so dependence on expert recall decreases as the corpus matures.

A user is more likely to choose OpenPrecedent when it does all of the following better than the substitute set:

- returns the relevant judgment faster than searching PRs, notes, and chat threads
- expresses the result as decision structure, not just related text
- appears at the moment of planning, writing, or recovery rather than only after the fact
- preserves repository-specific and customer-specific exceptions instead of flattening everything into generic best practice
- explains why a prior case is relevant so the result is auditable and trustworthy

Users may still choose substitutes when:

- the task is too small or low-risk to justify another step
- there is little or no prior history worth consulting
- the product returns too much raw history and not enough distilled guidance
- the best decision context still lives outside the captured corpus
- the user trusts a human expert more than the retrieved precedent
- the tool feels like another observability dashboard rather than an action-time aid

This means that better replay alone is unlikely to be enough.
If OpenPrecedent cannot beat the combined workflow of search plus human recall, it will not become a durable habit.

This also clarifies the product's core value in a simpler way.
The product is not primarily valuable because it records more history.
It is valuable because it can reduce wrong default decisions in situations where generic best practice no longer applies.

That value usually shows up through:

- less rework after following an apparently reasonable but actually invalid mainstream path
- less repeated rediscovery of already rejected reasoning
- less operational dependence on the memory of a few experts
- more stable handling of repository-specific and customer-specific exceptions

## How To Tell Whether OpenPrecedent Is Actually Useful

It is not enough to say that the system recorded decisions.
A useful precedent layer has to change later behavior, not just store more history.

The evidence ladder should therefore be explicit:

### Level 1: Capture success

The system can reliably produce precedent candidates from real work.
This only proves that the corpus exists.

### Level 2: Retrieval success

The system can return relevant prior cases when a similar situation appears later.
This proves that the stored history is retrievable at the right moment.

### Level 3: Decision-change success

The retrieved precedent changes what the agent or operator does next.
The strongest signals here are:

- the agent abandons a tempting default solution after seeing a prior exception
- the agent raises a clarification or approval need earlier than it otherwise would have
- the user or agent chooses a path that matches prior repository-specific or customer-specific constraints instead of generic best practice
- repeated reasoning that had already been rejected does not need to be rediscovered and rejected again

### Level 4: Outcome-change success

The changed behavior produces downstream benefit.
Examples include:

- less rework
- fewer confident-but-wrong default implementations
- less dependence on expert recall for recurring cases
- fewer cases where temporary fixes are mistaken for long-term design
- more stable handling of customer-specific and repository-specific exceptions

So the success bar for OpenPrecedent is not how much history was captured.
The stronger bar is whether future execution requires less guesswork, less rediscovery, and less fragile dependence on asking the right human.

## Open Source And Commercial Boundary

OpenPrecedent should not assume that open source alone or proprietary packaging alone answers the market question.
The more important question is which parts of the problem are best solved as an open precedent layer and which parts become enterprise buying reasons.

An open source foundation is especially strong for:

- the local-first precedent model
- transparent capture, replay, explanation, and retrieval primitives
- developer trust, auditability, and ecosystem adoption
- a self-hosted base for teams that want to experiment or extend the system

A proprietary or private-cloud offering only becomes defensible if it solves problems that customers struggle to assemble and maintain themselves, such as:

- enterprise deployment, tenancy, security, and compliance requirements
- connectors across repository systems, chat systems, meeting artifacts, support systems, and agent runtimes
- cross-team governance of precedent quality, invalidation, and access boundaries
- implementation support, domain-specific rollout, and operational accountability

That means the business cannot rely on "closed source" as the advantage.
It has to win on integration depth, enterprise fit, and responsibility for outcome.

This also explains why some customers will still choose a commercial offering over the open source base:

- they want faster deployment than self-assembly
- they need a vendor to own support and integration risk
- they operate under private-cloud, compliance, or data-boundary constraints
- they need precedent capture to work across more enterprise surfaces than an internal platform team can reasonably maintain

The business model should therefore be closer to organization-level capability sales than to a narrow developer-tool seat sale.
Reasonable revenue levers include:

- subscription for enterprise or private-cloud deployment
- pricing by managed projects, agent workflows, or organization scope rather than only individual seats
- professional services or implementation packages for enterprise rollout and system integration

The strategic caution is that the product should start from developer and agent workflows without getting trapped as "just another developer tool."
The deeper opportunity is an organizational decision-inheritance layer that begins in software delivery and later extends to adjacent product, delivery, and customer-exception decisions.

## Current MVP Versus Future Target

The current OpenPrecedent MVP is strongest at:

- capturing local case history
- extracting decision records
- replaying and explaining a case
- retrieving semantically related precedent from prior history

That is an important base, but it is still best understood as infrastructure that proves the loop is viable.
It is also proving that loop first inside a narrow, high-signal environment rather than across every possible agent domain at once.

The stronger future product target is narrower and more opinionated:

- surface decision lineage before the next critical action
- integrate decision-relevant signals from more than the raw runtime transcript
- preserve customer-specific and repository-specific exceptions as first-class precedent
- help agents inherit proven judgment structure instead of only retrieving adjacent text or operational similarity
- accumulate reusable precedent from expert-agent interaction so organizations get compounding returns instead of resetting to tribal memory each time people change

The future product should not become a generic graph, generic memory platform, or generic trace viewer.
Its distinctive value is decision inheritance under real project constraints.

Over time, that value should extend beyond coding agents.
The generalizable layer is not "software project history" as such.
The generalizable layer is contextual decision precedent for agent-assisted execution.
If the model is right, the same core object model should later support additional domains with domain-specific connectors, decision taxonomies, and evaluation logic layered on top.

These design questions are tightly linked rather than independent:

- pollution control defines what kind of historical judgment can be safely reused
- hybrid capture defines how that judgment enters the system in the first place
- first-slice prioritization defines where the product can start with the highest value and lowest ambiguity
- usefulness criteria define whether the product is changing downstream decisions instead of merely archiving them

## Open Questions

- How much off-transcript context should OpenPrecedent ingest directly versus reference indirectly?
- What is the smallest high-frequency trigger moment where decision-time lineage is clearly worth the workflow cost?
- How should the product distinguish stable precedent from one-off local exceptions?
- How should customer-specific exceptions be modeled without collapsing into a generic CRM or knowledge base product?
- What evidence would prove that decision-time lineage changes downstream decisions rather than merely explaining them better afterward?
- Which parts of expert judgment can realistically be externalized into precedent first, and which parts will remain expert-only for longer?

## Phase Conclusion

This JTBD round can now be treated as directionally converged.
Using the frame from *Competing Against Luck*, the key questions are no longer just "who is the user" in the abstract, but:

- in what situation the user hires the product
- what progress the user is trying to make
- what substitute set the user already uses instead

On those questions, this note now gives a coherent answer.

### What now appears answered

Users are not hiring OpenPrecedent to own a decision archive or to inspect agent logs for their own sake.
They are hiring it before a new meaningful decision so they can recover the historically relevant judgment from similar prior situations.
What they want back is the part of prior history that still matters now:

- decisive constraints
- real exceptions
- rejected options
- boundary conditions
- still-relevant trade-offs

The real substitute set is also clearer now.
It is not only tracing, observability, or memory tools.
The practical substitute set is the combined workflow of non-consumption, expert recall, code search, repository history, docs, notes, chat threads, email, memory systems, and checklists.
The strongest substitute is usually human recall and expert consultation rather than a single software product.

The discussion now explains more clearly why existing approaches are insufficient.
The problem is not that current systems store nothing.
The problem is that they do not reliably preserve reusable judgment structure.
What is especially easy to lose includes:

- why the default path stopped being valid
- which constraints forced the deviation
- which options were seriously rejected and why
- which exceptions were only locally valid
- which decisions later expired or were superseded

The analysis of the agent era is also more complete.
The agent era matters not because decisions suddenly exist, but because their density, speed, and visibility have changed.
Many decisions are now created through human-agent interaction, some are made by agents without direct human review of every step, and future execution is increasingly performed by agents that will default toward generic answers unless prior judgment is surfaced in time.
That is why precedent now matters not only for explanation after the fact, but for later execution while it is still happening.

The highest-value decision classes are also clearer.
OpenPrecedent should prioritize exception-shaped decisions that are hard to reconstruct from final artifacts but highly consequential for later maintenance and future judgment.
The leading examples identified in this round are:

- customer-specific exceptions
- historical compatibility constraints
- defect-repair trade-offs
- temporary or transitional fixes
- version cuts under time pressure
- architecture details that never fully made it into code or documentation

The common pattern is more important than the examples themselves:
the best initial precedents are decisions where a default path would normally have been taken, but a real constraint forced a different path.

The product category itself is also clearer.
OpenPrecedent should not be framed as a developer-only project precedent tool.
Its long-term category is general decision-precedent infrastructure for agent-assisted execution.
At the same time, the current wedge remains narrow: coding-agent and software-delivery work is still the first high-signal environment in which to validate the loop.

### Direct answers to the core questions

The customer should no longer be defined only as "developers."
The more accurate customer model has three layers:

- direct users who work with agents frequently and make decisions under local constraints
- organizational customers whose systems accumulate exceptions, legacy baggage, and fragile hidden judgment
- economic buyers who are accountable for maintenance burden, rework, delivery risk, or dependence on expert memory

What these users hire OpenPrecedent to do is also clearer.
They are not hiring it to own an archive.
They are hiring it so that when a new consequential decision has to be made, they do not have to guess why a similar situation was judged a certain way before.

The expected result is not abstractly "more knowledge."
The expected result is operational:

- fewer wrong default paths
- less rework
- less dependence on finding the right human expert at the right moment
- less loss of exception-specific judgment when teams change
- more agent behavior that reflects inherited experience rather than generic averaging

The shortest defensible value statement from this discussion round is:

OpenPrecedent reduces wrong default decisions.

The discussion also has a clearer answer to why manual entry systems are insufficient as the primary mechanism.
High-value decisions often happen under pressure, in exceptions, or in moments that still look temporary.
That is exactly when structured manual recording is least reliable.
Manual logging can still help as a supplement, but it is a weak default for the main capture path.

The analysis of precedent misuse is also more mature.
Precedent may be wrong when first recorded, only locally valid, or later invalidated.
So precedent must be treated as a contextual historical judgment sample rather than timeless truth.
That is why the current thesis now emphasizes:

- applicability
- invalidation and supersession
- candidate precedent rather than silent enforcement

The product also now has a cleaner answer to the generality question.
The ambition must be general, but the validation path must be specific.
So OpenPrecedent should be described as general agent precedent infrastructure, while the current wedge remains coding-agent and software-delivery validation.

### What remains unresolved

This phase can be considered directionally converged, but a few questions are still open at the product-definition level.

The minimum target customer is still not finally locked.
The discussion no longer treats "developers" as a sufficient answer, but it still has not defined the narrowest initial team profile that should adopt and buy first.

The semantic core is also clearer, but the split between core fields and enrichment fields is still not final.
The note now records a stronger candidate field set for case, decision, precedent, applicability, and related semantics, but it still does not fully distinguish:

- which fields are required for the MVP semantic core
- which fields can remain optional or arrive later as enrichment

Runtime use is also not fully defined yet.
The discussion is now clear that precedent should not be obeyed blindly, but it still has not fully specified when the product should:

- suggest a precedent
- require clarification
- block a default action
- escalate to a human
- only annotate a decision after the fact

Commercial packaging remains directional rather than final.
The open-source foundation versus enterprise private-cloud boundary is clearer, but the actual packaging model is not yet complete.

These are no longer questions of directional confusion.
They are questions for later product definition.

### Alignment with the current MVP

The current MVP is directionally aligned with this conclusion in several important ways.
It already follows the chain of case, event, decision, and precedent.
It does not define itself as a generic graph, generic memory platform, or generic trace viewer.
It already treats replay, explanation, and precedent retrieval as core capabilities.
It is already validating the idea that relevant precedent can be retrieved from prior history.
It already emphasizes local-first, single-agent validation over abstract platform claims.
And it already follows the right proof order: validate one concrete loop before expanding.

So the MVP should not be judged as having chosen the wrong direction.
It already contains the structural skeleton of the broader product thesis.

The main gap is one of level rather than direction.
The current MVP still behaves more like a foundation for capture, replay, extraction, and retrieval over existing history.
The stronger target described by this phase conclusion is decision-time judgment inheritance before the next meaningful action.

The most important remaining differences are:

- the MVP is still more focused on explaining past runs, while the conclusion emphasizes helping the next decision before it happens
- the MVP is mostly validating a local single-agent coding environment, while the conclusion defines a broader product category for agent-assisted execution across domains
- the MVP is still weak on off-path human context such as meetings, chat systems, email, and explicit expert supplementation
- the MVP does not yet center applicability, invalidation, supersession, and temporality strongly enough, even though the current conclusion treats them as crucial for preventing precedent misuse
- the MVP is still more oriented toward semantic retrieval plus replay, while the stronger thesis requires constraint-matching, exception-awareness, and historical validity checks
- the MVP does not yet explicitly present the architecture as a core precedent layer, a domain adaptation layer, and a runtime usage layer

So the best compact summary is:

The MVP has already shown that a precedent loop can run.
It has not yet fully become the general decision-precedent infrastructure described by this phase conclusion.
