#!/usr/bin/env bash
set -euo pipefail

# Internal-only repository helper.
# The supported product surface is `openprecedent lineage ...`.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

source "$ROOT_DIR/scripts/lib/openprecedent-rust-cli.sh"

PYTHON_BIN="${OPENPRECEDENT_PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  if [[ -x "$ROOT_DIR/../openprecedent/.venv/bin/python" ]]; then
    PYTHON_BIN="$ROOT_DIR/../openprecedent/.venv/bin/python"
  else
    PYTHON_BIN="python3"
  fi
fi

OPENPRECEDENT_BIN="$(resolve_openprecedent_rust_cli "$ROOT_DIR")"

if [[ -z "${OPENPRECEDENT_HOME:-}" ]]; then
  export OPENPRECEDENT_HOME="$HOME/.openprecedent/runtime"
fi

HARNESSHUB_REPO_ROOT="${OPENPRECEDENT_HARNESSHUB_REPO_ROOT:-/workspace/02-projects/active/HarnessHub}"

"$PYTHON_BIN" ./scripts/sync_harnesshub_shared_runtime.py \
  --repo-root "$HARNESSHUB_REPO_ROOT" \
  --runtime-home "$OPENPRECEDENT_HOME" \
  --python-bin "$PYTHON_BIN" \
  --export-output-root "$OPENPRECEDENT_HOME/harnesshub-round-bundles" \
  >"${OPENPRECEDENT_HARNESSHUB_SYNC_SUMMARY_PATH:-$OPENPRECEDENT_HOME/harnesshub-sync-summary.json}"

"$OPENPRECEDENT_BIN" \
  --home "$OPENPRECEDENT_HOME" \
  --format json \
  lineage brief "$@"
