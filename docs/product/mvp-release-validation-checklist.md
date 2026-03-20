# OpenPrecedent 0.1.0 MVP Release Validation Checklist

## Purpose

This checklist defines the minimum release-blocking validation that must pass before publishing the OpenPrecedent `0.1.0` MVP release.

It exists to make MVP publication auditable and repeatable. A release is not ready because the repository mostly looks healthy; it is ready only when the checks below have passed against the shipped Rust CLI and the current local-first MVP scope.

For the release scope and positioning that this checklist protects, see:

- [mvp-release-scope.md](/workspace/02-projects/incubation/openprecedent/docs/product/mvp-release-scope.md)

For the shortest new-project path that should remain consistent with this checklist, see:

- [mvp-quickstart.md](/workspace/02-projects/incubation/openprecedent/docs/engineering/cli/mvp-quickstart.md)

## Release-Blocking Checks

All items in this section are release blockers.

### 1. Repository preflight

Run:

```bash
OPENPRECEDENT_PYTHON_BIN=/workspace/02-projects/incubation/openprecedent/.venv/bin/python \
  ./scripts/run-agent-preflight.sh
```

This is the standard repository-local release gate and must pass cleanly.

### 2. Scoped MVP coverage gate

Run:

```bash
./scripts/run-coverage.sh
python3 scripts/check_mvp_coverage_gate.py \
  coverage/python/coverage.json \
  coverage/rust/coverage-summary.json
```

Pass criteria:

- Python scoped MVP release surface is at least `90%`
- Rust scoped MVP release implementation core is at least `90%`

This gate measures the release-facing MVP baseline, not every repository-local support surface.

### 3. Rust CLI smoke check

Confirm the public CLI resolves and reports the published MVP version:

```bash
cargo install --path rust/openprecedent-cli --locked
export PATH="$HOME/.cargo/bin:$PATH"
command -v openprecedent
openprecedent version
```

Pass criteria:

- `command -v openprecedent` resolves to the expected Cargo-installed binary
- `openprecedent version` reports `openprecedent 0.1.0 (mvp)`

### 4. Minimal end-to-end MVP loop

From a clean temporary directory, validate the documented quickstart path:

```bash
export OPENPRECEDENT_HOME="$(pwd)/.openprecedent-mvp-release-check"

openprecedent case create --case-id case_alpha --title "Alpha MVP release check"
openprecedent event append case_alpha message.user user --payload '{"message":"Give a short docs-only recommendation."}'
openprecedent event append case_alpha message.agent agent --payload '{"message":"I will stay docs-only."}'
openprecedent event append case_alpha case.completed system --payload '{"summary":"Delivered the recommendation."}'
openprecedent decision extract case_alpha
openprecedent replay case case_alpha

openprecedent case create --case-id case_beta --title "Beta MVP release check"
openprecedent event append case_beta message.user user --payload '{"message":"Provide a docs-only recommendation."}'
openprecedent event append case_beta message.agent agent --payload '{"message":"I will avoid code changes and provide a recommendation."}'
openprecedent event append case_beta case.completed system --payload '{"summary":"Delivered the second recommendation."}'
openprecedent decision extract case_beta
openprecedent precedent find case_alpha --limit 3
```

Pass criteria:

- case creation succeeds
- event append succeeds
- decision extraction succeeds
- replay succeeds
- precedent retrieval succeeds against at least one second case

## Non-Blocking Observations

These checks are useful release-notes inputs, but they are not blockers for the `0.1.0` MVP publication:

- ongoing post-MVP research issue progress
- HarnessHub private-skill research paths
- future memory-quality and retrieval-hygiene studies

Those remain important, but they belong to post-release research rather than MVP publication readiness.

## Release Record Expectations

When this checklist is run for publication, the release record should capture:

- the commit or tag being validated
- whether each blocking check passed
- links to CI artifacts where applicable
- any known non-blocking caveats carried into release notes
