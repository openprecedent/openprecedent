#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def classify_coverage(value: float) -> str:
    if value >= 90:
        return "high"
    if value >= 75:
        return "medium"
    return "low"


def format_percent(value: float) -> str:
    return f"{value:.1f}%"


def load_python_summary(path: Path) -> list[tuple[str, float, int, int]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    totals = payload.get("totals", {})
    return [
        (
            "Lines",
            float(totals.get("percent_covered", 0)),
            int(totals.get("covered_lines", 0)),
            int(totals.get("num_statements", 0)),
        ),
        (
            "Statements",
            float(totals.get("percent_statements_covered", 0)),
            int(totals.get("covered_lines", 0)),
            int(totals.get("num_statements", 0)),
        ),
        (
            "Branches",
            float(totals.get("percent_branches_covered", 0)),
            int(totals.get("covered_branches", 0)),
            int(totals.get("num_branches", 0)),
        ),
    ]


def load_rust_summary(path: Path) -> list[tuple[str, float, int, int]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    totals = payload.get("data", [{}])[0].get("totals", {})
    metrics: list[tuple[str, float, int, int]] = []
    for label, key in (("Lines", "lines"), ("Functions", "functions"), ("Regions", "regions")):
        metric = totals.get(key, {})
        count = int(metric.get("count", 0))
        covered = int(metric.get("covered", 0))
        percent = float(metric.get("percent", (covered / count * 100.0) if count else 0.0))
        metrics.append((label, percent, covered, count))
    return metrics


def render_table(title: str, metrics: list[tuple[str, float, int, int]]) -> list[str]:
    lines = [
        f"### {title}",
        "",
        "| Metric | Coverage | Covered / Total | Level |",
        "| --- | ---: | ---: | --- |",
    ]
    for label, percent, covered, total in metrics:
        lines.append(
            f"| {label} | {format_percent(percent)} | {covered} / {total} | {classify_coverage(percent)} |"
        )
    lines.append("")
    return lines


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print(
            "Usage: python3 scripts/render_coverage_summary.py <python-coverage.json> <rust-coverage-summary.json>",
            file=sys.stderr,
        )
        return 1

    python_path = Path(argv[0]).resolve()
    rust_path = Path(argv[1]).resolve()

    for path in (python_path, rust_path):
        if not path.exists():
            print(f"Coverage summary not found: {path}", file=sys.stderr)
            return 1

    lines = ["## Test Coverage", ""]
    lines.extend(render_table("Python", load_python_summary(python_path)))
    lines.extend(render_table("Rust", load_rust_summary(rust_path)))
    sys.stdout.write("\n".join(lines).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
