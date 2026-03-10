---
type: task
epic: local-runtime-validation
slug: collector-rollout
title: Roll out scheduled OpenClaw collector in a real target environment
status: done
labels: feature,ops
issue: 23
---

## Context

The collector command, wrapper script, and scheduling assets already exist, but the roadmap still treats real scheduled execution in the target machine environment as unfinished. This task is the operational prerequisite for the rest of the runtime-validation loop.

## Deliverable

Run the OpenClaw collector on a real schedule in the target environment and verify that repeated runs advance the local state cursor without duplicating imported sessions.

## Scope

- install the collector using the documented `systemd` or `cron` path
- confirm the state file advances correctly across repeated runs
- confirm imported sessions appear in the database as expected
- document the validated runtime path and any environment-specific caveats

## Acceptance Criteria

- at least one real target environment is running scheduled collection
- repeated collector runs do not duplicate previously imported sessions
- the validated rollout path and caveats are captured in-repo or in the linked PR
- the first collected-session evaluation report is produced or summarized after rollout

## Validation

- run `openprecedent runtime collect-openclaw-sessions --limit 1` on the target environment
- inspect collector state and imported cases after repeated runs
- run `openprecedent eval collected-openclaw-sessions ...` against the collected sessions after rollout

## Implementation Notes

This task likely needs a host with access to real OpenClaw sessions, so it may be blocked on target-environment access even if the repository-side code is already ready.
