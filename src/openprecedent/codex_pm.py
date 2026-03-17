from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


PM_ROOT = Path(".codex/pm")
ISSUE_STATE_ROOT = PM_ROOT / "issue-state"
VALID_STATUSES = ("backlog", "in_progress", "blocked", "done")
VALID_TASK_TYPES = ("implementation", "docs", "research", "umbrella")
PLACEHOLDER_COMMENT = "<!-- TODO: fill in -->"
CLOSING_ISSUE_PATTERN = re.compile(
    r"\b(?:close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s+#(\d+)\b",
    re.IGNORECASE,
)
GITHUB_REMOTE_PATTERN = re.compile(r"github\.com[:/]([^/]+)/([^/.]+?)(?:\.git)?$")
GITHUB_ISSUE_URL_PATTERN = re.compile(r"/issues/(\d+)(?:\b|$)")


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
    task_new.add_argument("--task-type", default="implementation", choices=VALID_TASK_TYPES)
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

    issue_state_init = subparsers.add_parser("issue-state-init")
    issue_state_init.add_argument("path")

    issue_state_show = subparsers.add_parser("issue-state-show")
    issue_state_show.add_argument("path")

    issue_state_check = subparsers.add_parser("issue-state-check")
    issue_state_check.add_argument("--branch")
    reconcile_task_statuses = subparsers.add_parser("reconcile-task-statuses")
    reconcile_task_statuses.add_argument("--issue", action="append", type=int, default=[])
    reconcile_task_statuses.add_argument("--apply", action="store_true")
    reconcile_task_statuses.add_argument("--json", action="store_true", dest="as_json")

    subparsers.add_parser("standup").add_argument("--json", action="store_true", dest="as_json")
    session_start = subparsers.add_parser("session-start")
    session_start.add_argument("--branch")
    session_start.add_argument("--json", action="store_true", dest="as_json")

    issue_body = subparsers.add_parser("issue-body")
    issue_body.add_argument("path")

    issue_create = subparsers.add_parser("issue-create")
    issue_create.add_argument("path")
    issue_create.add_argument("--title")
    issue_create.add_argument("--repo", default="openprecedent/openprecedent")

    pr_body = subparsers.add_parser("pr-body")
    pr_body.add_argument("path")
    pr_body.add_argument("--issue", type=int)
    pr_body.add_argument("--tests", action="append", default=[])

    pr_create = subparsers.add_parser("pr-create")
    pr_create.add_argument("path")
    pr_create.add_argument("--issue", type=int)
    pr_create.add_argument("--tests", action="append", default=[])
    pr_create.add_argument("--title")
    pr_create.add_argument("--base-repo", default="openprecedent/openprecedent")
    pr_create.add_argument("--base-branch", default="main")
    pr_create.add_argument("--head-owner")
    pr_create.add_argument("--head-branch")

    verify_pr_closure = subparsers.add_parser("verify-pr-closure-sync")
    verify_pr_closure.add_argument("--pr-body")
    verify_pr_closure.add_argument("--event-path")
    verify_pr_closure.add_argument("--changed-file", action="append", default=[])
    verify_pr_closure.add_argument("--base-sha")
    verify_pr_closure.add_argument("--head-sha")

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
            "task_type": args.task_type,
            "labels": args.labels,
            "depends_on": args.depends_on,
        }
        if args.issue:
            metadata["issue"] = args.issue
        _write_document(
            path,
            metadata=metadata,
            sections={
                "Context": PLACEHOLDER_COMMENT,
                "Deliverable": PLACEHOLDER_COMMENT,
                "Scope": PLACEHOLDER_COMMENT,
                "Acceptance Criteria": PLACEHOLDER_COMMENT,
                "Validation": PLACEHOLDER_COMMENT,
                "Implementation Notes": PLACEHOLDER_COMMENT,
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
    if args.action == "issue-state-init":
        document = _read_document(Path(args.path))
        state_document = _init_issue_state(document)
        print(state_document.path)
        return 0
    if args.action == "issue-state-show":
        document = _read_document(Path(args.path))
        state_document = _load_issue_state(document)
        if state_document is None:
            print("No issue state document found for task.", file=sys.stderr)
            return 1
        print(state_document.path)
        print()
        print(state_document.path.read_text(encoding="utf-8").rstrip())
        return 0
    if args.action == "issue-state-check":
        branch = args.branch or _current_branch()
        result = _check_issue_state(branch)
        if result is None:
            print("Issue state check skipped: current branch is not issue-scoped.")
            return 0
        ok, message = result
        stream = sys.stdout if ok else sys.stderr
        print(message, file=stream)
        return 0 if ok else 1
    if args.action == "reconcile-task-statuses":
        result = _reconcile_task_statuses(issue_numbers=args.issue, apply=args.apply)
        if args.as_json:
            print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True))
        else:
            print(_render_task_reconciliation(result))
        return 0 if not result["errors"] else 1
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
    if args.action == "session-start":
        summary = _build_session_start_summary(args.branch or _current_branch())
        if args.as_json:
            print(json.dumps(summary, ensure_ascii=True, indent=2, sort_keys=True))
        else:
            print(_render_session_start_summary(summary))
        return 0
    if args.action == "issue-body":
        document = _read_document(Path(args.path))
        print(_render_issue_body(document))
        return 0
    if args.action == "issue-create":
        document = _read_document(Path(args.path))
        try:
            issue_url = _create_issue(document, title=args.title, repo=args.repo)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        except subprocess.CalledProcessError as exc:
            message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
            print(message, file=sys.stderr)
            return exc.returncode or 1
        print(issue_url)
        return 0
    if args.action == "pr-body":
        document = _read_document(Path(args.path))
        print(_render_pr_body(document, issue=args.issue, tests=args.tests))
        return 0
    if args.action == "pr-create":
        document = _read_document(Path(args.path))
        try:
            pr_url = _create_pr(
                document,
                issue=args.issue,
                tests=args.tests,
                title=args.title,
                base_repo=args.base_repo,
                base_branch=args.base_branch,
                head_owner=args.head_owner,
                head_branch=args.head_branch,
            )
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        except subprocess.CalledProcessError as exc:
            message = exc.stderr.strip() or exc.stdout.strip() or str(exc)
            print(message, file=sys.stderr)
            return exc.returncode or 1
        print(pr_url)
        return 0
    if args.action == "verify-pr-closure-sync":
        pr_body = _resolve_pr_body(args.pr_body, args.event_path)
        changed_files = _resolve_changed_files(
            changed_files=args.changed_file,
            base_sha=args.base_sha,
            head_sha=args.head_sha,
        )
        errors = _verify_pr_closure_sync(pr_body, changed_files)
        if errors:
            for error in errors:
                print(error, file=sys.stderr)
            return 1
        print("PR task closure sync passed.")
        return 0

    parser.error("unknown action")
    return 2


def run() -> None:
    raise SystemExit(main())


def _init_pm() -> None:
    for name in ("prds", "epics", "tasks", "context", "updates", "issue-state"):
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
        "state_path": document.metadata.get("state_path"),
        "task_type": document.metadata.get("task_type", "implementation"),
        "labels": [item for item in document.metadata.get("labels", "").split(",") if item],
    }


def _build_session_start_summary(branch: str) -> dict[str, object]:
    issue = _parse_issue_from_branch(branch) if branch else None
    task = _find_task_by_issue(issue) if issue is not None else None
    issue_state = _load_issue_state(task) if task is not None else None
    pr_context = _pr_context_for_branch(branch)
    policies = [
        "When the user reports a concrete problem, directly diagnose, implement, verify, and close the loop unless blocked or high-risk.",
        "Prefer repository-local execution paths such as ./scripts/run-pytest.sh and the local .venv before treating missing global tools as blockers.",
        "Keep the issue, task twin, issue-state, and PR closure state synchronized before considering the work complete.",
    ]
    warnings: list[str] = []
    if issue is not None and task is None:
        warnings.append(f"No local task twin found for issue #{issue}.")
    if task is not None and task.metadata.get("status") == "in_progress" and issue_state is None:
        warnings.append(
            f"In-progress issue #{issue} has no issue-state document. Run `python3 -m openprecedent.codex_pm issue-state-init {task.path}`."
        )

    summary: dict[str, object] = {
        "branch": branch,
        "issue": issue,
        "task": _doc_to_dict(task) if task is not None else None,
        "issue_state": {
            "path": str(issue_state.path),
            "status": issue_state.metadata.get("status", ""),
        }
        if issue_state is not None
        else None,
        "pull_request": pr_context,
        "default_policies": policies,
        "warnings": warnings,
    }
    return summary


def _render_session_start_summary(summary: dict[str, object]) -> str:
    lines = [
        "Codex session-start summary",
        f"Branch: {summary.get('branch') or '(detached)'}",
    ]
    issue = summary.get("issue")
    lines.append(f"Issue: #{issue}" if issue is not None else "Issue: none detected from branch")

    task = summary.get("task")
    if isinstance(task, dict):
        lines.append(f"Task: {task.get('title')} ({task.get('path')})")
        lines.append(f"Task status: {task.get('status')}")
    else:
        lines.append("Task: no matching local task twin")

    issue_state = summary.get("issue_state")
    if isinstance(issue_state, dict):
        lines.append(f"Issue state: {issue_state.get('path')}")
    else:
        lines.append("Issue state: missing or not initialized")

    pull_request = summary.get("pull_request")
    if isinstance(pull_request, dict):
        lines.append(f"Pull request: #{pull_request.get('number')} {pull_request.get('title')} ({pull_request.get('url')})")
    else:
        lines.append("Pull request: none detected for the current branch")

    lines.extend(["", "Default execution policy:"])
    for item in summary.get("default_policies", []):
        lines.append(f"- {item}")

    warnings = summary.get("warnings", [])
    if warnings:
        lines.extend(["", "Warnings:"])
        for warning in warnings:
            lines.append(f"- {warning}")
    return "\n".join(lines)


def _current_branch() -> str:
    return _git_output(["git", "branch", "--show-current"]) or ""


def _git_output(args: list[str]) -> str | None:
    result = subprocess.run(
        args,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _parse_github_remote(remote_url: str) -> tuple[str, str] | None:
    match = GITHUB_REMOTE_PATTERN.search(remote_url)
    if match is None:
        return None
    return match.group(1), match.group(2)


def _repository_for_pr_lookup() -> str | None:
    for remote_name in ("upstream", "origin"):
        remote_url = _git_output(["git", "remote", "get-url", remote_name])
        if remote_url is None:
            continue
        parsed = _parse_github_remote(remote_url)
        if parsed is not None:
            return f"{parsed[0]}/{parsed[1]}"
    return None


def _pr_context_for_branch(branch: str) -> dict[str, object] | None:
    if not branch:
        return None
    repo = _repository_for_pr_lookup()
    origin_url = _git_output(["git", "remote", "get-url", "origin"])
    if repo is None or origin_url is None:
        return None
    parsed_origin = _parse_github_remote(origin_url)
    if parsed_origin is None:
        return None

    result = subprocess.run(
        [
            "gh",
            "pr",
            "list",
            "--repo",
            repo,
            "--head",
            f"{parsed_origin[0]}:{branch}",
            "--state",
            "open",
            "--json",
            "number,title,url",
            "--limit",
            "1",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    items = json.loads(result.stdout)
    if not items:
        return None
    pr = items[0]
    return {
        "number": pr.get("number"),
        "title": pr.get("title"),
        "url": pr.get("url"),
    }


def _parse_issue_from_branch(branch: str) -> int | None:
    match = re.search(r"\bissue-(\d+)\b", branch)
    if match is None:
        return None
    return int(match.group(1))


def _find_task_by_issue(issue: int) -> PMDocument | None:
    for document in _load_tasks():
        if _parse_issue_number(document.metadata.get("issue", "")) == issue:
            return document
    return None


def _issue_state_path(document: PMDocument) -> Path:
    issue = _parse_issue_number(document.metadata.get("issue", ""))
    if issue is None:
        raise ValueError(f"task has no numeric issue reference: {document.path}")
    slug = document.metadata.get("slug") or document.path.stem
    return ISSUE_STATE_ROOT / f"{issue}-{slug}.md"


def _init_issue_state(document: PMDocument) -> PMDocument:
    path = _issue_state_path(document)
    if not path.exists():
        _write_document(
            path,
            metadata={
                "type": "issue_state",
                "issue": document.metadata.get("issue", ""),
                "task": str(document.path),
                "title": document.metadata.get("title", ""),
                "status": document.metadata.get("status", ""),
            },
            sections={
                "Summary": "Record the current working state for this issue so later sessions do not have to rediscover it.",
                "Validated Facts": "- ",
                "Open Questions": "- ",
                "Next Steps": "- ",
                "Artifacts": "- ",
            },
        )
    document.metadata["state_path"] = str(path)
    _persist_document(document)
    return _read_document(path)


def _load_issue_state(document: PMDocument) -> PMDocument | None:
    state_path_value = document.metadata.get("state_path")
    candidate_paths: list[Path] = []
    if state_path_value:
        candidate_paths.append(Path(state_path_value))
    if document.metadata.get("issue", "").isdigit():
        candidate_paths.append(_issue_state_path(document))
    for path in candidate_paths:
        if path.exists():
            return _read_document(path)
    return None


def _check_issue_state(branch: str) -> tuple[bool, str] | None:
    issue = _parse_issue_from_branch(branch)
    if issue is None:
        return None
    task = _find_task_by_issue(issue)
    if task is None:
        return False, f"Issue state check failed: no task twin found for issue #{issue}."
    if task.metadata.get("status") != "in_progress":
        return True, f"Issue state check skipped: task for issue #{issue} is not in progress."
    state_document = _load_issue_state(task)
    if state_document is None:
        return (
            False,
            "Issue state check failed: in-progress issue has no state document. "
            f"Run `python3 -m openprecedent.codex_pm issue-state-init {task.path}`.",
        )
    return True, f"Issue state check passed: {state_document.path}"


def _print_tasks(documents: list[PMDocument], as_json: bool) -> int:
    if as_json:
        print(json.dumps([_doc_to_dict(document) for document in documents], ensure_ascii=True, indent=2, sort_keys=True))
        return 0
    for document in documents:
        issue = document.metadata.get("issue")
        issue_suffix = f" issue=#{issue}" if issue else ""
        print(f"{document.path} status={document.metadata.get('status', 'backlog')}{issue_suffix}")
    return 0


def _render_issue_body(document: PMDocument, *, include_labels: bool = True) -> str:
    lines = []
    context = _renderable_section_body(document.sections.get("Context", ""))
    deliverable = _renderable_section_body(document.sections.get("Deliverable", ""))
    scope = _renderable_section_body(document.sections.get("Scope", ""))
    acceptance = _renderable_section_body(document.sections.get("Acceptance Criteria", ""))
    task_type = document.metadata.get("task_type", "")

    if context:
        lines.extend(["## Context", context, ""])
    if deliverable:
        lines.extend(["## Deliverable", deliverable, ""])
    if scope:
        lines.extend(["## Scope", scope, ""])
    if acceptance:
        lines.extend(["## Acceptance Criteria", acceptance, ""])
    if task_type:
        lines.extend(["## Task Type", task_type, ""])
    labels = document.metadata.get("labels", "")
    if include_labels and labels:
        lines.extend(["## Labels", labels, ""])
    return "\n".join(lines).rstrip()


def _render_pr_body(document: PMDocument, *, issue: int | None, tests: list[str]) -> str:
    lines: list[str] = []
    closing_issue = issue or _parse_issue_number(document.metadata.get("issue", ""))
    task_type = document.metadata.get("task_type", "implementation")
    if closing_issue is not None and task_type != "umbrella":
        lines.extend([f"Closes #{closing_issue}", ""])
    deliverable = _renderable_section_body(document.sections.get("Deliverable", ""))
    implementation_notes = _renderable_section_body(document.sections.get("Implementation Notes", ""))
    validation = _renderable_section_body(document.sections.get("Validation", ""))
    if deliverable:
        lines.extend([deliverable, ""])
    if implementation_notes:
        lines.extend(["Implementation notes:", implementation_notes, ""])
    if validation or tests:
        lines.append("Validation:")
        if validation:
            for line in validation.splitlines():
                stripped = line.strip()
                if not stripped or stripped == "-":
                    continue
                lines.append(line)
        for test in tests:
            lines.append(f"- `{test}`")
    return "\n".join(lines).rstrip()


def _renderable_section_body(body: str) -> str:
    stripped = body.strip()
    if not stripped or stripped == PLACEHOLDER_COMMENT:
        return ""
    return body


def _remote_issue_states(issue_numbers: list[int]) -> tuple[dict[int, str], list[str]]:
    unique_issues = sorted(set(issue_numbers))
    if not unique_issues:
        return {}, []

    result = subprocess.run(
        [
            "gh",
            "issue",
            "list",
            "--repo",
            "openprecedent/openprecedent",
            "--state",
            "all",
            "--limit",
            str(max(200, len(unique_issues))),
            "--json",
            "number,state",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "failed to query GitHub issues"
        return {}, [f"Task reconciliation failed: {message}"]

    items = json.loads(result.stdout or "[]")
    state_map = {
        int(item["number"]): str(item["state"]).upper()
        for item in items
        if isinstance(item.get("number"), int) and item.get("state")
    }
    missing = [issue for issue in unique_issues if issue not in state_map]
    errors = [f"Task reconciliation failed: remote issue #{issue} was not returned by gh issue list." for issue in missing]
    return state_map, errors


def _reconcile_task_statuses(*, issue_numbers: list[int], apply: bool) -> dict[str, object]:
    documents = [
        document
        for document in _load_tasks()
        if document.metadata.get("issue", "").isdigit()
        and (not issue_numbers or _parse_issue_number(document.metadata.get("issue", "")) in issue_numbers)
    ]
    target_issue_numbers = [
        _parse_issue_number(document.metadata.get("issue", ""))
        for document in documents
        if _parse_issue_number(document.metadata.get("issue", "")) is not None
    ]
    remote_states, errors = _remote_issue_states(target_issue_numbers)
    findings: list[dict[str, object]] = []

    for document in documents:
        issue = _parse_issue_number(document.metadata.get("issue", ""))
        if issue is None:
            continue
        remote_state = remote_states.get(issue)
        if remote_state is None:
            continue
        local_status = document.metadata.get("status", "backlog")
        expected_status = "done" if remote_state == "CLOSED" else None
        drift_reason = None
        if expected_status == "done" and local_status != "done":
            drift_reason = "remote issue is closed but local task is not done"
            if apply:
                document.metadata["status"] = "done"
                _persist_document(document)
                local_status = "done"
        elif remote_state == "OPEN" and local_status == "done":
            drift_reason = "remote issue is still open but local task is marked done"

        if drift_reason is not None:
            findings.append(
                {
                    "issue": issue,
                    "path": str(document.path),
                    "remote_state": remote_state,
                    "local_status": local_status,
                    "expected_status": expected_status,
                    "drift_reason": drift_reason,
                    "applied": apply and expected_status == "done",
                }
            )

    return {
        "checked_tasks": len(documents),
        "findings": findings,
        "errors": errors,
    }


def _render_task_reconciliation(result: dict[str, object]) -> str:
    lines = [f"Checked tasks: {result['checked_tasks']}"]
    for finding in result["findings"]:
        status_note = "reconciled" if finding.get("applied") else "drift detected"
        lines.append(
            f"- issue #{finding['issue']} {status_note}: {finding['drift_reason']} ({finding['path']})"
        )
    for error in result["errors"]:
        lines.append(f"- {error}")
    if not result["findings"] and not result["errors"]:
        lines.append("- no task status drift detected")
    return "\n".join(lines)


def _assert_task_ready_for_pr(document: PMDocument, closing_issue: int | None) -> None:
    task_type = document.metadata.get("task_type", "implementation")
    if closing_issue is None or task_type == "umbrella":
        return
    if document.metadata.get("status") != "done":
        raise ValueError(
            "PR creation failed: matching task twin must be marked done before creating a PR that closes "
            f"#{closing_issue}. Update {document.path} first."
        )


def _create_pr(
    document: PMDocument,
    *,
    issue: int | None,
    tests: list[str],
    title: str | None,
    base_repo: str,
    base_branch: str,
    head_owner: str | None,
    head_branch: str | None,
) -> str:
    closing_issue = issue or _parse_issue_number(document.metadata.get("issue", ""))
    _assert_task_ready_for_pr(document, closing_issue)
    branch = head_branch or _current_branch()
    if not branch:
        raise ValueError("PR creation failed: current branch is unavailable.")

    origin_url = _git_output(["git", "remote", "get-url", "origin"])
    if head_owner is None:
        if origin_url is None:
            raise ValueError("PR creation failed: origin remote is unavailable.")
        origin_remote = _parse_github_remote(origin_url)
        if origin_remote is None:
            raise ValueError(
                "PR creation failed: could not derive the fork owner from the origin remote. "
                "Pass --head-owner explicitly."
            )
        head_owner = origin_remote[0]

    upstream_url = _git_output(["git", "remote", "get-url", "upstream"])
    if upstream_url is not None:
        upstream_remote = _parse_github_remote(upstream_url)
        if upstream_remote is None:
            raise ValueError(
                "PR creation failed: could not parse the upstream remote. "
                "Fix the upstream remote or pass --base-repo explicitly."
            )
        upstream_repo = f"{upstream_remote[0]}/{upstream_remote[1]}"
        if upstream_repo != base_repo:
            raise ValueError(
                f"PR creation failed: upstream remote points to {upstream_repo}, not {base_repo}. "
                "Use the intended upstream repository explicitly."
            )

    pr_title = title or document.metadata.get("title") or document.path.stem
    pr_body = _render_pr_body(document, issue=issue, tests=tests)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
        handle.write(pr_body)
        body_path = Path(handle.name)

    try:
        result = subprocess.run(
            [
                "gh",
                "pr",
                "create",
                "--repo",
                base_repo,
                "--base",
                base_branch,
                "--head",
                f"{head_owner}:{branch}",
                "--title",
                pr_title,
                "--body-file",
                str(body_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    finally:
        body_path.unlink(missing_ok=True)


def _create_issue(document: PMDocument, *, title: str | None, repo: str) -> str:
    issue_title = title or document.metadata.get("title") or document.path.stem
    issue_body = _render_issue_body(document, include_labels=False)
    labels = [item.strip() for item in document.metadata.get("labels", "").split(",") if item.strip()]

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
        handle.write(issue_body)
        body_path = Path(handle.name)

    try:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "create",
                "--repo",
                repo,
                "--title",
                issue_title,
                "--body-file",
                str(body_path),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        issue_url = result.stdout.strip()
    finally:
        body_path.unlink(missing_ok=True)

    issue_number = _parse_issue_number_from_url(issue_url)
    if issue_number is None:
        raise ValueError(f"Issue creation failed: could not parse the created issue number from `{issue_url}`.")

    for label in labels:
        subprocess.run(
            [
                "gh",
                "issue",
                "edit",
                str(issue_number),
                "--repo",
                repo,
                "--add-label",
                label,
            ],
            check=True,
            capture_output=True,
            text=True,
        )

    return issue_url


def _parse_issue_number(value: str) -> int | None:
    if value.isdigit():
        return int(value)
    return None


def _parse_issue_number_from_url(value: str) -> int | None:
    match = GITHUB_ISSUE_URL_PATTERN.search(value)
    if match is None:
        return None
    return int(match.group(1))


def _resolve_pr_body(pr_body: str | None, event_path: str | None) -> str:
    if pr_body is not None:
        return pr_body
    if event_path is not None:
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
        return event.get("pull_request", {}).get("body") or ""
    raise ValueError("either --pr-body or --event-path is required")


def _resolve_changed_files(
    *,
    changed_files: list[str],
    base_sha: str | None,
    head_sha: str | None,
) -> list[str]:
    if changed_files:
        return changed_files
    if base_sha and head_sha:
        result = subprocess.run(
            ["git", "diff", "--name-only", base_sha, head_sha],
            check=True,
            capture_output=True,
            text=True,
        )
        return [line for line in result.stdout.splitlines() if line]
    raise ValueError("either --changed-file or both --base-sha and --head-sha are required")


def _verify_pr_closure_sync(pr_body: str, changed_files: list[str]) -> list[str]:
    closing_issues = sorted({int(match) for match in CLOSING_ISSUE_PATTERN.findall(pr_body)})
    if not closing_issues:
        return []

    changed_task_paths = [
        Path(path)
        for path in changed_files
        if path.startswith(".codex/pm/tasks/") and path.endswith(".md") and Path(path).exists()
    ]
    changed_task_documents = [_read_document(path) for path in changed_task_paths]

    errors: list[str] = []
    for issue in closing_issues:
        matching_documents = [
            document
            for document in changed_task_documents
            if _parse_issue_number(document.metadata.get("issue", "")) == issue
        ]
        if not matching_documents:
            errors.append(
                f"PR closes #{issue} but does not update the matching local task file under .codex/pm/tasks/."
            )
            continue
        umbrella_paths = ", ".join(
            str(document.path)
            for document in matching_documents
            if document.metadata.get("task_type", "implementation") == "umbrella"
        )
        if umbrella_paths:
            errors.append(
                f"PR closes #{issue} but matching task file is task_type=umbrella and must remain open: {umbrella_paths}"
            )
            continue
        if not any(document.metadata.get("status") == "done" for document in matching_documents):
            matching_paths = ", ".join(str(document.path) for document in matching_documents)
            errors.append(
                f"PR closes #{issue} but matching task file is not marked done: {matching_paths}"
            )
    return errors


if __name__ == "__main__":
    run()
