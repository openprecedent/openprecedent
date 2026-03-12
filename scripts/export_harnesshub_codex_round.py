#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export one completed HarnessHub Codex development round as an importable searchable-history bundle."
    )
    parser.add_argument("--repo-root", required=True, help="HarnessHub repository root")
    parser.add_argument("--issue", required=True, type=int, help="HarnessHub issue number")
    parser.add_argument("--task-path", required=True, help="Path to the HarnessHub local task twin")
    parser.add_argument("--state-path", required=True, help="Path to the HarnessHub local issue-state file")
    parser.add_argument("--commit", required=True, help="Commit sha for the completed round")
    parser.add_argument(
        "--runtime-home",
        help="Override OPENPRECEDENT_HOME. Defaults to the environment variable or ~/.openprecedent/runtime.",
    )
    parser.add_argument(
        "--study",
        default="harnesshub",
        help="Study slug used in the output directory and case identity.",
    )
    parser.add_argument(
        "--output-root",
        default="research-artifacts/harnesshub-rounds",
        help="Repository-relative output root for exported round bundles.",
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


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "round"


def parse_frontmatter_title(text: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    for line in text[4:end].splitlines():
        if line.startswith("title:"):
            return line.partition(":")[2].strip()
    return None


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if current is not None:
            sections[current].append(line)
    return {key: "\n".join(value).strip() for key, value in sections.items()}


def parse_bullets(text: str) -> list[str]:
    return [line.strip()[2:].strip() for line in text.splitlines() if line.strip().startswith("- ")]


def run_git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def read_commit(repo_root: Path, commit: str) -> dict[str, object]:
    details = run_git(repo_root, "show", "--no-patch", "--format=%H%n%s%n%aI%n%an", commit).splitlines()
    if len(details) < 4:
        raise ValueError(f"unexpected commit metadata for {commit}")
    changed_files = [
        line.strip()
        for line in run_git(
            repo_root,
            "diff-tree",
            "--root",
            "--no-commit-id",
            "--name-only",
            "-r",
            commit,
        ).splitlines()
        if line.strip()
    ]
    return {
        "sha": details[0].strip(),
        "subject": details[1].strip(),
        "authored_at": details[2].strip(),
        "author_name": details[3].strip(),
        "changed_files": changed_files,
    }


def load_runtime_invocations(runtime_home: Path, issue_number: int) -> list[dict[str, object]]:
    log_path = runtime_home / "openprecedent-runtime-invocations.jsonl"
    if not log_path.exists():
        return []
    marker = f"#{issue_number}"
    selected: list[dict[str, object]] = []
    for line in log_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        haystack = " ".join(
            str(row.get(key, "")) for key in ("task_summary", "current_plan", "candidate_action")
        )
        if marker in haystack:
            selected.append(row)
    return selected


def build_user_message(issue_number: int, task_title: str, deliverable: str, scope: list[str]) -> str:
    parts = [f"Issue #{issue_number}: {task_title}."]
    if deliverable:
        parts.append(deliverable)
    if scope:
        parts.append("Focus only on: " + "; ".join(scope) + ".")
    return " ".join(parts).strip()


def build_agent_message(task_title: str, state_summary: str, acceptance: list[str]) -> str:
    parts = [f"I will {task_title.lower()}."]
    if state_summary:
        parts.append(state_summary)
    if acceptance:
        parts.append("Done when: " + "; ".join(acceptance) + ".")
    return " ".join(parts).strip()


def build_completion_message(issue_number: int, commit: dict[str, object]) -> str:
    changed_files = commit["changed_files"]
    file_summary = ", ".join(changed_files[:6]) if changed_files else "no file changes recorded"
    return (
        f"Completed HarnessHub issue #{issue_number} via commit {commit['subject']}. "
        f"Changed files: {file_summary}."
    )


def build_events(
    *,
    case_id: str,
    repo_root: Path,
    issue_number: int,
    user_message: str,
    agent_message: str,
    completion_message: str,
    runtime_invocations: list[dict[str, object]],
    commit: dict[str, object],
) -> list[dict[str, object]]:
    authored_at = datetime.fromisoformat(str(commit["authored_at"]).replace("Z", "+00:00"))
    start_time = authored_at - timedelta(minutes=5)
    events: list[dict[str, object]] = []

    def append_event(
        sequence_no: int,
        event_type: str,
        actor: str,
        timestamp: datetime,
        payload: dict[str, object],
    ) -> None:
        events.append(
            {
                "case_id": case_id,
                "event_id": f"{case_id}-evt-{sequence_no}",
                "event_type": event_type,
                "actor": actor,
                "timestamp": timestamp.astimezone(UTC).isoformat().replace("+00:00", "Z"),
                "sequence_no": sequence_no,
                "payload": payload,
            }
        )

    append_event(
        1,
        "case.started",
        "system",
        start_time,
        {
            "repo_root": str(repo_root),
            "issue": issue_number,
            "commit": commit["sha"],
            "source": "harnesshub-round-export",
        },
    )
    append_event(2, "message.user", "user", start_time + timedelta(seconds=30), {"message": user_message})
    append_event(3, "message.agent", "agent", start_time + timedelta(seconds=60), {"message": agent_message})

    sequence_no = 4
    for invocation in runtime_invocations:
        recorded_at = datetime.fromisoformat(str(invocation["recorded_at"]).replace("Z", "+00:00"))
        append_event(
            sequence_no,
            "message.user",
            "user",
            recorded_at,
            {
                "message": str(invocation.get("task_summary") or ""),
                "source": "runtime-invocation",
                "invocation_id": invocation.get("invocation_id"),
                "query_reason": invocation.get("query_reason"),
            },
        )
        sequence_no += 1
        synthesized_agent = str(invocation.get("current_plan") or invocation.get("candidate_action") or completion_message)
        append_event(
            sequence_no,
            "message.agent",
            "agent",
            recorded_at + timedelta(seconds=1),
            {
                "message": synthesized_agent,
                "source": "runtime-invocation",
                "invocation_id": invocation.get("invocation_id"),
            },
        )
        sequence_no += 1

    for changed_file in commit["changed_files"]:
        append_event(
            sequence_no,
            "file.write",
            "system",
            authored_at,
            {
                "path": changed_file,
                "summary": f"Changed in commit {commit['sha']}",
            },
        )
        sequence_no += 1

    append_event(
        sequence_no,
        "message.agent",
        "agent",
        authored_at + timedelta(seconds=30),
        {"message": completion_message},
    )
    sequence_no += 1
    append_event(
        sequence_no,
        "case.completed",
        "system",
        authored_at + timedelta(seconds=60),
        {
            "message": completion_message,
            "commit": commit["sha"],
            "issue": issue_number,
        },
    )
    return events


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True))
            handle.write("\n")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    task_path = Path(args.task_path).expanduser().resolve()
    state_path = Path(args.state_path).expanduser().resolve()
    runtime_home = resolve_runtime_home(args.runtime_home)

    task_text = task_path.read_text(encoding="utf-8")
    state_text = state_path.read_text(encoding="utf-8")
    task_title = parse_frontmatter_title(task_text) or f"HarnessHub issue {args.issue}"
    task_sections = parse_sections(task_text)
    state_sections = parse_sections(state_text)
    deliverable = task_sections.get("Deliverable", "")
    scope = parse_bullets(task_sections.get("Scope", ""))
    acceptance = parse_bullets(task_sections.get("Acceptance Criteria", ""))
    state_summary = state_sections.get("Summary", "")

    runtime_invocations = load_runtime_invocations(runtime_home, args.issue)
    commit = read_commit(repo_root, args.commit)
    slug = slugify(task_title)[:48]
    case_id = f"case_{args.study}_issue_{args.issue}_{slug}"
    case_title = f"HarnessHub issue #{args.issue}: {task_title}"
    stamp = stamp_now()
    output_dir = Path(args.output_root) / f"issue-{args.issue}-{slug}-{stamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    user_message = build_user_message(args.issue, task_title, deliverable, scope)
    agent_message = build_agent_message(task_title, state_summary, acceptance)
    completion_message = build_completion_message(args.issue, commit)
    events = build_events(
        case_id=case_id,
        repo_root=repo_root,
        issue_number=args.issue,
        user_message=user_message,
        agent_message=agent_message,
        completion_message=completion_message,
        runtime_invocations=runtime_invocations,
        commit=commit,
    )

    shutil.copy2(task_path, output_dir / "source-task.md")
    shutil.copy2(state_path, output_dir / "source-issue-state.md")
    write_jsonl(output_dir / "source-runtime-invocations.jsonl", runtime_invocations)
    write_json(output_dir / "source-commit.json", commit)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(
        output_dir / "round-manifest.json",
        {
            "study": args.study,
            "issue": args.issue,
            "case_id": case_id,
            "case_title": case_title,
            "repo_root": str(repo_root),
            "task_path": str(task_path),
            "state_path": str(state_path),
            "runtime_home": str(runtime_home),
            "commit": commit["sha"],
            "runtime_invocation_count": len(runtime_invocations),
            "artifact_files": [
                "source-task.md",
                "source-issue-state.md",
                "source-runtime-invocations.jsonl",
                "source-commit.json",
                "events.jsonl",
            ],
            "import_hints": {
                "case_id": case_id,
                "title": case_title,
                "agent_id": "codex",
                "event_import_path": "events.jsonl",
            },
        },
    )
    (output_dir / "README.md").write_text(
        "\n".join(
            [
                f"# HarnessHub Round Export: issue #{args.issue}",
                "",
                f"- Case id: `{case_id}`",
                f"- Commit: `{commit['sha']}`",
                f"- Runtime invocation count: `{len(runtime_invocations)}`",
                "",
                "This bundle is the minimal searchable-history export for one completed HarnessHub Codex development round.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
