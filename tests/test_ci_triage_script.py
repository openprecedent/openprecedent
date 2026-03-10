from __future__ import annotations

import importlib.util
from pathlib import Path


def _load_module():
    script_path = Path(__file__).parent.parent / "scripts" / "triage_pr_checks.py"
    spec = importlib.util.spec_from_file_location("triage_pr_checks", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_triage_pr_checks_classifies_known_failures() -> None:
    module = _load_module()

    classified = module._classify(
        {
            "name": "python-ci",
            "status": "COMPLETED",
            "conclusion": "FAILURE",
            "detailsUrl": "https://example.invalid/python-ci",
        }
    )

    assert classified["category"] == "test_regression"
    assert classified["is_failure"] is True


def test_triage_pr_checks_renders_text_summary() -> None:
    module = _load_module()

    rendered = module._render_text(
        [
            {
                "name": "python-ci",
                "category": "test_regression",
                "guidance": "Inspect failing pytest output.",
                "details_url": "https://example.invalid/python-ci",
                "is_failure": True,
            },
            {
                "name": "markdownlint",
                "category": "docs_lint",
                "guidance": "Inspect markdown formatting.",
                "details_url": "https://example.invalid/markdownlint",
                "is_failure": False,
            },
        ]
    )

    assert "Failing checks:" in rendered
    assert "python-ci [test_regression]" in rendered
    assert "Passing checks:" in rendered
    assert "markdownlint [docs_lint]" in rendered
