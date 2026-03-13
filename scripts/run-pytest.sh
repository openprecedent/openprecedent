#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

REPO_PYTHON_BIN="${OPENPRECEDENT_PYTHON_BIN:-}"
REPO_VENV_PYTHON="${OPENPRECEDENT_VENV_PYTHON:-$ROOT_DIR/.venv/bin/python}"
REPO_VENV_PYTEST="${OPENPRECEDENT_VENV_PYTEST:-$ROOT_DIR/.venv/bin/pytest}"
SYSTEM_PYTHON_BIN="${OPENPRECEDENT_SYSTEM_PYTHON:-python3}"
ALT_SYSTEM_PYTHON_BIN="${OPENPRECEDENT_ALT_SYSTEM_PYTHON:-python}"
SYSTEM_PYTEST_BIN="${OPENPRECEDENT_SYSTEM_PYTEST:-pytest}"

python_candidate_ready() {
  local candidate="$1"

  [[ -n "$candidate" ]] || return 1
  if [[ "$candidate" == */* ]]; then
    [[ -x "$candidate" ]] || return 1
  elif ! command -v "$candidate" >/dev/null 2>&1; then
    return 1
  fi

  "$candidate" -m pytest --version >/dev/null 2>&1
}

pytest_candidate_ready() {
  local candidate="$1"

  [[ -n "$candidate" ]] || return 1
  if [[ "$candidate" == */* ]]; then
    [[ -x "$candidate" ]] || return 1
  elif ! command -v "$candidate" >/dev/null 2>&1; then
    return 1
  fi

  "$candidate" --version >/dev/null 2>&1
}

if python_candidate_ready "$REPO_PYTHON_BIN"; then
  exec "$REPO_PYTHON_BIN" -m pytest "$@"
fi

if python_candidate_ready "$REPO_VENV_PYTHON"; then
  exec "$REPO_VENV_PYTHON" -m pytest "$@"
fi

if pytest_candidate_ready "$REPO_VENV_PYTEST"; then
  exec "$REPO_VENV_PYTEST" "$@"
fi

if python_candidate_ready "$SYSTEM_PYTHON_BIN"; then
  exec "$SYSTEM_PYTHON_BIN" -m pytest "$@"
fi

if python_candidate_ready "$ALT_SYSTEM_PYTHON_BIN"; then
  exec "$ALT_SYSTEM_PYTHON_BIN" -m pytest "$@"
fi

if pytest_candidate_ready "$SYSTEM_PYTEST_BIN"; then
  exec "$SYSTEM_PYTEST_BIN" "$@"
fi

echo "Unable to locate a usable pytest runner." >&2
echo "Tried OPENPRECEDENT_PYTHON_BIN, repository-local .venv, active Python runtimes, and bare pytest." >&2
echo "Preferred local path: ./scripts/run-pytest.sh <pytest args> or .venv/bin/python -m pytest <pytest args>." >&2
exit 1
