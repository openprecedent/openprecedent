#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import one exported HarnessHub Codex development round into the shared runtime and extract decisions."
    )
    parser.add_argument("--bundle-dir", required=True, help="Path to the exported HarnessHub round bundle")
    parser.add_argument(
        "--runtime-home",
        help="Override OPENPRECEDENT_HOME. Defaults to the environment variable or ~/.openprecedent/runtime.",
    )
    parser.add_argument(
        "--python-bin",
        help="Python binary used to run the OpenPrecedent CLI. Defaults to .venv/bin/python or python3.",
    )
    parser.add_argument(
        "--skip-if-case-exists",
        action="store_true",
        help="Return success without importing when the target case already exists.",
    )
    return parser.parse_args()


def resolve_runtime_home(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    env_value = os.environ.get("OPENPRECEDENT_HOME")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return Path.home() / ".openprecedent" / "runtime"


def resolve_python_bin(explicit: str | None) -> str:
    if explicit:
        return explicit
    root_dir = Path(__file__).resolve().parents[1]
    bundled = root_dir / ".venv" / "bin" / "python"
    if bundled.exists():
        return str(bundled)
    return sys.executable


def run_openprecedent(python_bin: str, runtime_home: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["OPENPRECEDENT_HOME"] = str(runtime_home)
    result = subprocess.run(
        [python_bin, "-c", "from openprecedent.cli import run; run()", *args],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )
    return result


def load_manifest(bundle_dir: Path) -> dict[str, object]:
    return json.loads((bundle_dir / "round-manifest.json").read_text(encoding="utf-8"))


def main() -> int:
    args = parse_args()
    bundle_dir = Path(args.bundle_dir).expanduser().resolve()
    manifest = load_manifest(bundle_dir)
    runtime_home = resolve_runtime_home(args.runtime_home)
    python_bin = resolve_python_bin(args.python_bin)

    case_id = str(manifest["case_id"])
    case_title = str(manifest["case_title"])
    agent_id = str(manifest.get("import_hints", {}).get("agent_id", "codex"))
    events_path = bundle_dir / str(manifest.get("import_hints", {}).get("event_import_path", "events.jsonl"))

    show_result = run_openprecedent(python_bin, runtime_home, "case", "show", case_id)
    if show_result.returncode == 0:
        if args.skip_if_case_exists:
            print(json.dumps({"case_id": case_id, "status": "skipped_existing"}))
            return 0
        raise SystemExit(f"case already exists: {case_id}")

    create_result = run_openprecedent(
        python_bin,
        runtime_home,
        "case",
        "create",
        "--case-id",
        case_id,
        "--title",
        case_title,
        "--agent-id",
        agent_id,
    )
    if create_result.returncode != 0:
        raise SystemExit(create_result.stderr.strip() or create_result.stdout.strip())

    import_result = run_openprecedent(
        python_bin,
        runtime_home,
        "event",
        "import-jsonl",
        str(events_path),
    )
    if import_result.returncode != 0:
        raise SystemExit(import_result.stderr.strip() or import_result.stdout.strip())

    extract_result = run_openprecedent(
        python_bin,
        runtime_home,
        "extract",
        "decisions",
        case_id,
    )
    if extract_result.returncode != 0:
        raise SystemExit(extract_result.stderr.strip() or extract_result.stdout.strip())

    decisions = json.loads(extract_result.stdout)
    imported_events = json.loads(import_result.stdout)
    print(
        json.dumps(
            {
                "case_id": case_id,
                "imported_event_count": len(imported_events),
                "decision_count": len(decisions),
                "decision_types": [item["decision_type"] for item in decisions],
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
