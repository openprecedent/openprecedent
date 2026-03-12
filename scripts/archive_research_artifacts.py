#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a sanitized research archive from OpenPrecedent runtime artifacts."
    )
    parser.add_argument("--study", required=True, help="Study slug, for example: harnesshub")
    parser.add_argument(
        "--query",
        action="append",
        default=[],
        help="Case-insensitive text filter applied to task_summary and current_plan. Repeatable.",
    )
    parser.add_argument(
        "--repo-root",
        action="append",
        default=[],
        help="Repository root whose absolute paths should be normalized to relative paths. Repeatable.",
    )
    parser.add_argument(
        "--runtime-home",
        help="Override OPENPRECEDENT_HOME. Defaults to the environment variable or ~/.openprecedent/runtime.",
    )
    parser.add_argument(
        "--output-root",
        default="research-artifacts",
        help="Repository-relative output root for sanitized archives.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=200,
        help="Maximum number of invocation records to archive after filtering.",
    )
    parser.add_argument(
        "--include-empty",
        action="store_true",
        help="Include archives even when no matching invocations are found.",
    )
    return parser.parse_args()


def resolve_runtime_home(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()
    env_value = os.environ.get("OPENPRECEDENT_HOME")
    if env_value:
        return Path(env_value).expanduser().resolve()
    return Path.home() / ".openprecedent" / "runtime"


def stamp_now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H%M%SZ")


def normalize_query_terms(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


@dataclass(frozen=True)
class RepoRoot:
    absolute: Path
    label: str


def load_repo_roots(values: list[str]) -> list[RepoRoot]:
    roots: list[RepoRoot] = []
    for value in values:
        absolute = Path(value).expanduser().resolve()
        roots.append(RepoRoot(absolute=absolute, label=absolute.name))
    roots.sort(key=lambda item: len(str(item.absolute)), reverse=True)
    return roots


def load_invocations(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as error:
                raise ValueError(
                    f"invalid JSON in runtime invocation log at line {line_no}"
                ) from error
    return rows


def invocation_matches(row: dict[str, object], terms: list[str]) -> bool:
    if not terms:
        return True
    haystack = " ".join(
        str(row.get(key, "")) for key in ("task_summary", "current_plan", "candidate_action")
    ).lower()
    return all(term in haystack for term in terms)


def sanitize_text(value: object) -> object:
    if not isinstance(value, str):
        return value
    sanitized = re.sub(r"/workspace/[^\\s\"']+", "<workspace-path>", value)
    sanitized = re.sub(r"/root/[^\\s\"']+", "<root-path>", sanitized)
    sanitized = re.sub(r"/home/[^\\s\"']+", "<home-path>", sanitized)
    return sanitized


def _render_repo_relative(root: RepoRoot, relative: Path) -> str:
    relative_text = relative.as_posix()
    return f"{root.label}/{relative_text}" if relative_text != "." else root.label


def sanitize_known_path(value: str, repo_roots: list[RepoRoot]) -> str:
    path = Path(value).expanduser()

    if not path.is_absolute():
        matching_roots = [
            root for root in repo_roots if (root.absolute / path).exists()
        ]
        if matching_roots:
            return _render_repo_relative(matching_roots[0], path)
        if len(repo_roots) == 1:
            return _render_repo_relative(repo_roots[0], path)
        return path.as_posix()

    try:
        resolved = path.resolve(strict=False)
    except OSError:
        resolved = path
    for root in repo_roots:
        try:
            relative = resolved.relative_to(root.absolute)
            return _render_repo_relative(root, relative)
        except ValueError:
            continue
    path_text = str(resolved)
    path_text = path_text.replace(str(Path.home()), "<home>")
    path_text = re.sub(r"^/workspace/", "<workspace>/", path_text)
    return path_text


def sanitize_invocation(
    row: dict[str, object],
    repo_roots: list[RepoRoot],
) -> dict[str, object]:
    sanitized = dict(row)
    if "known_files" in sanitized and isinstance(sanitized["known_files"], list):
        sanitized["known_files"] = [
            sanitize_known_path(str(item), repo_roots) for item in sanitized["known_files"]
        ]
    for key in ("task_summary", "current_plan", "candidate_action", "task_frame", "suggested_focus"):
        sanitized[key] = sanitize_text(sanitized.get(key))
    for key in (
        "accepted_constraints",
        "success_criteria",
        "rejected_options",
        "authority_signals",
        "cautions",
        "matched_case_ids",
    ):
        if isinstance(sanitized.get(key), list):
            sanitized[key] = [sanitize_text(item) for item in sanitized[key]]
    if sanitized.get("session_id"):
        sanitized["session_id"] = "<redacted-session>"
    return sanitized


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True))
            handle.write("\n")


def build_readme(
    study: str,
    stamp: str,
    invocation_count: int,
    query_terms: list[str],
) -> str:
    query_text = ", ".join(query_terms) if query_terms else "(no query filter)"
    return "\n".join(
        [
            f"# Research Archive: {study}",
            "",
            f"- Archive stamp: `{stamp}`",
            f"- Sanitized invocation count: `{invocation_count}`",
            f"- Query terms: `{query_text}`",
            "",
            "Files:",
            "",
            "- `archive-manifest.json`: provenance and sanitization settings",
            "- `runtime-invocations-sanitized.jsonl`: sanitized runtime invocation records",
            "- `archive-summary.json`: aggregate counts and filters",
            "",
            "This archive is git-safe evidence intended for research review, not a full runtime backup.",
            "",
        ]
    )


def main() -> int:
    args = parse_args()
    runtime_home = resolve_runtime_home(args.runtime_home)
    invocation_log = runtime_home / "openprecedent-runtime-invocations.jsonl"
    query_terms = normalize_query_terms(args.query)
    repo_roots = load_repo_roots(args.repo_root)

    rows = load_invocations(invocation_log)
    filtered = [row for row in rows if invocation_matches(row, query_terms)]
    selected = filtered[-args.limit :]
    sanitized = [sanitize_invocation(row, repo_roots) for row in selected]

    if not sanitized and not args.include_empty:
        print("No matching invocation records found. Nothing archived.")
        return 0

    stamp = stamp_now()
    output_dir = Path(args.output_root) / args.study / stamp
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "study": args.study,
        "stamp": stamp,
        "created_at": datetime.now(UTC).isoformat(),
        "source": {
            "runtime_home": str(runtime_home),
            "invocation_log": str(invocation_log),
        },
        "filters": {
            "query_terms": query_terms,
            "limit": args.limit,
        },
        "sanitization": {
            "repo_roots": [str(item.absolute) for item in repo_roots],
            "session_id": "redacted",
            "known_files": "repo-relative when possible",
        },
        "counts": {
            "total_invocations_seen": len(rows),
            "matching_invocations": len(filtered),
            "archived_invocations": len(sanitized),
        },
    }
    summary = {
        "study": args.study,
        "stamp": stamp,
        "query_terms": query_terms,
        "archived_invocation_count": len(sanitized),
        "query_reasons": sorted(
            {
                str(row.get("query_reason"))
                for row in sanitized
                if row.get("query_reason") is not None
            }
        ),
    }

    write_json(output_dir / "archive-manifest.json", manifest)
    write_jsonl(output_dir / "runtime-invocations-sanitized.jsonl", sanitized)
    write_json(output_dir / "archive-summary.json", summary)
    (output_dir / "README.md").write_text(
        build_readme(args.study, stamp, len(sanitized), query_terms), encoding="utf-8"
    )

    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
