---
type: task
epic: real-history-quality
slug: resolve-local-test-runner-before-reporting-missing-pytest
title: Resolve repository-local test runner before reporting missing pytest
status: done
task_type: implementation
labels: ops,test
issue: 164
---

## Context

Agents have repeatedly attempted to run a bare `pytest` command, observed that it was not available on the global `PATH`, and then reported test execution as blocked.
In this repository, that response is a harness failure rather than a true environment diagnosis because the local workflow already standardizes repository-local Python entrypoints, virtualenv usage, and wrapper scripts.

## Deliverable

Define and implement the smallest reliable local harness rule so test execution resolves the repository-local Python or pytest path before reporting that `pytest` is unavailable.

## Scope

- define the preferred repository-local test runner resolution order
- add the smallest practical local guardrail, wrapper, or fail-fast script update
- ensure the fallback path produces a clear message only after repository-local resolution is exhausted
- document the expected behavior in contributor-facing workflow guidance

## Acceptance Criteria

- the repository defines one preferred local test runner resolution path
- the harness checks repository-local Python or virtualenv entrypoints before treating missing `pytest` as a blocker
- user-facing failure messaging distinguishes command-resolution mistakes from real dependency absence
- automated regression coverage exists for the chosen guardrail where practical

## Validation

- run targeted regression coverage for the chosen guardrail or wrapper
- verify the documented preferred command path matches the implemented resolution order
- confirm the harness no longer fails fast on a missing global `pytest` when a repository-local runner is available

## Implementation Notes

- Prefer reusing the repository's existing `.venv` and `OPENPRECEDENT_PYTHON_BIN` conventions instead of adding a second parallel setup path.
- This is a harness-gap closure item and should be completed on its own issue branch rather than piggybacked onto product work.
