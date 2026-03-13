#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ "${OPENPRECEDENT_PREFLIGHT_ACTIVE:-0}" == "1" ]]; then
  echo "Agent preflight is already running; skipping recursive invocation."
  exit 0
fi
export OPENPRECEDENT_PREFLIGHT_ACTIVE=1

PYTHON_BIN="${OPENPRECEDENT_PYTHON_BIN:-$ROOT_DIR/.venv/bin/python}"
if [[ ! -x "$PYTHON_BIN" ]]; then
  PYTHON_BIN="python3"
fi

RUN_E2E="${OPENPRECEDENT_PREFLIGHT_RUN_E2E:-0}"
REVIEW_FILE="${OPENPRECEDENT_REVIEW_FILE:-$ROOT_DIR/.codex-review}"
REVIEW_PROOF_FILE="${OPENPRECEDENT_REVIEW_PROOF_FILE:-$ROOT_DIR/.codex-review-proof}"
PYTEST_ARGS="${OPENPRECEDENT_PREFLIGHT_PYTEST_ARGS:-tests --ignore=tests/test_preflight_script.py}"
BASE_REF="${OPENPRECEDENT_PREFLIGHT_BASE_REF:-upstream/main}"
ENFORCE_ISSUE_STATE="${OPENPRECEDENT_PREFLIGHT_ENFORCE_ISSUE_STATE:-0}"
FORCE_RUST_TESTS="${OPENPRECEDENT_FORCE_RUST_TESTS:-0}"
SKIP_RUST_TESTS="${OPENPRECEDENT_SKIP_RUST_TESTS:-0}"

check_review_note() {
  if [[ ! -f "$REVIEW_FILE" ]]; then
    echo "Preflight failed: missing .codex-review"
    echo "Run ./scripts/run-codex-review-checkpoint.sh, then use native Codex /review and update the note."
    exit 1
  fi

  if ! grep -Eq '^scope reviewed:' "$REVIEW_FILE" \
    || ! grep -Eq '^(findings:|no findings$)' "$REVIEW_FILE" \
    || ! grep -Eq '^remaining risks:' "$REVIEW_FILE"; then
    echo "Preflight failed: .codex-review exists but is incomplete"
    echo "Rerun ./scripts/run-codex-review-checkpoint.sh if you need a fresh template."
    exit 1
  fi

  if grep -Fq 'native /review has not been run yet' "$REVIEW_FILE"; then
    echo "Preflight failed: .codex-review still contains the checkpoint placeholder"
    echo "Run native Codex /review and replace the placeholder text with the real review result."
    exit 1
  fi
}

read_review_proof_value() {
  local key="$1"
  sed -n "s/^${key}=//p" "$REVIEW_PROOF_FILE" | head -n 1
}

check_review_proof() {
  local current_head proof_head proof_branch current_branch

  if [[ ! -f "$REVIEW_PROOF_FILE" ]]; then
    echo "Preflight failed: missing .codex-review-proof"
    echo "Run ./scripts/run-codex-review-checkpoint.sh before preflight."
    exit 1
  fi

  current_head="$(git rev-parse HEAD)"
  current_branch="$(git branch --show-current)"
  proof_head="$(read_review_proof_value head_sha)"
  proof_branch="$(read_review_proof_value branch)"

  if [[ -z "$proof_head" ]]; then
    echo "Preflight failed: .codex-review-proof is missing head_sha"
    exit 1
  fi

  if [[ "$proof_head" != "$current_head" ]]; then
    echo "Preflight failed: .codex-review-proof does not match the current HEAD"
    echo "Run ./scripts/run-codex-review-checkpoint.sh again for the current commit set."
    exit 1
  fi

  if [[ -n "$current_branch" ]] && [[ -n "$proof_branch" ]] && [[ "$proof_branch" != "$current_branch" ]]; then
    echo "Preflight failed: .codex-review-proof was generated for a different branch"
    exit 1
  fi

  if [[ "$REVIEW_FILE" -ot "$REVIEW_PROOF_FILE" ]]; then
    echo "Preflight failed: .codex-review has not been updated since the latest review checkpoint"
    echo "Update .codex-review after the native Codex /review step."
    exit 1
  fi
}

check_merged_branch_reuse() {
  local current_branch origin_url owner merged_pr_json
  current_branch="$(git branch --show-current)"
  origin_url="$(git remote get-url origin 2>/dev/null || true)"

  if [[ -z "$current_branch" ]]; then
    return 0
  fi

  if [[ "$origin_url" =~ github\.com[:/]([^/]+)/[^/]+(\.git)?$ ]]; then
    owner="${BASH_REMATCH[1]}"
  else
    return 0
  fi

  merged_pr_json="$(
    gh pr list \
      --repo openprecedent/openprecedent \
      --head "$owner:$current_branch" \
      --state merged \
      --json number,url \
      2>/dev/null || true
  )"

  if [[ "$merged_pr_json" != "[]" ]] && [[ -n "$merged_pr_json" ]]; then
    echo "Preflight failed: current branch already has a merged PR in openprecedent/openprecedent"
    exit 1
  fi
}

check_branch_freshness() {
  if [[ "${BYPASS_BRANCH_FRESHNESS_CHECK:-}" == "1" ]]; then
    echo "Bypassing branch freshness check because BYPASS_BRANCH_FRESHNESS_CHECK=1"
    return 0
  fi

  python3 "$ROOT_DIR/scripts/check_branch_freshness.py" --base-ref "$BASE_REF" --allow-missing-base-ref
}

should_run_rust_tests() {
  if [[ "$SKIP_RUST_TESTS" == "1" ]]; then
    return 1
  fi

  if [[ "$FORCE_RUST_TESTS" == "1" ]]; then
    return 0
  fi

  if ! git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
    return 1
  fi

  git diff --name-only "$BASE_REF"...HEAD | grep -Eq '^(Cargo\.toml|Cargo\.lock|rust/)'
}

run_rust_tests_if_needed() {
  if ! should_run_rust_tests; then
    echo "Skipping Rust tests: no Rust-affecting changes detected"
    return 0
  fi

  if ! command -v cargo >/dev/null 2>&1; then
    echo "Preflight failed: Rust-affecting changes detected but cargo is unavailable"
    echo "Install Rust or set OPENPRECEDENT_SKIP_RUST_TESTS=1 only if you are intentionally bypassing the local guardrail."
    exit 1
  fi

  echo "Running Rust tests"
  cargo test
}

run_markdownlint_if_available() {
  if command -v markdownlint-cli2 >/dev/null 2>&1; then
    markdownlint-cli2 "**/*.md"
    return
  fi

  if [[ -x "$ROOT_DIR/node_modules/.bin/markdownlint-cli2" ]]; then
    "$ROOT_DIR/node_modules/.bin/markdownlint-cli2" "**/*.md"
    return
  fi

  echo "Skipping markdownlint: markdownlint-cli2 not installed locally"
}

run_local_pr_closure_check() {
  local branch base_ref changed_files pr_body issue_numbers body_input
  branch="$(git branch --show-current)"
  base_ref="${OPENPRECEDENT_PREFLIGHT_BASE_REF:-upstream/main}"

  if [[ -z "$branch" ]]; then
    return 0
  fi

  if ! git rev-parse --verify "$base_ref" >/dev/null 2>&1; then
    echo "Skipping PR closure sync check: base ref $base_ref is unavailable"
    return 0
  fi

  changed_files="$(git diff --name-only "$base_ref"...HEAD)"
  if [[ -z "$changed_files" ]]; then
    return 0
  fi

  pr_body="$(
    gh pr view --json body --jq .body 2>/dev/null || true
  )"
  if [[ -z "$pr_body" ]]; then
    issue_numbers="$(printf '%s\n' "$changed_files" | sed -n 's#^.*/##; s#\.md$##p' | xargs -r rg -N '^issue: ' .codex/pm/tasks -g '*.md' -l 2>/dev/null || true)"
    return 0
  fi

  body_input=("--pr-body" "$pr_body")
  while IFS= read -r path; do
    [[ -n "$path" ]] || continue
    body_input+=("--changed-file" "$path")
  done <<< "$changed_files"

  PYTHONPATH=src "$PYTHON_BIN" -m openprecedent.codex_pm verify-pr-closure-sync "${body_input[@]}"
}

check_issue_state() {
  local output
  local status

  set +e
  output="$(
    PYTHONPATH=src "$PYTHON_BIN" -m openprecedent.codex_pm issue-state-check 2>&1
  )"
  status=$?
  set -e
  if [[ $status -eq 0 ]]; then
    echo "$output"
    return 0
  fi

  if [[ "$ENFORCE_ISSUE_STATE" == "1" ]]; then
    echo "$output"
    exit 1
  fi

  echo "$output"
  echo "Continuing without enforced issue-state check. Set OPENPRECEDENT_PREFLIGHT_ENFORCE_ISSUE_STATE=1 to require it."
}

echo "Running agent preflight in $ROOT_DIR"

check_branch_freshness
check_review_note
check_review_proof
check_issue_state
check_merged_branch_reuse

echo "Running pytest"
PYTHONPATH=src OPENPRECEDENT_PYTHON_BIN="$PYTHON_BIN" ./scripts/run-pytest.sh $PYTEST_ARGS

run_rust_tests_if_needed

echo "Running markdownlint if available"
run_markdownlint_if_available

echo "Running local PR closure sync check if PR body is available"
run_local_pr_closure_check

if [[ "$RUN_E2E" == "1" ]]; then
  echo "Running standard E2E"
  ./scripts/run-e2e.sh
fi

echo "Agent preflight passed."
