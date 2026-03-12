#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ -n "${OPENPRECEDENT_BIN:-}" ]]; then
  OPENPRECEDENT_BIN="$OPENPRECEDENT_BIN"
elif [[ -x "$ROOT_DIR/.venv/bin/openprecedent" ]]; then
  OPENPRECEDENT_BIN="$ROOT_DIR/.venv/bin/openprecedent"
elif [[ -x "$ROOT_DIR/../openprecedent/.venv/bin/openprecedent" ]]; then
  OPENPRECEDENT_BIN="$ROOT_DIR/../openprecedent/.venv/bin/openprecedent"
else
  OPENPRECEDENT_BIN="openprecedent"
fi

if [[ -n "${OPENPRECEDENT_PYTHON_BIN:-}" ]]; then
  PYTHON_BIN="$OPENPRECEDENT_PYTHON_BIN"
elif [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
elif [[ -x "$ROOT_DIR/../openprecedent/.venv/bin/python" ]]; then
  PYTHON_BIN="$ROOT_DIR/../openprecedent/.venv/bin/python"
else
  PYTHON_BIN="python3"
fi

LIVE_ROOT="${OPENPRECEDENT_HARNESSHUB_MATCH_ROOT:-/tmp/openprecedent-harnesshub-match}"
RUNTIME_HOME="${OPENPRECEDENT_HARNESSHUB_MATCH_RUNTIME_HOME:-$LIVE_ROOT/runtime-home}"
OUTPUT_ROOT="$LIVE_ROOT/output"
RESET="${OPENPRECEDENT_HARNESSHUB_MATCH_RESET:-0}"
BUNDLE_DIR="${OPENPRECEDENT_HARNESSHUB_BUNDLE_DIR:-$ROOT_DIR/research-artifacts/harnesshub-rounds/issue-53-refine-verification-into-explicit-readiness-clas-2026-03-12T082148Z}"
QUERY_REASON="${OPENPRECEDENT_HARNESSHUB_QUERY_REASON:-before_file_write}"
TASK_SUMMARY="${OPENPRECEDENT_HARNESSHUB_TASK_SUMMARY:-HarnessHub later task: refine verify output so imported images report explicit readiness classes instead of a binary runtimeReady signal.}"
CURRENT_PLAN="${OPENPRECEDENT_HARNESSHUB_CURRENT_PLAN:-Keep the verification scope narrow and map current runtime-readiness issues into explicit readiness classes for operators.}"
CANDIDATE_ACTION="${OPENPRECEDENT_HARNESSHUB_CANDIDATE_ACTION:-Update verification output and tests to describe explicit readiness classes.}"
KNOWN_FILES="${OPENPRECEDENT_HARNESSHUB_KNOWN_FILES:-HarnessHub/src/core/verifier.ts,HarnessHub/test/e2e.test.ts}"

if [[ "$RESET" == "1" ]]; then
  rm -rf "$LIVE_ROOT"
fi

mkdir -p "$RUNTIME_HOME" "$OUTPUT_ROOT"
export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
export LIVE_ROOT RUNTIME_HOME OUTPUT_ROOT BUNDLE_DIR

IFS=',' read -r -a KNOWN_FILE_ARGS <<<"$KNOWN_FILES"

run_openprecedent() {
  OPENPRECEDENT_HOME="$RUNTIME_HOME" "$OPENPRECEDENT_BIN" "$@"
}

run_workflow() {
  OPENPRECEDENT_HOME="$RUNTIME_HOME" \
  OPENPRECEDENT_PYTHON_BIN="$PYTHON_BIN" \
  ./scripts/run-codex-decision-lineage-workflow.sh "$@"
}

"$PYTHON_BIN" scripts/import_harnesshub_codex_round.py \
  --bundle-dir "$BUNDLE_DIR" \
  --runtime-home "$RUNTIME_HOME" \
  --python-bin "$PYTHON_BIN" \
  --skip-if-case-exists \
  >"$OUTPUT_ROOT/01-import-summary.json"

WORKFLOW_ARGS=(
  --query-reason "$QUERY_REASON"
  --task-summary "$TASK_SUMMARY"
  --current-plan "$CURRENT_PLAN"
  --candidate-action "$CANDIDATE_ACTION"
)

for file in "${KNOWN_FILE_ARGS[@]}"; do
  if [[ -n "$file" ]]; then
    WORKFLOW_ARGS+=(--known-file "$file")
  fi
done

run_workflow "${WORKFLOW_ARGS[@]}" >"$OUTPUT_ROOT/10-brief.json"
run_openprecedent runtime list-decision-lineage-invocations >"$OUTPUT_ROOT/20-invocation-list.json"

"$PYTHON_BIN" - "$BUNDLE_DIR/round-manifest.json" "$OUTPUT_ROOT/20-invocation-list.json" "$OUTPUT_ROOT/21-latest-invocation-summary.json" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
invocations = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
latest = invocations[-1] if invocations else {}
summary = {
    "bundle_case_id": manifest["case_id"],
    "invocation_count": len(invocations),
    "latest_invocation_id": latest.get("invocation_id"),
    "latest_query_reason": latest.get("query_reason"),
    "latest_matched_case_ids": latest.get("matched_case_ids", []),
    "latest_task_summary": latest.get("task_summary"),
}
Path(sys.argv[3]).write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

"$PYTHON_BIN" - "$OUTPUT_ROOT/20-invocation-list.json" <<'PY' >"$OUTPUT_ROOT/.latest-invocation-id"
import json
import sys
from pathlib import Path

items = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if items:
    print(items[-1]["invocation_id"])
PY

if [[ -s "$OUTPUT_ROOT/.latest-invocation-id" ]]; then
  run_openprecedent runtime inspect-decision-lineage-invocation \
    --invocation-id "$(cat "$OUTPUT_ROOT/.latest-invocation-id")" \
    >"$OUTPUT_ROOT/22-latest-invocation-inspection.json"
fi
rm -f "$OUTPUT_ROOT/.latest-invocation-id"

"$PYTHON_BIN" - "$BUNDLE_DIR/round-manifest.json" "$OUTPUT_ROOT/manifest.json" <<'PY'
import json
import os
import sys
from pathlib import Path

bundle_manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
manifest = {
    "live_root": os.environ["LIVE_ROOT"],
    "runtime_home": os.environ["RUNTIME_HOME"],
    "output_root": os.environ["OUTPUT_ROOT"],
    "bundle_dir": os.environ["BUNDLE_DIR"],
    "bundle_case_id": bundle_manifest["case_id"],
}
Path(sys.argv[2]).write_text(json.dumps(manifest, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

echo "HarnessHub matched-case validation workspace prepared."
echo "Workspace: $LIVE_ROOT"
echo "Artifacts:"
echo "  $OUTPUT_ROOT/manifest.json"
echo "  $OUTPUT_ROOT/01-import-summary.json"
echo "  $OUTPUT_ROOT/10-brief.json"
echo "  $OUTPUT_ROOT/20-invocation-list.json"
echo "  $OUTPUT_ROOT/21-latest-invocation-summary.json"
echo "  $OUTPUT_ROOT/22-latest-invocation-inspection.json"
