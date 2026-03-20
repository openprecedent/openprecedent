# OpenPrecedent

Open decision replay and precedent layer for agents.

## What It Is

OpenPrecedent is an open-source project for capturing agent execution history, extracting key decisions, replaying why those decisions happened, and turning past cases into reusable precedent.

The current published release should be read as the OpenPrecedent `0.1.0` MVP release: a local-first, research-oriented, developer-facing baseline rather than a hosted platform or a finished enterprise product.

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

For the current release-facing scope and positioning, see:

- [docs/product/mvp-release-scope.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-scope.md)

## How To Use It

- quickstart for a new local project: [docs/engineering/cli/mvp-quickstart.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/mvp-quickstart.md)
- usage guide for humans and agents: [docs/engineering/cli/using-openprecedent.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/using-openprecedent.md)
- MVP release scope and positioning: [docs/product/mvp-release-scope.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-scope.md)
- MVP release closeout: [docs/product/mvp-release-closeout.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-closeout.md)
- MVP release validation checklist: [docs/product/mvp-release-validation-checklist.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-validation-checklist.md)
- MVP release publication flow: [docs/product/mvp-release-publication-flow.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-publication-flow.md)
- runtime decision-lineage validation baseline: [docs/engineering/validation/openclaw-runtime-decision-lineage-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-runtime-decision-lineage-validation.md)
- real OpenClaw runtime decision-lineage validation: [docs/engineering/validation/openclaw-real-runtime-decision-lineage-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-real-runtime-decision-lineage-validation.md)
- Codex runtime research boundary: [docs/engineering/runtime/codex-runtime-boundary.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-boundary.md)
- Codex runtime workflow: [docs/engineering/runtime/codex-runtime-decision-lineage-workflow.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-decision-lineage-workflow.md)
- Codex runtime startup guide: [docs/engineering/runtime/codex-runtime-startup-guide.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-startup-guide.md)
- Codex runtime startup validation: [docs/engineering/runtime/codex-runtime-startup-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/runtime/codex-runtime-startup-validation.md)

For live OpenClaw skill installs, set `OPENPRECEDENT_HOME` to a stable shared directory so runtime brief lookups and invocation logs do not fall back to workspace-local files.

## License

Apache-2.0
