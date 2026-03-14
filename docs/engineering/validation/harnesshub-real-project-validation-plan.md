# HarnessHub Real-Project Validation Plan

## Purpose

Use real HarnessHub development as the first cross-project Codex validation target for OpenPrecedent issue `#131`.

This work tests whether OpenPrecedent can do more than replay or explain prior Codex work inside its own repository.
The question is whether prior decision lineage and harness practice can materially improve work in a different real project.

## Repository Roles

OpenPrecedent owns the research framing:

- hypothesis
- method
- evidence standard
- interpretation of results

HarnessHub owns the local execution context:

- repository-local agent instructions
- current task handoff
- runtime setup steps used inside the repository
- the actual feature work and resulting code changes

This split keeps the research record in OpenPrecedent while allowing new Codex sessions to operate inside HarnessHub without re-reading prior chat history.

## Validation Target

HarnessHub is the first target because it is:

- a real external repository rather than an OpenPrecedent self-study
- small enough for fast iteration
- close to the agent runtime domain
- a good place to test whether OpenPrecedent harness practice transfers cleanly

## Working Product Hypotheses

### Hypothesis 1

OpenPrecedent runtime decision-lineage retrieval can improve real development judgment in HarnessHub, especially around:

- task framing
- accepted constraints
- approval and authority boundaries
- success criteria
- recovery after directional failures

### Hypothesis 2

Harness practices developed in OpenPrecedent can be reused in HarnessHub with enough fidelity to improve execution consistency across Codex sessions.

### Hypothesis 3

HarnessHub should evolve from its earlier OpenClaw-specific packaging CLI phase into an agent harness packaging tool that standardizes a reusable agent runtime environment.

## Why It Matters

If these hypotheses are supported, OpenPrecedent gains evidence that:

- precedent and lineage are useful during execution, not only after the fact
- research value extends beyond one repository
- harness practices are themselves reusable precedent

If they are not supported, the result will clarify whether the gap is in:

- retrieval quality
- workflow timing
- missing runtime signals
- overfitting to OpenPrecedent's own repository habits

## Method

Run real Codex development in HarnessHub with a shared OpenPrecedent runtime home.

Use a narrow, issue-scoped workflow:

1. start a new Codex session on a single HarnessHub issue
2. read the HarnessHub-local execution docs
3. run one `initial_planning` lineage query
4. use additional lineage queries only at:
   - `before_file_write`
   - `after_failure`
5. record when lineage changed or confirmed a decision
6. complete at least one real HarnessHub feature task under this workflow

## Minimum Harness Transfer

The first transferred harness set is intentionally small:

- repository-local `AGENTS.md` guidance
- a current issue state handoff file
- runtime setup instructions for shared OpenPrecedent state
- a standard Codex session start prompt
- a small validation todo list

This is enough to test continuity and discipline without recreating the entire OpenPrecedent harness at once.

## Evidence To Capture

The study should produce durable evidence in four categories:

1. Runtime evidence
   - lineage invocations
   - matched cases
   - returned constraints, cautions, authority signals, or task frame

2. Execution evidence
   - feature work completed in HarnessHub
   - tests added or updated
   - docs changed to reflect the new product framing or workflow

3. Behavioral evidence
   - examples where lineage changed a decision
   - examples where lineage confirmed an intended direction
   - examples where harness guardrails prevented scope drift

4. Interpretation evidence
   - final result report stating whether confidence increased, decreased, or stayed ambiguous

## Preferred Validation Task Shapes

The first HarnessHub feature task should be one of:

- manifest or schema changes for harness-oriented metadata
- stronger import or rebinding behavior for portable agent environments
- stronger verification rules for reusable agent environments
- clearer packaging boundaries between template material, state, and credentials

Avoid generic platform abstraction work unless the chosen feature truly requires it.

## Success Interpretation

This validation supports issue `#131` if:

- at least one lineage brief materially affects a HarnessHub development decision
- the transferred harness is actually used across sessions rather than documented and ignored
- the work sharpens HarnessHub's product positioning instead of introducing a vaguer one
- the resulting evidence increases confidence that OpenPrecedent can help later real project work

## Failure Interpretation

This validation weakens the hypothesis if:

- lineage retrieval is repeatedly irrelevant or noisy during real HarnessHub work
- harness transfer adds documentation burden but does not improve execution continuity
- HarnessHub feature work proceeds no better with lineage than without it

## Ambiguity Interpretation

The result remains ambiguous if:

- the feature task is too small to require meaningful judgment
- lineage is queried too rarely or at the wrong moments
- the transferred harness is too thin to test continuity seriously

In that case, a second, more demanding HarnessHub task should be run before drawing broader conclusions.

## Current Constraints

- keep the study issue-scoped
- keep the OpenPrecedent research framing in OpenPrecedent
- keep HarnessHub documents limited to local execution context
- avoid broad multi-runtime abstraction

## Related Artifacts

- [Codex runtime boundary](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-boundary.md)
- [Codex runtime startup guide](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-startup-guide.md)

## Naming Note

Earlier records in this study refer to the target repository as `ClawPack`.
That name is now historical. The active study target is `HarnessHub`, and future OpenPrecedent research documents should use that name unless they are explicitly describing the earlier phase.
