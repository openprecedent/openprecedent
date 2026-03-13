---
type: prd
slug: public-interface-evolution
title: Public interface evolution
status: draft
---

## Summary
Define how OpenPrecedent evolves from an MVP-era Python-and-script command surface into a long-lived, Rust-based public CLI that remains the stable external interface for humans, skills, and automation.

## Problem
OpenPrecedent's current executable story is split between a Python CLI and multiple repository-local shell wrappers. That makes the effective public interface unstable and implementation-bound:

- external automation can end up depending on repository-local scripts instead of a product CLI
- skills can fail due to shell composition or path assumptions even when the underlying product capability is present
- the current top-level command taxonomy reflects MVP plumbing rather than a long-term public object model
- the Python CLI is the current implementation, not a deliberately designed public contract

Without an intentional interface-evolution plan, OpenPrecedent risks letting temporary research wrappers harden into the de facto product API.

## Goals
- make a Rust-based `openprecedent` CLI the sole long-term public executable interface
- define a stable command tree, output contract, configuration model, and error contract
- remove public dependence on repository-local shell wrappers
- remove the public Python CLI after Rust cutover
- separate product CLI concerns from repository-internal PM and harness tooling
- preserve persisted runtime-home and storage compatibility during interface migration

## Non-Goals
- preserving Python CLI as a long-term public fallback
- preserving public shell wrappers as parallel public entrypoints
- designing a generic SDK or plugin framework in the same initial step
- redesigning hosted service or HTTP API strategy in the same workstream
- treating repository-internal PM commands as part of the product CLI surface

## Success Criteria
- the repository contains a design baseline for the Rust public CLI and its migration path
- there is a dedicated epic and issue chain for public CLI evolution
- the design explicitly defines one-way cutover to Rust CLI and removal of public Python CLI and shell wrappers
- skill integration is planned against stable CLI commands and JSON outputs rather than scripts
- future implementation issues can execute against the design without inventing command hierarchy or contract rules ad hoc

## Dependencies
- the shipped MVP case, event, replay, decision, precedent, capture, and lineage flows
- the current runtime-home and SQLite persistence contract
- research findings showing that shell-wrapper-based skill integration is less stable than direct CLI invocation
