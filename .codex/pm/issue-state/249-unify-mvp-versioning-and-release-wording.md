---
type: issue_state
issue: 249
task: .codex/pm/tasks/mvp-release-closeout/unify-mvp-versioning-and-release-wording.md
title: Unify MVP versioning and release wording
status: in_progress
---

## Summary

Normalize release-facing wording and version presentation so the published MVP reads as one coherent release rather than a mix of implementation history and bootstrap-era terminology.

## Next Steps

- replace public `bootstrap` wording with MVP release wording on the Rust CLI version surface
- normalize the release-facing docs around one phrase: `OpenPrecedent 0.1.0 MVP release`
- keep internal migration or implementation-history language out of the public MVP surface

## Outcome

- Release-facing docs now consistently describe the published baseline as the `OpenPrecedent 0.1.0 MVP release`.
- The public Rust CLI version surface now renders `openprecedent 0.1.0 (mvp)` instead of a bootstrap-era phase label.
- The English and Chinese MVP architecture docs now align on the same versioned MVP wording.
