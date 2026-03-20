from __future__ import annotations

import json
import sys
from pathlib import Path


PYTHON_THRESHOLD = 90.0
RUST_THRESHOLD = 90.0
ROOT = Path(__file__).resolve().parent.parent
PYTHON_EXCLUDE = {"src/openprecedent/codex_pm.py"}
RUST_EXCLUDE = {"rust/openprecedent-cli/src/main.rs"}


def _load_json(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Coverage summary not found: {path}")
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _percent(covered: int, total: int) -> float:
    if total == 0:
        return 100.0
    return (covered / total) * 100


def _python_release_surface(summary: dict) -> tuple[int, int]:
    covered = 0
    total = 0
    for name, payload in summary["files"].items():
        if not name.startswith("src/openprecedent/"):
            continue
        if name in PYTHON_EXCLUDE:
            continue
        file_summary = payload["summary"]
        covered += file_summary["covered_lines"]
        total += file_summary["num_statements"]
    return covered, total


def _rust_release_surface(summary: dict) -> tuple[int, int]:
    covered = 0
    total = 0
    for payload in summary["data"][0]["files"]:
        filename = payload["filename"]
        relative = Path(filename).resolve().relative_to(ROOT)
        relative_str = relative.as_posix()
        if not relative_str.startswith("rust/"):
            continue
        if relative_str in RUST_EXCLUDE:
            continue
        file_summary = payload["summary"]["lines"]
        covered += file_summary["covered"]
        total += file_summary["count"]
    return covered, total


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(
            "Usage: python3 scripts/check_mvp_coverage_gate.py <python-coverage.json> <rust-coverage-summary.json>",
            file=sys.stderr,
        )
        return 1

    python_summary = _load_json(Path(argv[1]))
    rust_summary = _load_json(Path(argv[2]))

    python_covered, python_total = _python_release_surface(python_summary)
    rust_covered, rust_total = _rust_release_surface(rust_summary)

    python_percent = _percent(python_covered, python_total)
    rust_percent = _percent(rust_covered, rust_total)

    print("MVP release coverage gate")
    print(
        f"- Python release surface (excluding repo-local PM tooling): {python_percent:.1f}% ({python_covered} / {python_total})"
    )
    print(
        f"- Rust release implementation core (excluding CLI shell glue): {rust_percent:.1f}% ({rust_covered} / {rust_total})"
    )
    print(
        f"- Threshold: Python >= {PYTHON_THRESHOLD:.1f}%, Rust >= {RUST_THRESHOLD:.1f}%"
    )

    failures: list[str] = []
    if python_percent < PYTHON_THRESHOLD:
        failures.append(
            f"Python MVP release surface is below threshold: {python_percent:.1f}% < {PYTHON_THRESHOLD:.1f}%"
        )
    if rust_percent < RUST_THRESHOLD:
        failures.append(
            f"Rust MVP release implementation core is below threshold: {rust_percent:.1f}% < {RUST_THRESHOLD:.1f}%"
        )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print("PASS: MVP release coverage gate satisfied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
