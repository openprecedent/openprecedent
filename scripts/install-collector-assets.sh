#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-systemd}"

render_template() {
  local source_path="$1"
  local escaped_root
  escaped_root="$(printf '%s\n' "$ROOT_DIR" | sed 's/[&]/\\&/g')"
  sed "s|__OPENPRECEDENT_ROOT__|$escaped_root|g" "$source_path"
}

install_systemd() {
  local target_dir="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
  mkdir -p "$target_dir"

  render_template "$ROOT_DIR/deploy/systemd/openprecedent-collector.service" \
    > "$target_dir/openprecedent-collector.service"
  cp "$ROOT_DIR/deploy/systemd/openprecedent-collector.timer" \
    "$target_dir/openprecedent-collector.timer"

  cat <<EOF
Installed:
- $target_dir/openprecedent-collector.service
- $target_dir/openprecedent-collector.timer

Next:
  systemctl --user daemon-reload
  systemctl --user enable --now openprecedent-collector.timer
  systemctl --user list-timers openprecedent-collector.timer
EOF
}

install_cron() {
  local target_path="${1:-$ROOT_DIR/runtime/openprecedent-collector.cron}"
  mkdir -p "$(dirname "$target_path")"
  render_template "$ROOT_DIR/deploy/cron/openprecedent-collector.cron" > "$target_path"

  cat <<EOF
Rendered:
- $target_path

Next:
  crontab "$target_path"
  crontab -l
EOF
}

case "$MODE" in
  systemd)
    install_systemd
    ;;
  cron)
    install_cron "${2:-}"
    ;;
  *)
    echo "usage: $0 [systemd|cron] [cron-output-path]" >&2
    exit 1
    ;;
esac
