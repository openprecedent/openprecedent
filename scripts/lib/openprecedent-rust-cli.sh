resolve_openprecedent_rust_cli() {
  local root_dir="$1"

  if [[ -n "${OPENPRECEDENT_BIN:-}" ]]; then
    printf '%s\n' "$OPENPRECEDENT_BIN"
    return 0
  fi

  if [[ -x "$root_dir/target/release/openprecedent" ]]; then
    printf '%s\n' "$root_dir/target/release/openprecedent"
    return 0
  fi

  if [[ -x "$root_dir/target/debug/openprecedent" ]]; then
    printf '%s\n' "$root_dir/target/debug/openprecedent"
    return 0
  fi

  if ! command -v cargo >/dev/null 2>&1; then
    echo "Rust openprecedent CLI is unavailable: set OPENPRECEDENT_BIN or install cargo." >&2
    return 1
  fi

  cargo build -q -p openprecedent-cli --manifest-path "$root_dir/Cargo.toml"

  if [[ -x "$root_dir/target/debug/openprecedent" ]]; then
    printf '%s\n' "$root_dir/target/debug/openprecedent"
    return 0
  fi

  echo "Rust openprecedent CLI build completed but target/debug/openprecedent was not found." >&2
  return 1
}
