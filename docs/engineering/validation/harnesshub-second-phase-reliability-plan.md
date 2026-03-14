# HarnessHub Second-Phase Reliability Plan

## Purpose

Define the post-closeout HarnessHub research plan for issue `#217`.

The first-phase study closed issue `#131` by proving that OpenPrecedent can retrieve and reuse imported HarnessHub precedent during later live development.
This plan does not reopen that feasibility question.
Its job is to determine whether the same behavior remains reliable across repeated later HarnessHub rounds after the Rust CLI cutover and private-skill refactor.

## Boundary From First-Phase Closeout

The first-phase study established:

- live HarnessHub development can return non-empty `matched_case_ids`
- imported prior HarnessHub cases can materially shape a later product decision
- the major early gaps were pipeline closure first and retrieval quality second

The second-phase study starts after that conclusion.
It should evaluate reliability, not re-argue whether external-project reuse is possible at all.

## Existing Positive Evidence Carried Forward

The reliability study begins with two known positive anchors:

- `research-artifacts/harnesshub/2026-03-12T164942Z/`
  - preserves the first strong live-reuse milestone for issue `#67`
  - contains `16` sanitized HarnessHub invocations
  - includes the first non-empty live `matched_case_ids`
- `research-artifacts/harnesshub/2026-03-13T082811Z/`
  - preserves later positive evidence after the first-phase closeout boundary
  - contains `18` sanitized HarnessHub invocations
  - shows that live non-empty matches were not limited to one single round

These anchors are enough to justify a reliability study, but not enough to claim long-run reliability already.

## Duplicate Archive Note

The local snapshot `research-artifacts/harnesshub/2026-03-12T165042Z/` is not treated as a separate milestone.
It duplicated the sanitized invocation payload from `research-artifacts/harnesshub/2026-03-12T164942Z/` rather than contributing a new round of evidence.

The second-phase study should keep that exclusion explicit so future archive reviews do not mistake duplicate snapshots for added experimental depth.

## Additional Positive Evidence After The First-Phase Boundary

The `2026-03-13T082811Z` archive adds two later invocations:

- `rtinv_f5134ab644ed`
- `rtinv_1b35aaa5fc0c`

Both returned non-empty `matched_case_ids` during a later HarnessHub round focused on Chinese product-strategy and staffing documents.
That makes the archive useful as an initial signal that live reuse continued after the first-phase closeout point.

It does not, by itself, prove reliability.
The task shape is different from issue `#67`, and one more positive round is still too small a sample.

## Research Question

After the Rust CLI and private-skill refactor, does HarnessHub decision-lineage retrieval remain reliably invoked and materially useful across repeated real development rounds?

## Secondary Questions

- when lineage is not used, is the gap caused by invocation-adherence failure or retrieval-quality failure
- when lineage is invoked, do non-empty matches remain semantically relevant
- when non-empty matches are returned, do they still materially influence live task framing or decision narrowing
- at what point does the dominant unanswered question stop being reliability and become contamination control under issue `#163`

## Hypotheses

### Hypothesis 1

The Rust CLI and updated private skill should improve invocation reliability by reducing shell-path friction and making the lineage entry surface more stable across sessions.

### Hypothesis 2

Later HarnessHub rounds should continue to return non-empty matches often enough to show that the `#67` success case was not an isolated coincidence.

### Hypothesis 3

When matches are returned, they should still contribute observable decision value rather than only generic process discipline.

## Method

Run repeated real HarnessHub development rounds under the current private skill and Rust CLI boundary.

For each round:

1. confirm OpenPrecedent availability through the current project-local invocation path
2. record whether `initial_planning` and `before_file_write` lineage invocations occur
3. preserve a sanitized archive milestone after the round
4. record whether the returned brief was empty, useful, or contaminated
5. classify the round as success, failure, or ambiguity

## Round Structure

### Round 1: Invocation Adherence

Goal:
verify that the Rust CLI plus private-skill surface reliably produces lineage invocations at the intended stages.

Primary outputs:

- invocation present or absent
- CLI friction or skill-loading failures
- whether the round ended without ever touching the lineage path

### Round 2: Retrieval Usefulness

Goal:
verify whether invoked rounds return non-empty and semantically relevant briefs often enough to count as useful.

Primary outputs:

- matched-case presence
- semantic relevance of the returned cases
- whether the brief changed or confirmed the task framing

### Round 3: Reuse Durability

Goal:
verify that precedent continues shaping later live decisions beyond one successful moment.

Primary outputs:

- repeated live-impact evidence
- or a clear regression diagnosis if later rounds degrade

## Success Signals

The study supports reliability if:

- at least three new HarnessHub rounds are observed under the post-cutover interface
- lineage invocation occurs often enough at the intended points to count as expected workflow behavior rather than accident
- at least two later rounds produce non-empty or otherwise clearly useful lineage output
- at least one later round shows direct decision impact grounded in retrieved precedent

## Failure Signals

The study weakens reliability if:

- repeated rounds complete without any lineage invocation even though OpenPrecedent is available
- invocations occur but returned matches regress to consistently empty results
- non-empty results are mostly irrelevant or unusable in practice

## Ambiguity Signals

The study remains ambiguous if:

- invocations occur only sporadically and the sample stays too small
- briefs are non-empty but their practical effect on decisions remains unclear
- later tasks are too heterogeneous to compare without tighter grouping

## Evidence And Archive Policy

Each future round should end with:

- one observation entry
- one sanitized archive milestone under `research-artifacts/harnesshub/`
- one explicit interpretation: success, failure, or ambiguity

The second-phase study should keep those artifacts separate from issue `#131` rather than modifying the first-phase archive trail.

## Relationship To Issue 163

Issue `#217` is about reliability.
Issue `#163` is about contamination control.

The two are related but not identical:

- `#217` asks whether the workflow reliably invokes and returns useful precedent
- `#163` asks how to prevent partially related precedent from contributing misleading constraints, cautions, or framing

If later rounds show that the workflow is invoked consistently but the main failures are irrelevant or mixed-quality matches, the dominant question should move from `#217` to `#163`.

## Exit Criteria

Issue `#217` can close when one of these is true:

- repeated post-cutover rounds show reliable invocation plus repeated useful precedent reuse
- repeated rounds show a clear regression pattern and the repository records that result explicitly
- the study reaches the point where contamination control, not reliability, is the main blocker and the work should hand off to `#163`

Until then, later HarnessHub evidence should be archived as phase-two material rather than folded back into the first-phase closeout.
