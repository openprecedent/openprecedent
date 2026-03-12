#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill and auto-seed the shared OpenPrecedent runtime from completed HarnessHub rounds."
    )
    parser.add_argument("--repo-root", required=True, help="HarnessHub repository root")
    parser.add_argument(
        "--runtime-home",
        help="Override OPENPRECEDENT_HOME. Defaults to the environment variable or ~/.openprecedent/runtime.",
    )
    parser.add_argument(
        "--python-bin",
        help="Python binary used to run the local OpenPrecedent scripts. Defaults to .venv/bin/python or python3.",
    )
    parser.add_argument(
        "--export-output-root",
        help="Directory used for intermediate exported round bundles. Defaults to <runtime-home>/harnesshub-round-bundles.",
    )
    parser.add_argument(
        "--issue",
        dest="issues",
        type=int,
        action="append",
        help="Restrict sync to one or more HarnessHub issue numbers.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero when any completed round cannot yet be resolved for export/import.",
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
    parent_bundled = root_dir.parent / "openprecedent" / ".venv" / "bin" / "python"
    if parent_bundled.exists():
        return str(parent_bundled)
    return sys.executable


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        result[key.strip()] = value.strip()
    return result


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "round"


def run_git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def resolve_task_candidates(repo_root: Path, selected_issues: set[int] | None) -> list[dict[str, object]]:
    tasks_root = repo_root / ".codex" / "pm" / "tasks"
    candidates: list[dict[str, object]] = []
    for task_path in sorted(tasks_root.rglob("*.md")):
        frontmatter = parse_frontmatter(task_path)
        if frontmatter.get("status") != "done":
            continue
        issue_text = frontmatter.get("issue")
        if issue_text is None or not issue_text.isdigit():
            continue
        issue = int(issue_text)
        if selected_issues and issue not in selected_issues:
            continue
        title = frontmatter.get("title")
        if not title:
            continue
        state_path_text = frontmatter.get("state_path")
        state_path = repo_root / state_path_text if state_path_text else None
        if state_path is None or not state_path.exists():
            continue
        candidates.append(
            {
                "issue": issue,
                "title": title,
                "task_path": task_path,
                "state_path": state_path,
                "case_id": f"case_harnesshub_issue_{issue}_{slugify(title)[:48]}",
            }
        )
    return candidates


def resolve_commit_for_task(repo_root: Path, issue: int, title: str) -> str | None:
    merge_subject = run_git(repo_root, "log", "--merges", "--format=%H\t%s", "--grep", f"issue-{issue}", "-n", "1").strip()
    if merge_subject:
        return merge_subject.split("\t", 1)[0]

    title_subject = run_git(repo_root, "log", "--format=%H\t%s", "--grep", title, "-n", "1").strip()
    if title_subject:
        return title_subject.split("\t", 1)[0]

    return None


def case_exists(runtime_home: Path, case_id: str) -> bool:
    db_path = runtime_home / "openprecedent.db"
    if not db_path.exists():
        return False
    conn = sqlite3.connect(db_path)
    try:
        row = conn.execute("SELECT 1 FROM cases WHERE case_id = ? LIMIT 1", (case_id,)).fetchone()
    finally:
        conn.close()
    return row is not None


def db_counts(runtime_home: Path) -> dict[str, int]:
    db_path = runtime_home / "openprecedent.db"
    if not db_path.exists():
        return {"cases": 0, "events": 0, "decisions": 0}
    conn = sqlite3.connect(db_path)
    try:
        return {
            "cases": conn.execute("SELECT COUNT(*) FROM cases").fetchone()[0],
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "decisions": conn.execute("SELECT COUNT(*) FROM decisions").fetchone()[0],
        }
    finally:
        conn.close()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    runtime_home = resolve_runtime_home(args.runtime_home)
    python_bin = resolve_python_bin(args.python_bin)
    export_output_root = (
        Path(args.export_output_root).expanduser().resolve()
        if args.export_output_root
        else runtime_home / "harnesshub-round-bundles"
    )
    export_output_root.mkdir(parents=True, exist_ok=True)
    runtime_home.mkdir(parents=True, exist_ok=True)

    selected_issues = set(args.issues or [])
    candidates = resolve_task_candidates(repo_root, selected_issues or None)

    script_root = Path(__file__).resolve().parent
    export_script = script_root / "export_harnesshub_codex_round.py"
    import_script = script_root / "import_harnesshub_codex_round.py"

    imported: list[dict[str, object]] = []
    skipped_existing: list[dict[str, object]] = []
    unresolved: list[dict[str, object]] = []

    for candidate in candidates:
        issue = int(candidate["issue"])
        title = str(candidate["title"])
        case_id = str(candidate["case_id"])
        if case_exists(runtime_home, case_id):
            skipped_existing.append({"issue": issue, "case_id": case_id, "reason": "case_exists"})
            continue

        commit = resolve_commit_for_task(repo_root, issue, title)
        if commit is None:
            unresolved.append({"issue": issue, "title": title, "reason": "commit_not_found"})
            continue

        export_result = subprocess.run(
            [
                python_bin,
                str(export_script),
                "--repo-root",
                str(repo_root),
                "--issue",
                str(issue),
                "--task-path",
                str(candidate["task_path"]),
                "--state-path",
                str(candidate["state_path"]),
                "--commit",
                commit,
                "--runtime-home",
                str(runtime_home),
                "--output-root",
                str(export_output_root),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if export_result.returncode != 0:
            unresolved.append(
                {"issue": issue, "title": title, "reason": "export_failed", "detail": export_result.stderr.strip()}
            )
            continue

        bundle_dir = Path(export_result.stdout.strip())
        import_result = subprocess.run(
            [
                python_bin,
                str(import_script),
                "--bundle-dir",
                str(bundle_dir),
                "--runtime-home",
                str(runtime_home),
                "--python-bin",
                python_bin,
                "--skip-if-case-exists",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if import_result.returncode != 0:
            unresolved.append(
                {"issue": issue, "title": title, "reason": "import_failed", "detail": import_result.stderr.strip()}
            )
            continue

        imported.append(
            {
                "issue": issue,
                "title": title,
                "case_id": case_id,
                "commit": commit,
                "bundle_dir": str(bundle_dir),
                "import_summary": json.loads(import_result.stdout),
            }
        )

    print(
        json.dumps(
            {
                "repo_root": str(repo_root),
                "runtime_home": str(runtime_home),
                "export_output_root": str(export_output_root),
                "candidate_issue_count": len(candidates),
                "imported_count": len(imported),
                "skipped_existing_count": len(skipped_existing),
                "unresolved_count": len(unresolved),
                "imported": imported,
                "skipped_existing": skipped_existing,
                "unresolved": unresolved,
                "db_counts": db_counts(runtime_home),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0 if (not unresolved or not args.strict) else 1


if __name__ == "__main__":
    raise SystemExit(main())
