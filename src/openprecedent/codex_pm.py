from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path


PM_ROOT = Path(".codex/pm")
VALID_STATUSES = ("backlog", "in_progress", "blocked", "done")


@dataclass
class PMDocument:
    path: Path
    metadata: dict[str, str]
    sections: dict[str, str]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="openprecedent-pm")
    subparsers = parser.add_subparsers(dest="action", required=True)

    subparsers.add_parser("init")

    prd_new = subparsers.add_parser("prd-new")
    prd_new.add_argument("slug")
    prd_new.add_argument("--title", required=True)

    epic_new = subparsers.add_parser("epic-new")
    epic_new.add_argument("slug")
    epic_new.add_argument("--title", required=True)
    epic_new.add_argument("--prd")

    task_new = subparsers.add_parser("task-new")
    task_new.add_argument("epic")
    task_new.add_argument("slug")
    task_new.add_argument("--title", required=True)
    task_new.add_argument("--issue")
    task_new.add_argument("--labels", default="")
    task_new.add_argument("--status", default="backlog", choices=VALID_STATUSES)
    task_new.add_argument("--depends-on", default="")

    tasks = subparsers.add_parser("tasks")
    tasks.add_argument("--status")
    tasks.add_argument("--epic")
    tasks.add_argument("--json", action="store_true", dest="as_json")

    next_task = subparsers.add_parser("next")
    next_task.add_argument("--epic")
    next_task.add_argument("--json", action="store_true", dest="as_json")

    set_status = subparsers.add_parser("set-status")
    set_status.add_argument("path")
    set_status.add_argument("status", choices=VALID_STATUSES)
    set_status.add_argument("--reason", default="")

    blocked = subparsers.add_parser("blocked")
    blocked.add_argument("path")
    blocked.add_argument("--reason", required=True)

    subparsers.add_parser("standup").add_argument("--json", action="store_true", dest="as_json")

    issue_body = subparsers.add_parser("issue-body")
    issue_body.add_argument("path")

    pr_body = subparsers.add_parser("pr-body")
    pr_body.add_argument("path")
    pr_body.add_argument("--issue", type=int)
    pr_body.add_argument("--tests", action="append", default=[])

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.action == "init":
        _init_pm()
        return 0
    if args.action == "prd-new":
        _init_pm()
        path = PM_ROOT / "prds" / f"{args.slug}.md"
        _write_document(
            path,
            metadata={
                "type": "prd",
                "slug": args.slug,
                "title": args.title,
                "status": "draft",
            },
            sections={
                "Summary": "",
                "Problem": "",
                "Goals": "- ",
                "Non-Goals": "- ",
                "Success Criteria": "- ",
                "Dependencies": "- ",
            },
        )
        print(path)
        return 0
    if args.action == "epic-new":
        _init_pm()
        path = PM_ROOT / "epics" / f"{args.slug}.md"
        metadata = {
            "type": "epic",
            "slug": args.slug,
            "title": args.title,
            "status": "backlog",
        }
        if args.prd:
            metadata["prd"] = args.prd
        _write_document(
            path,
            metadata=metadata,
            sections={
                "Outcome": "",
                "Scope": "- ",
                "Acceptance Criteria": "- ",
                "Child Issues": "- ",
                "Notes": "",
            },
        )
        print(path)
        return 0
    if args.action == "task-new":
        _init_pm()
        path = PM_ROOT / "tasks" / args.epic / f"{args.slug}.md"
        metadata = {
            "type": "task",
            "epic": args.epic,
            "slug": args.slug,
            "title": args.title,
            "status": args.status,
            "labels": args.labels,
            "depends_on": args.depends_on,
        }
        if args.issue:
            metadata["issue"] = args.issue
        _write_document(
            path,
            metadata=metadata,
            sections={
                "Context": "",
                "Deliverable": "",
                "Scope": "- ",
                "Acceptance Criteria": "- ",
                "Validation": "- ",
                "Implementation Notes": "",
            },
        )
        print(path)
        return 0
    if args.action == "tasks":
        documents = _load_tasks(status=args.status, epic=args.epic)
        return _print_tasks(documents, args.as_json)
    if args.action == "next":
        documents = _load_tasks(status=None, epic=args.epic)
        candidates = [document for document in documents if document.metadata.get("status") == "backlog"]
        if not candidates:
            if args.as_json:
                print("null")
            else:
                print("No backlog task found.")
            return 0
        next_document = _sort_tasks(candidates)[0]
        if args.as_json:
            print(json.dumps(_doc_to_dict(next_document), ensure_ascii=True, indent=2, sort_keys=True))
        else:
            print(next_document.path)
        return 0
    if args.action == "set-status":
        document = _read_document(Path(args.path))
        document.metadata["status"] = args.status
        if args.reason:
            document.metadata["status_reason"] = args.reason
        _persist_document(document)
        print(document.path)
        return 0
    if args.action == "blocked":
        document = _read_document(Path(args.path))
        document.metadata["status"] = "blocked"
        document.metadata["status_reason"] = args.reason
        _persist_document(document)
        print(document.path)
        return 0
    if args.action == "standup":
        documents = _load_tasks()
        summary = {
            "backlog": [],
            "in_progress": [],
            "blocked": [],
            "done": [],
        }
        for document in _sort_tasks(documents):
            summary[document.metadata.get("status", "backlog")].append(_doc_to_dict(document))
        if args.as_json:
            print(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True))
        else:
            for status in VALID_STATUSES:
                print(f"{status}: {len(summary[status])}")
                for item in summary[status]:
                    print(f"  - {item['title']} ({item['path']})")
        return 0
    if args.action == "issue-body":
        document = _read_document(Path(args.path))
        print(_render_issue_body(document))
        return 0
    if args.action == "pr-body":
        document = _read_document(Path(args.path))
        print(_render_pr_body(document, issue=args.issue, tests=args.tests))
        return 0

    parser.error("unknown action")
    return 2


def run() -> None:
    raise SystemExit(main())


def _init_pm() -> None:
    for name in ("prds", "epics", "tasks", "context", "updates"):
        (PM_ROOT / name).mkdir(parents=True, exist_ok=True)


def _write_document(path: Path, *, metadata: dict[str, str], sections: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = PMDocument(path=path, metadata=metadata, sections=sections)
    _persist_document(document)


def _persist_document(document: PMDocument) -> None:
    lines = ["---"]
    for key, value in document.metadata.items():
        if value:
            lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    for heading, body in document.sections.items():
        lines.append(f"## {heading}")
        lines.append("")
        if body:
            lines.extend(body.rstrip().splitlines())
        lines.append("")
    document.path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def _read_document(path: Path) -> PMDocument:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, str] = {}
    sections: dict[str, str] = {}

    if not text.startswith("---\n"):
        raise ValueError(f"document missing frontmatter: {path}")
    _, remainder = text.split("---\n", 1)
    frontmatter, body = remainder.split("---\n", 1)
    for line in frontmatter.strip().splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition(":")
        metadata[key.strip()] = value.strip()

    current_heading: str | None = None
    current_lines: list[str] = []
    for line in body.splitlines():
        if line.startswith("## "):
            if current_heading is not None:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = line[3:].strip()
            current_lines = []
            continue
        if line.startswith("# "):
            continue
        if current_heading is not None:
            current_lines.append(line)
    if current_heading is not None:
        sections[current_heading] = "\n".join(current_lines).strip()

    return PMDocument(path=path, metadata=metadata, sections=sections)


def _load_tasks(*, status: str | None = None, epic: str | None = None) -> list[PMDocument]:
    base = PM_ROOT / "tasks"
    if not base.exists():
        return []
    documents: list[PMDocument] = []
    for path in sorted(base.glob("*/*.md")):
        document = _read_document(path)
        if status and document.metadata.get("status") != status:
            continue
        if epic and document.metadata.get("epic") != epic:
            continue
        documents.append(document)
    return _sort_tasks(documents)


def _sort_tasks(documents: list[PMDocument]) -> list[PMDocument]:
    return sorted(
        documents,
        key=lambda item: (
            item.metadata.get("epic", ""),
            _status_rank(item.metadata.get("status", "backlog")),
            int(item.metadata.get("issue", "999999")) if item.metadata.get("issue", "").isdigit() else 999999,
            item.metadata.get("title", ""),
            str(item.path),
        ),
    )


def _status_rank(status: str) -> int:
    try:
        return VALID_STATUSES.index(status)
    except ValueError:
        return len(VALID_STATUSES)


def _doc_to_dict(document: PMDocument) -> dict[str, object]:
    return {
        "path": str(document.path),
        "title": document.metadata.get("title", ""),
        "status": document.metadata.get("status", ""),
        "epic": document.metadata.get("epic", ""),
        "issue": document.metadata.get("issue"),
        "labels": [item for item in document.metadata.get("labels", "").split(",") if item],
    }


def _print_tasks(documents: list[PMDocument], as_json: bool) -> int:
    if as_json:
        print(json.dumps([_doc_to_dict(document) for document in documents], ensure_ascii=True, indent=2, sort_keys=True))
        return 0
    for document in documents:
        issue = document.metadata.get("issue")
        issue_suffix = f" issue=#{issue}" if issue else ""
        print(f"{document.path} status={document.metadata.get('status', 'backlog')}{issue_suffix}")
    return 0


def _render_issue_body(document: PMDocument) -> str:
    lines = []
    context = document.sections.get("Context", "")
    deliverable = document.sections.get("Deliverable", "")
    scope = document.sections.get("Scope", "")
    acceptance = document.sections.get("Acceptance Criteria", "")

    if context:
        lines.extend(["## Context", context, ""])
    if deliverable:
        lines.extend(["## Deliverable", deliverable, ""])
    if scope:
        lines.extend(["## Scope", scope, ""])
    if acceptance:
        lines.extend(["## Acceptance Criteria", acceptance, ""])
    labels = document.metadata.get("labels", "")
    if labels:
        lines.extend(["## Labels", labels, ""])
    return "\n".join(lines).rstrip()


def _render_pr_body(document: PMDocument, *, issue: int | None, tests: list[str]) -> str:
    lines: list[str] = []
    closing_issue = issue or _parse_issue_number(document.metadata.get("issue", ""))
    if closing_issue is not None:
        lines.extend([f"Closes #{closing_issue}", ""])
    deliverable = document.sections.get("Deliverable", "")
    implementation_notes = document.sections.get("Implementation Notes", "")
    validation = document.sections.get("Validation", "")
    if deliverable:
        lines.extend([deliverable, ""])
    if implementation_notes:
        lines.extend(["Implementation notes:", implementation_notes, ""])
    if validation or tests:
        lines.append("Validation:")
        if validation:
            lines.extend(validation.splitlines())
        for test in tests:
            lines.append(f"- `{test}`")
    return "\n".join(lines).rstrip()


def _parse_issue_number(value: str) -> int | None:
    if value.isdigit():
        return int(value)
    return None


if __name__ == "__main__":
    run()
