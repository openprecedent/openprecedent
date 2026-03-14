#!/usr/bin/env bash
set -euo pipefail

# Internal-only repository helper.
# This harness wraps the Rust CLI for repo-local validation and is not the public product interface.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

source "$ROOT_DIR/scripts/lib/openprecedent-rust-cli.sh"

OPENPRECEDENT_BIN="$(resolve_openprecedent_rust_cli "$ROOT_DIR")"

LIVE_ROOT="${OPENPRECEDENT_CODEX_LIVE_ROOT:-/tmp/openprecedent-codex-live}"
RUNTIME_HOME="${OPENPRECEDENT_CODEX_LIVE_RUNTIME_HOME:-$LIVE_ROOT/runtime-home}"
OUTPUT_ROOT="$LIVE_ROOT/output"
PROMPTS_ROOT="$LIVE_ROOT/prompts"
RESET="${OPENPRECEDENT_CODEX_LIVE_RESET:-0}"
AUTO_RUN="${OPENPRECEDENT_CODEX_LIVE_AUTO_RUN:-0}"

SEED_CURRENT_FIXTURE="${OPENPRECEDENT_CODEX_LIVE_SEED_CURRENT_FIXTURE:-$ROOT_DIR/tests/fixtures/codex_rollout_precedent_current.jsonl}"
SEED_SEMANTIC_FIXTURE="${OPENPRECEDENT_CODEX_LIVE_SEED_SEMANTIC_FIXTURE:-$ROOT_DIR/tests/fixtures/codex_rollout_precedent_semantic_match.jsonl}"
SEED_OPERATIONAL_FIXTURE="${OPENPRECEDENT_CODEX_LIVE_SEED_OPERATIONAL_FIXTURE:-$ROOT_DIR/tests/fixtures/codex_rollout_precedent_operational_overlap.jsonl}"

if [[ "$RESET" == "1" ]]; then
  rm -rf "$LIVE_ROOT"
fi

mkdir -p "$RUNTIME_HOME" "$OUTPUT_ROOT" "$PROMPTS_ROOT"

run_openprecedent() {
  "$OPENPRECEDENT_BIN" --home "$RUNTIME_HOME" --format json "$@"
}

write_prompt_files() {
  cat >"$PROMPTS_ROOT/01-initial-planning.txt" <<'EOF'
Use prior Codex lineage before planning.
Stay within docs-only scope and provide a short written recommendation.
EOF

  cat >"$PROMPTS_ROOT/02-before-file-write.txt" <<'EOF'
Before writing a file, check whether prior Codex lineage narrows the scope or confirms approval.
Use this before any risky file write.
EOF

  cat >"$PROMPTS_ROOT/03-after-failure.txt" <<'EOF'
After a directional failure, request prior Codex lineage to recover without widening scope.
Do not use this for transient command noise.
EOF
}

seed_history() {
  run_openprecedent capture codex import-rollout \
    "$SEED_CURRENT_FIXTURE" \
    --case-id case_codex_live_current \
    --title "Codex live seed current" \
    >"$OUTPUT_ROOT/01-seed-current.json"
  run_openprecedent decision extract case_codex_live_current \
    >"$OUTPUT_ROOT/02-seed-current-decisions.json"

  run_openprecedent capture codex import-rollout \
    "$SEED_SEMANTIC_FIXTURE" \
    --case-id case_codex_live_semantic \
    --title "Codex live seed semantic" \
    >"$OUTPUT_ROOT/03-seed-semantic.json"
  run_openprecedent decision extract case_codex_live_semantic \
    >"$OUTPUT_ROOT/04-seed-semantic-decisions.json"

  run_openprecedent capture codex import-rollout \
    "$SEED_OPERATIONAL_FIXTURE" \
    --case-id case_codex_live_operational \
    --title "Codex live seed operational" \
    >"$OUTPUT_ROOT/05-seed-operational.json"
  run_openprecedent decision extract case_codex_live_operational \
    >"$OUTPUT_ROOT/06-seed-operational-decisions.json"
}

run_validation_rounds() {
  run_openprecedent lineage brief \
    --query-reason initial_planning \
    --task-summary "Do not edit code. Provide a short written recommendation only and keep it consistent with earlier Codex runtime decisions." \
    >"$OUTPUT_ROOT/10-initial-planning-brief.json"

  run_openprecedent lineage brief \
    --query-reason before_file_write \
    --task-summary "Stay within docs-only scope. Before writing README.md, confirm whether prior Codex lineage narrows the allowed change." \
    --current-plan "Draft a short docs-only recommendation before any edits." \
    --candidate-action "Edit README.md" \
    >"$OUTPUT_ROOT/11-before-file-write-brief.json"

  run_openprecedent lineage brief \
    --query-reason after_failure \
    --task-summary "A broader implementation path was rejected. Recover with prior Codex lineage and stay within docs-only scope." \
    --current-plan "Recover from a broader path by narrowing back to documentation guidance." \
    --candidate-action "Retry broad implementation changes" \
    >"$OUTPUT_ROOT/12-after-failure-brief.json"
}

write_manifest() {
  python3 - "$OUTPUT_ROOT/manifest.json" <<'PY'
import json
import os
import sys

manifest = {
    "live_root": os.environ["LIVE_ROOT"],
    "runtime_home": os.environ["RUNTIME_HOME"],
    "output_root": os.environ["OUTPUT_ROOT"],
    "prompts_root": os.environ["PROMPTS_ROOT"],
    "auto_run": os.environ["AUTO_RUN"] == "1",
}
with open(sys.argv[1], "w", encoding="utf-8") as handle:
    json.dump(manifest, handle, ensure_ascii=True, indent=2, sort_keys=True)
    handle.write("\n")
PY
}

write_invocation_artifacts() {
  run_openprecedent lineage invocation list \
    >"$OUTPUT_ROOT/20-invocation-list.json"

  python3 - "$OUTPUT_ROOT/20-invocation-list.json" "$OUTPUT_ROOT/21-latest-invocation-summary.json" <<'PY'
import json
import sys
from pathlib import Path

items = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
summary = {
    "invocation_count": len(items),
    "latest_invocation_id": None,
    "latest_query_reason": None,
    "latest_matched_case_ids": [],
    "latest_task_summary": None,
}
if items:
    latest = items[-1]
    summary.update(
        {
            "latest_invocation_id": latest.get("invocation_id"),
            "latest_query_reason": latest.get("query_reason"),
            "latest_matched_case_ids": latest.get("matched_case_ids", []),
            "latest_task_summary": latest.get("task_summary"),
        }
    )

Path(sys.argv[2]).write_text(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

  python3 - "$OUTPUT_ROOT/20-invocation-list.json" <<'PY' >"$OUTPUT_ROOT/.latest-invocation-id"
import json
import sys
from pathlib import Path

items = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if items:
    print(items[-1]["invocation_id"])
PY

  if [[ -s "$OUTPUT_ROOT/.latest-invocation-id" ]]; then
    run_openprecedent lineage invocation inspect \
      --invocation-id "$(cat "$OUTPUT_ROOT/.latest-invocation-id")" \
      >"$OUTPUT_ROOT/22-latest-invocation-inspection.json"
  fi
  rm -f "$OUTPUT_ROOT/.latest-invocation-id"
}

write_next_steps() {
  cat >"$LIVE_ROOT/next-steps.txt" <<EOF
Codex live validation workspace: $LIVE_ROOT

1. Export the shared runtime home:
   export OPENPRECEDENT_HOME="$RUNTIME_HOME"

2. Read the round prompts under:
   $PROMPTS_ROOT

3. During real Codex work, call:
   openprecedent --home "$RUNTIME_HOME" --format json lineage brief --query-reason <reason> --task-summary "<summary>"

4. Re-run this harness with OPENPRECEDENT_CODEX_LIVE_AUTO_RUN=0 to refresh the invocation artifacts:
   ./scripts/run-codex-live-validation.sh

5. Inspect:
   $OUTPUT_ROOT/20-invocation-list.json
   $OUTPUT_ROOT/21-latest-invocation-summary.json
   $OUTPUT_ROOT/22-latest-invocation-inspection.json
EOF
}

export LIVE_ROOT RUNTIME_HOME OUTPUT_ROOT PROMPTS_ROOT AUTO_RUN

write_prompt_files
seed_history
if [[ "$AUTO_RUN" == "1" ]]; then
  run_validation_rounds
fi
write_manifest
write_invocation_artifacts
write_next_steps

echo "Codex live validation workspace prepared."
echo "Workspace: $LIVE_ROOT"
echo "Artifacts:"
echo "  $OUTPUT_ROOT/manifest.json"
echo "  $OUTPUT_ROOT/20-invocation-list.json"
echo "  $OUTPUT_ROOT/21-latest-invocation-summary.json"
if [[ -f "$OUTPUT_ROOT/22-latest-invocation-inspection.json" ]]; then
  echo "  $OUTPUT_ROOT/22-latest-invocation-inspection.json"
fi
