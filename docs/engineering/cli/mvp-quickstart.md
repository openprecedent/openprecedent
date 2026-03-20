# OpenPrecedent 0.1.0 MVP Quickstart

## Goal

This quickstart is the shortest supported path for trying the OpenPrecedent `0.1.0` MVP release in a new local project.

It assumes:

- you have a checkout of this repository
- Rust and Cargo are installed
- you want to prove the MVP loop on a local machine before reading the deeper usage docs

If you want the release boundary first, see:

- [mvp-release-scope.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-scope.md)

If you want the longer usage guide after this quickstart works, see:

- [using-openprecedent.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/using-openprecedent.md)

## Install The CLI

From the repository root, install the Rust CLI into Cargo's local bin directory:

```bash
cargo install --path rust/openprecedent-cli --locked
export PATH="$HOME/.cargo/bin:$PATH"
```

After that, confirm the public command is available:

```bash
command -v openprecedent
openprecedent version
```

You should see:

```text
openprecedent 0.1.0 (mvp)
```

If you prefer not to install globally yet, you can also run the binary directly from the repository:

```bash
cargo run -q -p openprecedent-cli -- version
```

If another older `openprecedent` binary already exists on your machine, keeping `$HOME/.cargo/bin` ahead of it in `PATH` avoids accidentally running the stale install.

## Create An Isolated Runtime Home

Use a dedicated runtime directory so the quickstart does not mix with other local experiments:

```bash
export OPENPRECEDENT_HOME="$(pwd)/.openprecedent-mvp-quickstart"
mkdir -p "$OPENPRECEDENT_HOME"
```

With that one variable set, the CLI will keep its SQLite database and runtime invocation log under the same local directory.

## Run The Minimal MVP Loop

### 1. Create the first case

```bash
openprecedent case create \
  --case-id case_alpha \
  --title "Alpha docs-only recommendation"
```

### 2. Append the task events

```bash
openprecedent event append case_alpha message.user user \
  --payload '{"message":"Do not edit code. Provide a short written recommendation only."}'

openprecedent event append case_alpha message.agent agent \
  --payload '{"message":"I will stay within docs-only scope and provide a short recommendation."}'

openprecedent event append case_alpha case.completed system \
  --payload '{"summary":"Delivered a short written recommendation."}'
```

### 3. Extract decisions

```bash
openprecedent decision extract case_alpha
```

### 4. Replay the case

```bash
openprecedent replay case case_alpha
```

### 5. Add a second similar case so precedent retrieval has something to compare

```bash
openprecedent case create \
  --case-id case_beta \
  --title "Beta docs-only recommendation"

openprecedent event append case_beta message.user user \
  --payload '{"message":"Give me a short recommendation without editing code."}'

openprecedent event append case_beta message.agent agent \
  --payload '{"message":"I will provide a docs-only recommendation and avoid code changes."}'

openprecedent event append case_beta case.completed system \
  --payload '{"summary":"Second recommendation delivered."}'

openprecedent decision extract case_beta
```

### 6. Retrieve precedent

```bash
openprecedent precedent find case_alpha --limit 3
```

At this point you have exercised the full MVP loop:

1. capture a case
2. store ordered events
3. extract decisions
4. replay a case
5. retrieve similar precedent

## Next Practical Steps

After the minimal loop works, choose the next path that matches your use case:

- For deeper CLI usage and OpenClaw import flows:
  - [using-openprecedent.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/using-openprecedent.md)
- For the strongest currently supported real-history workflow:
  - OpenClaw import and collection in [using-openprecedent.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/using-openprecedent.md)
- For runtime decision-lineage validation context:
  - [openclaw-runtime-decision-lineage-validation.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/validation/openclaw-runtime-decision-lineage-validation.md)

## What This Quickstart Deliberately Does Not Cover

This page does not try to teach:

- repository-local PM tooling
- live OpenClaw validation harness setup
- HarnessHub private skill installation
- post-MVP research workflows

Those are real repository capabilities, but they are not part of the shortest new-project MVP path.
