#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ -n "${OPENPRECEDENT_BIN:-}" ]]; then
  OPENPRECEDENT_BIN="$OPENPRECEDENT_BIN"
elif [[ -x "$ROOT_DIR/.venv/bin/openprecedent" ]]; then
  OPENPRECEDENT_BIN="$ROOT_DIR/.venv/bin/openprecedent"
else
  OPENPRECEDENT_BIN="openprecedent"
fi

LIVE_ROOT="${OPENPRECEDENT_LIVE_ROOT:-/tmp/openprecedent-openclaw-live}"
PROFILE="${OPENPRECEDENT_LIVE_PROFILE:-opv80}"
RUNTIME_HOME="${OPENPRECEDENT_LIVE_RUNTIME_HOME:-$LIVE_ROOT/runtime-home}"
OUTPUT_ROOT="$LIVE_ROOT/output"
SEED_ROOT="$LIVE_ROOT/seed-sessions"
DB_PATH="$RUNTIME_HOME/openprecedent.db"
INVOCATION_LOG="$RUNTIME_HOME/openprecedent-runtime-invocations.jsonl"
PROMPT_FILE="$LIVE_ROOT/prompt.txt"
SEED_SESSION_FILE="${OPENPRECEDENT_LIVE_SEED_SESSION_FILE:-}"
SEED_SESSION_ID="${OPENPRECEDENT_LIVE_SEED_SESSION_ID:-prior-session}"
SEED_CASE_ID="${OPENPRECEDENT_LIVE_SEED_CASE_ID:-case_openclaw_live_prior}"
SEED_MARKER="$LIVE_ROOT/.seeded"
RESET="${OPENPRECEDENT_LIVE_RESET:-0}"
GATEWAY_PORT="${OPENPRECEDENT_LIVE_GATEWAY_PORT:-}"
DEFAULT_PROMPT="Do not edit code. Provide a short written recommendation only for improving repository navigation, and keep it consistent with earlier repository decisions if relevant."
PROMPT_TEXT="${OPENPRECEDENT_LIVE_PROMPT:-$DEFAULT_PROMPT}"

if [[ "$RESET" == "1" ]]; then
  rm -rf "$LIVE_ROOT"
fi

mkdir -p "$RUNTIME_HOME" "$OUTPUT_ROOT" "$SEED_ROOT"

if [[ ! -f "$PROMPT_FILE" ]]; then
  printf '%s\n' "$PROMPT_TEXT" > "$PROMPT_FILE"
fi

run_openprecedent() {
  OPENPRECEDENT_HOME="$RUNTIME_HOME" \
  "$OPENPRECEDENT_BIN" "$@"
}

seed_prior_history() {
  [[ -n "$SEED_SESSION_FILE" ]] || return 0

  if [[ -f "$SEED_MARKER" ]]; then
    echo "Seed prior history already initialized; preserving existing runtime home."
    return 0
  fi

  local seed_basename seed_target sessions_index
  seed_basename="$(basename "$SEED_SESSION_FILE")"
  seed_target="$SEED_ROOT/$seed_basename"
  sessions_index="$SEED_ROOT/sessions.json"

  cp "$SEED_SESSION_FILE" "$seed_target"
  cat >"$sessions_index" <<EOF
[
  {
    "key": "agent:${PROFILE}:seed:${SEED_SESSION_ID}",
    "label": "Seed session: ${SEED_SESSION_ID}",
    "displayName": "Seed session: ${SEED_SESSION_ID}",
    "updatedAt": 1773018022842,
    "sessionId": "${SEED_SESSION_ID}",
    "model": "gpt-5.3-codex",
    "sessionFile": "$seed_target",
    "isActive": false
  }
]
EOF

  run_openprecedent runtime import-openclaw-session \
    --session-id "$SEED_SESSION_ID" \
    --sessions-root "$SEED_ROOT" \
    --case-id "$SEED_CASE_ID" \
    > "$OUTPUT_ROOT/01-seed-import.json"

  run_openprecedent extract decisions "$SEED_CASE_ID" \
    > "$OUTPUT_ROOT/02-seed-extract.json"

  : > "$SEED_MARKER"
}

write_gateway_launcher() {
  local gateway_cmd
  gateway_cmd="OPENPRECEDENT_HOME=\"$RUNTIME_HOME\" openclaw --profile \"$PROFILE\" gateway"
  if [[ -n "$GATEWAY_PORT" ]]; then
    gateway_cmd="${gateway_cmd}  # gateway port should be configured in the ${PROFILE} profile: ${GATEWAY_PORT}"
  fi

  cat >"$LIVE_ROOT/launch-openclaw-gateway.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail

$gateway_cmd
EOF
  chmod +x "$LIVE_ROOT/launch-openclaw-gateway.sh"
}

write_next_steps() {
  cat >"$LIVE_ROOT/next-steps.txt" <<EOF
Live OpenClaw validation workspace: $LIVE_ROOT

1. Start the isolated gateway:
   ./launch-openclaw-gateway.sh

2. Run a live OpenClaw turn using the prompt in:
   $PROMPT_FILE

3. Re-run this harness after the turn to refresh the invocation summary:
   ./scripts/run-openclaw-live-validation.sh

4. Inspect the artifacts under:
   $OUTPUT_ROOT
EOF
}

write_manifest() {
  python3 - "$OUTPUT_ROOT/manifest.json" <<'PY'
import json
import os
import sys

output_path = sys.argv[1]
manifest = {
    "profile": os.environ["PROFILE"],
    "live_root": os.environ["LIVE_ROOT"],
    "runtime_home": os.environ["RUNTIME_HOME"],
    "db_path": os.environ["DB_PATH"],
    "invocation_log": os.environ["INVOCATION_LOG"],
    "prompt_file": os.environ["PROMPT_FILE"],
    "seed_session_file": os.environ.get("SEED_SESSION_FILE") or None,
    "seed_session_id": os.environ["SEED_SESSION_ID"],
    "seed_case_id": os.environ["SEED_CASE_ID"],
}
# keep the launcher command inspectable without trying to shell-escape here
manifest["gateway_launcher"] = os.path.join(os.environ["LIVE_ROOT"], "launch-openclaw-gateway.sh")
with open(output_path, "w", encoding="utf-8") as handle:
    json.dump(manifest, handle, ensure_ascii=True, indent=2, sort_keys=True)
    handle.write("\n")
PY
}

write_invocation_summary() {
  python3 - "$INVOCATION_LOG" "$OUTPUT_ROOT/03-invocation-summary.json" <<'PY'
import json
import os
import sys
from pathlib import Path

log_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
records = []
if log_path.exists():
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        records.append(json.loads(line))

summary = {
    "invocation_log": str(log_path),
    "invocation_count": len(records),
    "latest_invocation_id": None,
    "latest_recorded_at": None,
    "latest_query_reason": None,
    "latest_matched_case_ids": [],
    "latest_task_summary": None,
}
if records:
    latest = records[-1]
    summary.update(
        {
            "latest_invocation_id": latest.get("invocation_id"),
            "latest_recorded_at": latest.get("recorded_at"),
            "latest_query_reason": latest.get("query_reason"),
            "latest_matched_case_ids": latest.get("matched_case_ids", []),
            "latest_task_summary": latest.get("task_summary"),
        }
    )

with output_path.open("w", encoding="utf-8") as handle:
    json.dump(summary, handle, ensure_ascii=True, indent=2, sort_keys=True)
    handle.write("\n")
PY
}

export PROFILE LIVE_ROOT RUNTIME_HOME DB_PATH INVOCATION_LOG PROMPT_FILE
export SEED_SESSION_FILE SEED_SESSION_ID SEED_CASE_ID

seed_prior_history
write_gateway_launcher
write_next_steps
write_manifest
write_invocation_summary

echo "OpenClaw live validation harness prepared."
echo "Workspace: $LIVE_ROOT"
echo "Prompt: $PROMPT_FILE"
echo "Launcher: $LIVE_ROOT/launch-openclaw-gateway.sh"
echo "Artifacts:"
echo "  $OUTPUT_ROOT/manifest.json"
if [[ -f "$OUTPUT_ROOT/01-seed-import.json" ]]; then
  echo "  $OUTPUT_ROOT/01-seed-import.json"
fi
if [[ -f "$OUTPUT_ROOT/02-seed-extract.json" ]]; then
  echo "  $OUTPUT_ROOT/02-seed-extract.json"
fi
echo "  $OUTPUT_ROOT/03-invocation-summary.json"
