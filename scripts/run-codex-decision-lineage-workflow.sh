#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

PYTHON_BIN="${OPENPRECEDENT_PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python3"
fi

if [[ -z "${OPENPRECEDENT_HOME:-}" ]]; then
  export OPENPRECEDENT_HOME="$HOME/.openprecedent/runtime"
fi

run_openprecedent_cli() {
  "$PYTHON_BIN" -c 'from openprecedent.cli import run; run()' "$@"
}

INSPECT_LATEST=0
ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --inspect-latest)
      INSPECT_LATEST=1
      shift
      ;;
    *)
      ARGS+=("$1")
      shift
      ;;
  esac
done

run_openprecedent_cli runtime decision-lineage-brief "${ARGS[@]}"

if [[ "$INSPECT_LATEST" != "1" ]]; then
  exit 0
fi

LOG_FILE="${OPENPRECEDENT_RUNTIME_INVOCATION_LOG:-$OPENPRECEDENT_HOME/openprecedent-runtime-invocations.jsonl}"
if [[ ! -f "$LOG_FILE" ]]; then
  echo "No runtime invocation log found at $LOG_FILE" >&2
  exit 1
fi

INVOCATION_ID="$(
  "$PYTHON_BIN" - "$LOG_FILE" <<'PY'
import json
import sys
from pathlib import Path

log_path = Path(sys.argv[1])
last_id = None
for line in log_path.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    item = json.loads(line)
    last_id = item.get("invocation_id")
if not last_id:
    raise SystemExit(1)
print(last_id)
PY
)"

run_openprecedent_cli runtime inspect-decision-lineage-invocation \
  --invocation-id "$INVOCATION_ID" \
  --log-file "$LOG_FILE"
