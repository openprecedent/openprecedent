---
type: prd
slug: mvp-release-closeout
title: Standardize the OpenPrecedent MVP release baseline
status: draft
---

## Summary

Standardize the current OpenPrecedent MVP into a releaseable local-first baseline that can be installed, validated, and reused in new projects without reopening already-completed MVP implementation scope.


## Problem

The repository already documents MVP v1 as complete, but it is still easier to read as an active research workspace than as a standard release baseline. Before publishing an MVP release for broader reuse, the project still needs a release-facing closeout pass that clarifies the release scope, standardizes wording, improves installation and quickstart guidance, adds test coverage visibility, sets a concrete coverage gate, and defines a repeatable publication checklist.


## Goals

- treat the current local-first Rust CLI baseline as a standard research-oriented MVP release
- make the release easy to install and use in new projects without deep repository archaeology
- add coverage reporting and a concrete release coverage gate before publication
- define a repeatable validation and publication workflow for the release
- separate the published MVP baseline from later post-release research issues

## Non-Goals

- expanding the MVP scope with new product capabilities
- reopening closed core-loop implementation work
- forcing near-term adoption of long-horizon storage or capture architecture changes
- blocking the release on current post-MVP research issues such as contamination or knowledge-layer modeling

## Success Criteria

- the MVP release has an explicit release-scope and positioning document
- the repository has a standard quickstart for new-project use
- CI exposes Rust and Python coverage, and the release baseline is set to 90 percent before publication
- the repository has a documented release validation checklist and publication flow
- the release closeout clearly hands off later work to post-release research issues

## Dependencies

- existing MVP completion docs in `docs/product/`
- existing Rust CLI public interface and usage docs in `docs/engineering/cli/`
- current CI and preflight harness
