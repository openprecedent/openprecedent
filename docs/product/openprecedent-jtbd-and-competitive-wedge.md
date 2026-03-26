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

## Current Product Thesis

OpenPrecedent should become a judgment-inheritance layer for agents and operators.
Its job is not to store more history for its own sake.
Its job is to preserve and retrieve the prior judgment that still matters when a new decision has to be made under real project constraints.

That matters most when critical context is fragmented across runtime history, human discussion, customer-specific exceptions, and expert memory.
The strategic path is not instant expert replacement.
The strategic path is to capture precedent during real expert-agent work, so reusable judgment compounds over time and dependence on fragile human recall gradually decreases.

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

The stronger future product target is narrower and more opinionated:

- surface decision lineage before the next critical action
- integrate decision-relevant signals from more than the raw runtime transcript
- preserve customer-specific and repository-specific exceptions as first-class precedent
- help agents inherit proven judgment structure instead of only retrieving adjacent text or operational similarity
- accumulate reusable precedent from expert-agent interaction so organizations get compounding returns instead of resetting to tribal memory each time people change

The future product should not become a generic graph, generic memory platform, or generic trace viewer.
Its distinctive value is decision inheritance under real project constraints.

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
