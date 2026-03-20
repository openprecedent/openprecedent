# HarnessHub Research Artifact Index

Date: 2026-03-20

This directory contains timestamped sanitized research snapshots for HarnessHub-related OpenPrecedent studies.

The snapshots are preserved as historical point-in-time archives.
They are not all incremental.
Some early archives capture milestone snapshots during the first-phase study, while the newest closeout archive is a cumulative snapshot that intentionally includes earlier matching records.

## Phase Index

### First-Phase Validation Archives

These snapshots belong to the first HarnessHub validation line that culminated in issue `#131`.
They record milestone evidence while the project moved from empty matched cases to the first successful live reuse.

- `2026-03-12T035639Z`
  - early first-phase sanitized snapshot
- `2026-03-12T072058Z`
  - first-phase milestone snapshot
- `2026-03-12T073347Z`
  - first-phase milestone snapshot
- `2026-03-12T075659Z`
  - first-phase milestone snapshot
- `2026-03-12T080016Z`
  - first-phase milestone snapshot
- `2026-03-12T092548Z`
  - later first-phase empty-match diagnostic wave
- `2026-03-12T164942Z`
  - first strong live-reuse evidence with non-empty `matched_case_ids`
- `2026-03-13T082811Z`
  - post-first-phase follow-up positive evidence before the second-phase reliability study was formalized

### Second-Phase Reliability Closeout Archive

This snapshot belongs to the second-phase reliability study closed by issue `#220`.

- `2026-03-20T043601Z`
  - cumulative closeout snapshot for the second-phase study
  - includes matching HarnessHub invocation records from earlier phases as well as the later release, governance, PRD, and `v0.2.0` implementation rounds
  - should not be interpreted as "only the newly added `#220` data"

## How To Read These Archives

- Use the timestamped subdirectory `README.md` files for per-snapshot metadata.
- Use `docs/engineering/validation/` for the derived human-readable interpretation.
- When citing first-phase feasibility evidence, prefer the first-phase milestone snapshots above.
- When citing the final second-phase reliability closeout, prefer `2026-03-20T043601Z` together with:
  - `docs/engineering/validation/harnesshub-second-phase-observation-log.md`
  - `docs/engineering/validation/harnesshub-second-phase-reliability-closeout.md`
