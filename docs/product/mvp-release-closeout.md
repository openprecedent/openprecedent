# OpenPrecedent 0.1.0 MVP Release Closeout

## Summary

OpenPrecedent `0.1.0` is now standardized as a publishable MVP baseline for local-first, research-oriented use in new projects.

This closeout does not claim that product research is finished. It records that the MVP baseline is sufficiently defined, validated, and documented to be published without reopening MVP scope, while later improvements return to the post-release research queue.

## What The MVP Release Baseline Includes

The `0.1.0` MVP release baseline now includes:

- a stable Rust `openprecedent` public CLI
- local SQLite-backed case, event, decision, replay, and precedent workflows
- OpenClaw import and collection support
- documented new-project quickstart and usage guidance
- a scoped `90%` MVP coverage gate
- a release-blocking validation checklist
- a standard publication flow and release-notes template

Together, these define the current publishable product boundary for a local-first, developer-facing MVP.

## Release-Closeout Issues Completed

The MVP release baseline was standardized through these completed child issues:

- `#244` frame the release-closeout plan
- `#246` add Python and Rust coverage reporting
- `#243` enforce the `90%` scoped MVP coverage gate
- `#245` define the MVP release scope and positioning
- `#249` unify versioning and release wording
- `#248` add the MVP quickstart and new-project installation guide
- `#251` codify the MVP release validation checklist
- `#247` define the standard publication flow and release artifacts

## Release Record

The release baseline should be understood through these reference documents:

- [mvp-release-scope.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-scope.md)
- [mvp-quickstart.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/mvp-quickstart.md)
- [mvp-release-validation-checklist.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-validation-checklist.md)
- [mvp-release-publication-flow.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-publication-flow.md)
- [mvp-release-notes-template.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-notes-template.md)
- [mvp-status.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-status.md)

These documents together answer:

- what the MVP release is
- what it includes
- how a new project adopts it
- what must pass before publication
- how publication should be carried out

## What Is Explicitly Handed Back To Post-Release Research

The following open issues are not MVP blockers and now clearly belong to post-release research:

- `#163` contamination controls for decision-lineage retrieval
- `#224` reusable-knowledge layer above cases
- `#225` fact-versus-prescription modeling
- `#226` memory utility versus context cost
- `#227` smaller retrieval units
- `#235` explicit adoption tracking
- `#236` explicit miss classification
- `#237` lightweight closeout capture
- `#240` hybrid semantic-plus-passive capture research
- `#241` graph-shaped semantics and long-horizon storage evolution

The umbrella issue for that next stage remains:

- `#100` Define the post-MVP research evolution framework for OpenPrecedent

## Final Interpretation

The repository should now be read in two layers:

1. a published `0.1.0` MVP release baseline that is stable enough for new-project adoption
2. a post-release research program that continues to improve retrieval quality, explainability, and long-horizon architecture only after that baseline

That separation is the main point of this closeout.
