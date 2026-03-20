from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_render_coverage_summary_usage_error() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/render_coverage_summary.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Usage: python3 scripts/render_coverage_summary.py" in result.stderr


def test_render_coverage_summary_renders_python_and_rust_tables(tmp_path: Path) -> None:
    python_summary = tmp_path / "python-coverage.json"
    rust_summary = tmp_path / "rust-coverage-summary.json"

    python_summary.write_text(
        json.dumps(
            {
                "totals": {
                    "percent_covered": 92.5,
                    "covered_lines": 185,
                    "num_statements": 200,
                    "percent_statements_covered": 92.5,
                    "percent_branches_covered": 80.0,
                    "covered_branches": 40,
                    "num_branches": 50,
                }
            }
        ),
        encoding="utf-8",
    )
    rust_summary.write_text(
        json.dumps(
            {
                "data": [
                    {
                        "totals": {
                            "lines": {"count": 120, "covered": 108},
                            "functions": {"count": 50, "covered": 45},
                            "regions": {"count": 150, "covered": 135},
                        }
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "scripts/render_coverage_summary.py", str(python_summary), str(rust_summary)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "## Test Coverage" in result.stdout
    assert "### Python" in result.stdout
    assert "| Lines | 92.5% | 185 / 200 | high |" in result.stdout
    assert "| Statements | 92.5% | 185 / 200 | high |" in result.stdout
    assert "| Branches | 80.0% | 40 / 50 | medium |" in result.stdout
    assert "### Rust" in result.stdout
    assert "| Functions | 90.0% | 45 / 50 | high |" in result.stdout


def test_render_coverage_summary_fails_when_a_summary_is_missing(tmp_path: Path) -> None:
    python_summary = tmp_path / "python-coverage.json"
    python_summary.write_text(json.dumps({"totals": {}}), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "scripts/render_coverage_summary.py",
            str(python_summary),
            str(tmp_path / "missing-rust.json"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Coverage summary not found:" in result.stderr


def test_check_mvp_coverage_gate_accepts_release_surface_threshold(tmp_path: Path) -> None:
    python_summary = tmp_path / "python-coverage.json"
    rust_summary = tmp_path / "rust-coverage-summary.json"

    python_summary.write_text(
        json.dumps(
            {
                "files": {
                    "src/openprecedent/services.py": {
                        "summary": {"covered_lines": 900, "num_statements": 1000}
                    },
                    "src/openprecedent/config.py": {
                        "summary": {"covered_lines": 45, "num_statements": 45}
                    },
                    "src/openprecedent/codex_pm.py": {
                        "summary": {"covered_lines": 0, "num_statements": 1000}
                    },
                }
            }
        ),
        encoding="utf-8",
    )
    rust_summary.write_text(
        json.dumps(
            {
                "data": [
                    {
                        "files": [
                            {
                                "filename": str(
                                    (ROOT / "rust" / "openprecedent-core" / "src" / "lib.rs").resolve()
                                ),
                                "summary": {"lines": {"covered": 91, "count": 100}},
                            },
                            {
                                "filename": str(
                                    (ROOT / "rust" / "openprecedent-cli" / "src" / "main.rs").resolve()
                                ),
                                "summary": {"lines": {"covered": 0, "count": 1000}},
                            },
                        ]
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_mvp_coverage_gate.py",
            str(python_summary),
            str(rust_summary),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "PASS: MVP release coverage gate satisfied." in result.stdout


def test_check_mvp_coverage_gate_reports_release_surface_failure(tmp_path: Path) -> None:
    python_summary = tmp_path / "python-coverage.json"
    rust_summary = tmp_path / "rust-coverage-summary.json"

    python_summary.write_text(
        json.dumps(
            {
                "files": {
                    "src/openprecedent/services.py": {
                        "summary": {"covered_lines": 89, "num_statements": 100}
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    rust_summary.write_text(
        json.dumps(
            {
                "data": [
                    {
                        "files": [
                            {
                                "filename": str(
                                    (ROOT / "rust" / "openprecedent-core" / "src" / "lib.rs").resolve()
                                ),
                                "summary": {"lines": {"covered": 90, "count": 100}},
                            }
                        ]
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "scripts/check_mvp_coverage_gate.py",
            str(python_summary),
            str(rust_summary),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Python MVP release surface is below threshold" in result.stderr
