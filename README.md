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

This repository contains:

- product direction and MVP documentation
- competitive and technical research
- the initial Python implementation scaffold

## Initial Structure

```text
openprecedent/
├── docs/
│   ├── architecture/
│   ├── engineering/
│   ├── product/
│   └── research/
├── scripts/
├── src/
└── tests/
```

## Near-Term Roadmap

- phase 0: align strategy, MVP, design, and technical direction
- phase 1: define core schemas for case, event, decision, artifact, and precedent
- phase 2: build minimal event ingestion and replay APIs
- phase 3: implement first decision extraction pipeline
- phase 4: implement case-level precedent retrieval
- phase 5: validate the full loop against a local agent runtime

## Current Stack Direction

- Python first
- Rust later for engine-grade components if real bottlenecks appear
- FastAPI + Pydantic for the first executable layer

## Current Status

The repository now includes:

- local import and collector flows for OpenClaw session transcripts
- fixture-based evaluation
- collected-session evaluation/reporting
- operational `systemd` and `cron` templates plus installer script for collector scheduling

## How To Use It

- usage guide for humans and agents: [docs/engineering/using-openprecedent.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/using-openprecedent.md)
- runtime decision-lineage validation baseline: [docs/engineering/openclaw-runtime-decision-lineage-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-runtime-decision-lineage-validation.md)
- real OpenClaw runtime decision-lineage validation: [docs/engineering/openclaw-real-runtime-decision-lineage-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/openclaw-real-runtime-decision-lineage-validation.md)

## License

Apache-2.0
