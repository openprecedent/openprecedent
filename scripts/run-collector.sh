#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT_DIR/scripts/lib/openprecedent-rust-cli.sh"

OPENPRECEDENT_BIN="$(resolve_openprecedent_rust_cli "$ROOT_DIR")"
OPENPRECEDENT_DB="${OPENPRECEDENT_DB:-$ROOT_DIR/runtime/openprecedent.db}"
OPENPRECEDENT_COLLECTOR_STATE="${OPENPRECEDENT_COLLECTOR_STATE:-$ROOT_DIR/runtime/openprecedent-collector-state.json}"
OPENCLAW_SESSIONS_ROOT="${OPENCLAW_SESSIONS_ROOT:-$HOME/.openclaw/agents/main/sessions}"
OPENPRECEDENT_COLLECT_LIMIT="${OPENPRECEDENT_COLLECT_LIMIT:-1}"
OPENPRECEDENT_AGENT_ID="${OPENPRECEDENT_AGENT_ID:-openclaw}"

mkdir -p "$(dirname "$OPENPRECEDENT_DB")"
mkdir -p "$(dirname "$OPENPRECEDENT_COLLECTOR_STATE")"

export OPENPRECEDENT_DB
export OPENPRECEDENT_COLLECTOR_STATE

exec "$OPENPRECEDENT_BIN" \
  --db "$OPENPRECEDENT_DB" \
  --state-file "$OPENPRECEDENT_COLLECTOR_STATE" \
  --format json \
  capture openclaw collect-sessions \
  --sessions-root "$OPENCLAW_SESSIONS_ROOT" \
  --limit "$OPENPRECEDENT_COLLECT_LIMIT" \
  --agent-id "$OPENPRECEDENT_AGENT_ID"
