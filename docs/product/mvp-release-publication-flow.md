# OpenPrecedent 0.1.0 MVP Release Publication Flow

## Purpose

This document defines the standard publication flow for the OpenPrecedent `0.1.0` MVP release.

The goal is to make MVP publication repeatable and auditable without pretending that this first release already needs a heavy distribution stack. The release should be easy for a new project to obtain and verify, while keeping the first publication surface aligned with the current local-first, research-oriented product boundary.

## Chosen First-Release Artifact Strategy

For the `0.1.0` MVP release, the standard published artifacts are:

1. a validated release commit on `main`
2. a Git tag named `v0.1.0`
3. a GitHub Release attached to that tag
4. release notes that summarize scope, validation, and known non-blocking caveats
5. the standard GitHub-generated source archives for the tagged release

This first release does not require prebuilt binaries, package-registry publication, or hosted runtime services.

That is intentional:

- the current MVP is local-first and developer-facing
- the quickstart already uses the supported source-build path
- forcing prebuilt binary distribution now would add operational complexity before the repository has fully validated its longer-term release needs

## How A New Project Obtains The Published MVP

The standard new-project acquisition path for the first release is:

1. open the GitHub Release for `v0.1.0`
2. download the tagged source archive or clone the repository at that tag
3. follow the published quickstart
4. build or install the Rust CLI from the tagged source

This keeps the public release path consistent with the current quickstart and avoids introducing a second, less-tested installation story.

## Required Inputs Before Publication

Before creating the release:

- the release scope and positioning must be current
- the MVP release validation checklist must pass
- the release notes draft must reflect the actual shipped scope
- the final release closeout issue must still be pending, because it records the publication result after the release is created

Reference documents:

- [mvp-release-scope.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-scope.md)
- [mvp-release-validation-checklist.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-validation-checklist.md)
- [mvp-quickstart.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/mvp-quickstart.md)

## Standard Publication Steps

### 1. Verify the release candidate commit

Run the release-blocking checklist against the intended release commit.

If any blocking step fails, stop the publication flow and fix the issue first.

### 2. Prepare release notes

The release notes should summarize:

- what the `0.1.0` MVP release includes
- the intended user and environment
- the supported installation path
- the strongest validated usage mode
- known non-blocking caveats

For consistency, start from the repository template:

- [mvp-release-notes-template.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-notes-template.md)

### 3. Create the release tag

Create the release tag on the validated commit:

```bash
git checkout main
git pull --ff-only upstream main
git tag -a v0.1.0 -m "OpenPrecedent 0.1.0 MVP release"
git push upstream v0.1.0
```

### 4. Create the GitHub Release

Create a GitHub Release for `v0.1.0` using the prepared release notes.

The release page should:

- point to the MVP release scope
- point to the quickstart
- point to the release validation checklist or closeout record
- make it clear that the supported acquisition path is from the tagged source

### 5. Confirm the published acquisition path

After the release is live, verify that a new project can still follow the documented path from the published tag:

- acquire the tagged source
- install the CLI from source
- run the quickstart successfully

## What This Flow Deliberately Does Not Do Yet

This first MVP publication flow does not yet include:

- multi-platform binary build and upload
- package-registry publication
- automated release signing and provenance pipelines
- hosted service deployment

Those may become appropriate later, but they are not required for publishing the current research-oriented MVP baseline.

## Why This Strategy Is Sufficient For The MVP

The current release is already strongest when:

- the user is technical
- the workflow is local-first
- the Rust CLI is built from source
- the goal is to validate real usage, not maximize installation convenience for a broad audience

So the first publication flow should optimize for clarity and repeatability, not for premature distribution complexity.
