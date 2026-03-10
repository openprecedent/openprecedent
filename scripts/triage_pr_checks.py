#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess


KNOWN_CHECKS: dict[str, tuple[str, str]] = {
    "python-ci": ("test_regression", "Inspect failing pytest output and rerun the relevant local test subset."),
    "markdownlint": ("docs_lint", "Inspect Markdown formatting and rerun the relevant local doc or lint checks."),
    "pr-review-gate": ("workflow_policy", "Check PR approvals and issue/task closure-sync state."),
    "feishu-pr-notify": ("notification", "Notification-only check; inspect only if delivery signaling matters."),
}


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="triage-pr-checks")
    parser.add_argument("--pr", help="PR number, URL, or branch. Defaults to current branch PR.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def _load_rollup(pr: str | None) -> list[dict[str, object]]:
    command = ["gh", "pr", "view", "--json", "statusCheckRollup"]
    if pr:
        command[3:3] = [pr]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(result.stdout)
    return payload.get("statusCheckRollup", [])


def _classify(entry: dict[str, object]) -> dict[str, object]:
    name = str(entry.get("name", ""))
    status = str(entry.get("status", ""))
    conclusion = str(entry.get("conclusion", ""))
    details_url = str(entry.get("detailsUrl", ""))
    category, guidance = KNOWN_CHECKS.get(
        name,
        ("unknown", "Inspect the linked check details and classify whether it is a test, policy, or external failure."),
    )
    return {
        "name": name,
        "status": status,
        "conclusion": conclusion,
        "category": category,
        "guidance": guidance,
        "details_url": details_url,
        "is_failure": conclusion.lower() == "failure",
    }


def _render_text(entries: list[dict[str, object]]) -> str:
    if not entries:
        return "No PR checks found."

    lines: list[str] = []
    failures = [entry for entry in entries if entry["is_failure"]]
    passes = [entry for entry in entries if not entry["is_failure"]]

    if failures:
        lines.append("Failing checks:")
        for entry in failures:
            lines.append(
                f"- {entry['name']} [{entry['category']}]: {entry['guidance']} ({entry['details_url']})"
            )
    else:
        lines.append("No failing checks.")

    if passes:
        lines.append("")
        lines.append("Passing checks:")
        for entry in passes:
            lines.append(f"- {entry['name']} [{entry['category']}]")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    entries = [_classify(entry) for entry in _load_rollup(args.pr)]
    if args.as_json:
        print(json.dumps(entries, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        print(_render_text(entries))
    return 1 if any(entry["is_failure"] for entry in entries) else 0


if __name__ == "__main__":
    raise SystemExit(main())
