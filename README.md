# OpenPrecedent

Open decision replay and precedent layer for agents.

## What It Is

OpenPrecedent is an open-source project for capturing agent execution history, extracting key decisions, replaying why those decisions happened, and turning past cases into reusable precedent.

The first target runtime is a local single-agent workflow such as OpenClaw. The initial product loop is:

1. Capture a case
2. Structure the event timeline
3. Extract decision records
4. Replay and explain decisions
5. Retrieve similar precedent

## Repository Scope

This repository is for the executable project and implementation artifacts.

Product and research documents currently live in `/workspace/01-product/` and can be migrated into this repository over time as needed.

## Initial Structure

```text
openprecedent/
├── docs/
├── scripts/
├── src/
└── tests/
```

## Near-Term Goals

- Define the event schema for case capture
- Define the decision record schema
- Build a minimal replay API
- Build precedent retrieval for historical cases
- Validate the loop against a local agent runtime

## License

Apache-2.0
