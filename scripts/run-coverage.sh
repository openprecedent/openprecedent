#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

COVERAGE_DIR="${OPENPRECEDENT_COVERAGE_DIR:-$ROOT_DIR/coverage}"
PYTHON_BIN="${OPENPRECEDENT_PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python3"
fi

if ! command -v cargo >/dev/null 2>&1; then
  echo "Rust coverage failed: cargo is unavailable." >&2
  exit 1
fi

if ! command -v cargo-llvm-cov >/dev/null 2>&1 && ! cargo llvm-cov --version >/dev/null 2>&1; then
  echo "Rust coverage failed: cargo-llvm-cov is unavailable." >&2
  exit 1
fi

rm -rf "$COVERAGE_DIR"
mkdir -p "$COVERAGE_DIR/python" "$COVERAGE_DIR/rust"

echo "Running Python coverage"
./scripts/run-pytest.sh \
  --cov=src/openprecedent \
  --cov-report=term \
  --cov-report="json:$COVERAGE_DIR/python/coverage.json" \
  --cov-report="xml:$COVERAGE_DIR/python/coverage.xml" \
  --cov-report="html:$COVERAGE_DIR/python/html"

echo "Running Rust coverage"
cargo llvm-cov clean --workspace
cargo llvm-cov --workspace --all-features --no-report
cargo llvm-cov report --json --summary-only --output-path "$COVERAGE_DIR/rust/coverage-summary.json"
cargo llvm-cov report --lcov --output-path "$COVERAGE_DIR/rust/lcov.info"
cargo llvm-cov report --html --output-dir "$COVERAGE_DIR/rust"

echo "Rendering coverage summary"
"$PYTHON_BIN" scripts/render_coverage_summary.py \
  "$COVERAGE_DIR/python/coverage.json" \
  "$COVERAGE_DIR/rust/coverage-summary.json" \
  > "$COVERAGE_DIR/coverage-summary.md"
