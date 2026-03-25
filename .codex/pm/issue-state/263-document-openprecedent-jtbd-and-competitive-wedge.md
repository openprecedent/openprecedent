---
type: issue_state
issue: 263
task: .codex/pm/tasks/codex-runtime-research/document-openprecedent-jtbd-and-competitive-wedge.md
title: Document OpenPrecedent jobs-to-be-done, substitute solutions, and competitive wedge
status: done
---

## Summary

First-pass English and Chinese JTBD discussion notes are in place and the GitHub issue is open for iterative review.
This issue should remain the anchor for later discussion rounds that refine OpenPrecedent's primary job, substitute solutions, and future product wedge.
The current draft now also captures a four-part design analysis around precedent contamination, hybrid capture boundaries, initial capture scope, and usefulness criteria.

## Validated Facts

- GitHub issue `#263` exists and is labeled `documentation` and `research`.
- The local task twin is `.codex/pm/tasks/codex-runtime-research/document-openprecedent-jtbd-and-competitive-wedge.md`.
- The draft living note is `docs/product/openprecedent-jtbd-and-competitive-wedge.md`.
- The aligned Chinese companion note is `docs/zh/product/openprecedent-jtbd-and-competitive-wedge.md`.
- The current note now frames OpenPrecedent primarily around new-decision judgment inheritance rather than only execution-time support.
- The note now treats human recall and expert consultation as the most important long-term substitute for OpenPrecedent to displace gradually.
- The note explicitly calls out off-transcript decision context such as meetings, Slack, IM, expert recall, and customer-specific exceptions.
- The note now makes the compounding path explicit: OpenPrecedent should accumulate reusable precedent through repeated expert-agent interaction rather than claim instant expert replacement.
- The note now identifies the highest-value precedent classes as hard-to-recover exception decisions: route changes, defect-repair trade-offs, customer-specific exceptions, time-cut version decisions, undocumented architecture details, and temporary fix choices.
- The note now makes the first-phase prioritization explicit: exception-driven decisions under real constraints should land before generic architecture commentary or broad strategy notes.
- The note now explains why existing infrastructure and manual recording systems are insufficient, and why agent-era precedent capture must sit on the execution path rather than only in after-the-fact documentation.
- The note now explains that precedent is contextual historical judgment rather than timeless truth, and that early rollout must rely on hybrid capture because many high-value decisions still happen outside direct agent visibility.
- The note now separates wrong precedents, locally valid precedents, and later-invalid precedents, and makes the product boundary more explicit: OpenPrecedent should surface candidate precedent rather than silently enforce historical imitation.
- The note now explains that contamination control should be layered: capture nearby constraints first, allow later enrichment, and treat retrieved precedent as something to re-evaluate rather than obey.
- The note now makes the hybrid-capture boundary more concrete by distinguishing execution-path auto capture, human supplementation for off-path decisions, and artifact linkage without over-structuring every discussion thread.
- The note now narrows the first real capture slice toward implementation decisions where customer-specific constraints or compatibility constraints forced a deviation from the default solution.
- The note now states usefulness as a ladder: capture success, retrieval success, decision-change success, and outcome-change success.

## Open Questions

- How much off-transcript context should future OpenPrecedent ingest directly versus reference indirectly?
- What should count as the narrowest initial product wedge: planning, before-write, failure-recovery, or approval-boundary support?
- How should customer-specific exceptions be modeled without broadening into a generic memory platform?
- What future evidence would show that lineage changes downstream decisions rather than only helping later explanation?
- Which contamination signals are realistic to capture early, and which ones require later enrichment or explicit human review?
- Among customer-specific exceptions, compatibility constraints, temporary fixes, and version cuts, which first real capture slice should be prioritized for initial runtime validation?

## Next Steps

- Use the PR for issue `#263` as the review surface for ongoing thesis corrections.
- Continue discussion and revise the living notes rather than opening duplicate strategy notes.
- Keep the English and Chinese notes aligned as later discussion rounds modify the thesis.

## Artifacts

- `docs/product/openprecedent-jtbd-and-competitive-wedge.md`
- `docs/zh/product/openprecedent-jtbd-and-competitive-wedge.md`
- `.codex/pm/tasks/codex-runtime-research/document-openprecedent-jtbd-and-competitive-wedge.md`
- `https://github.com/openprecedent/openprecedent/issues/263`
