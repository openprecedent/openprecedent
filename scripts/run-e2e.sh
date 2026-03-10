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

E2E_ROOT="${OPENPRECEDENT_E2E_ROOT:-/tmp/openprecedent-openclaw-journey}"
FIXTURE_ROOT="${OPENPRECEDENT_E2E_FIXTURE_ROOT:-$ROOT_DIR/tests/fixtures/openclaw_sessions}"
SESSIONS_ROOT="$E2E_ROOT/sessions"
OUTPUT_ROOT="$E2E_ROOT/output"
DB_PATH="$E2E_ROOT/openprecedent.db"
STATE_PATH="$E2E_ROOT/collector-state.json"
EVAL_DB_PATH="$E2E_ROOT/eval-fixtures.db"

mkdir -p "$SESSIONS_ROOT" "$OUTPUT_ROOT"
rm -f "$DB_PATH" "$STATE_PATH" "$EVAL_DB_PATH"
rm -f "$OUTPUT_ROOT"/*.json

cp "$FIXTURE_ROOT/file-ops-session.jsonl" "$SESSIONS_ROOT/"
cp "$FIXTURE_ROOT/search-read-session.jsonl" "$SESSIONS_ROOT/"
cp "$FIXTURE_ROOT/sample-session.jsonl" "$SESSIONS_ROOT/"

cat > "$SESSIONS_ROOT/sessions.json" <<EOF
[
  {
    "key": "agent:main:user:file-ops",
    "label": "User session: file ops fixture",
    "displayName": "User session: file ops fixture",
    "updatedAt": 1773018022842,
    "sessionId": "file-ops-session",
    "model": "gpt-5.3-codex",
    "sessionFile": "$SESSIONS_ROOT/file-ops-session.jsonl",
    "isActive": false
  },
  {
    "key": "agent:main:user:search-read",
    "label": "User session: search roadmap docs",
    "displayName": "User session: search roadmap docs",
    "updatedAt": 1773018022841,
    "sessionId": "search-read-session",
    "model": "gpt-5.3-codex",
    "sessionFile": "$SESSIONS_ROOT/search-read-session.jsonl",
    "isActive": false
  },
  {
    "key": "agent:main:user:sample",
    "label": "User session: summarize context graph",
    "displayName": "User session: summarize context graph",
    "updatedAt": 1773018022840,
    "sessionId": "sample-session",
    "model": "gpt-5.3-codex",
    "sessionFile": "$SESSIONS_ROOT/sample-session.jsonl",
    "isActive": true
  }
]
EOF

run_openprecedent() {
  OPENPRECEDENT_DB="$DB_PATH" \
  OPENPRECEDENT_COLLECTOR_STATE="$STATE_PATH" \
  "$OPENPRECEDENT_BIN" "$@"
}

echo "Running OpenPrecedent E2E validation in $E2E_ROOT"

run_openprecedent runtime list-openclaw-sessions \
  --sessions-root "$SESSIONS_ROOT" \
  > "$OUTPUT_ROOT/01-list-openclaw-sessions.json"

run_openprecedent runtime collect-openclaw-sessions \
  --sessions-root "$SESSIONS_ROOT" \
  --limit 1 \
  > "$OUTPUT_ROOT/02-collect-openclaw-sessions.json"

run_openprecedent runtime import-openclaw-session \
  --session-id search-read-session \
  --sessions-root "$SESSIONS_ROOT" \
  --case-id case_openclaw_search_read \
  > "$OUTPUT_ROOT/03-import-search-read-session.json"

run_openprecedent runtime import-openclaw-session \
  --session-id sample-session \
  --sessions-root "$SESSIONS_ROOT" \
  --case-id case_openclaw_sample \
  > "$OUTPUT_ROOT/04-import-sample-session.json"

run_openprecedent extract decisions openclaw_fileopssession \
  > "$OUTPUT_ROOT/05-extract-decisions-file-ops.json"

run_openprecedent extract decisions case_openclaw_search_read \
  > "$OUTPUT_ROOT/06-extract-decisions-search-read.json"

run_openprecedent extract decisions case_openclaw_sample \
  > "$OUTPUT_ROOT/07-extract-decisions-sample.json"

run_openprecedent replay case case_openclaw_search_read --json \
  > "$OUTPUT_ROOT/08-replay-search-read.json"

run_openprecedent precedent find case_openclaw_search_read --limit 3 \
  > "$OUTPUT_ROOT/09-precedent-search-read.json"

OPENPRECEDENT_DB="$EVAL_DB_PATH" \
"$OPENPRECEDENT_BIN" eval fixtures "$ROOT_DIR/tests/fixtures/evaluation/real_session_suite.json" --json \
  > "$OUTPUT_ROOT/10-eval-fixtures.json"

run_openprecedent eval collected-openclaw-sessions \
  --sessions-root "$SESSIONS_ROOT" \
  --json \
  > "$OUTPUT_ROOT/11-eval-collected-openclaw-sessions.json"

echo "E2E validation completed."
echo "Workspace: $E2E_ROOT"
echo "Outputs:"
echo "  $OUTPUT_ROOT/01-list-openclaw-sessions.json"
echo "  $OUTPUT_ROOT/02-collect-openclaw-sessions.json"
echo "  $OUTPUT_ROOT/03-import-search-read-session.json"
echo "  $OUTPUT_ROOT/04-import-sample-session.json"
echo "  $OUTPUT_ROOT/05-extract-decisions-file-ops.json"
echo "  $OUTPUT_ROOT/06-extract-decisions-search-read.json"
echo "  $OUTPUT_ROOT/07-extract-decisions-sample.json"
echo "  $OUTPUT_ROOT/08-replay-search-read.json"
echo "  $OUTPUT_ROOT/09-precedent-search-read.json"
echo "  $OUTPUT_ROOT/10-eval-fixtures.json"
echo "  $OUTPUT_ROOT/11-eval-collected-openclaw-sessions.json"
