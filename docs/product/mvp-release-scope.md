# OpenPrecedent MVP Release Scope

2026-03-20

## Release Positioning

OpenPrecedent `0.1.0` MVP release should be understood as a:

- local-first release
- research-oriented release
- developer-facing release

It is a standard baseline that new projects can install and use directly, but it is not positioned as a hosted platform or a finished production control plane.

## Intended Audience

This MVP release is for:

- developers who want a stable local CLI for decision replay and precedent work
- researchers validating decision-lineage and precedent reuse on real local history
- agent builders who can import or emit structured local history into OpenPrecedent

## Included In This Release

The MVP release includes:

- the Rust `openprecedent` CLI as the stable public interface
- local SQLite-backed storage for `case`, `event`, `decision`, `artifact`, and `precedent`
- replay, explanation, and precedent retrieval over stored local history
- OpenClaw transcript import and local collection flows
- fixture-backed and real-history evaluation flows
- documented local validation and release-readiness workflows

## Strongest Supported Usage Path

The strongest supported MVP path today is:

1. work in a local single-agent runtime
2. import or collect local OpenClaw history into OpenPrecedent
3. extract decisions
4. replay and explain cases
5. retrieve similar precedent from local history

The release also supports direct CLI-driven case and event creation, but the OpenClaw-first path is the most validated usage mode.

## What This Release Is Not

This MVP release is not:

- a hosted SaaS product
- a multi-agent orchestration system
- a generic graph database or memory platform
- a promise of broad runtime integration coverage
- a guarantee that all current research paths are complete

## Supported Stability Boundary

For this release, the stable public product boundary is:

- the Rust `openprecedent` CLI
- the documented local-first data model and workflows behind that CLI

Repository-local harness tooling, PM tooling, and current post-MVP research instrumentation may remain important for repository development, but they are not the primary public release contract.

## Relationship To Current Research

The current open research issues are post-release work, not MVP blockers.

They should be read as:

- quality and retrieval research
- explanation and observability research
- longer-horizon architecture research

They do not mean the MVP core loop is unfinished.

## Release Gate Implication

When later release-readiness issues define coverage and checklist gates, they should measure the MVP release baseline against this scope rather than against every repository-local support surface.

For the concrete release-blocking checklist, see:

- [mvp-release-validation-checklist.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-validation-checklist.md)
