from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_run_pytest_script_prefers_repo_python(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env["OPENPRECEDENT_PYTHON_BIN"] = sys.executable
    env["OPENPRECEDENT_VENV_PYTHON"] = sys.executable
    env["OPENPRECEDENT_VENV_PYTEST"] = str(tmp_path / "missing-pytest")
    env["OPENPRECEDENT_SYSTEM_PYTHON"] = "missing-python3"
    env["OPENPRECEDENT_ALT_SYSTEM_PYTHON"] = "missing-python"
    env["OPENPRECEDENT_SYSTEM_PYTEST"] = "missing-pytest"
    env["PATH"] = "/usr/bin:/bin"
    env["PYTHONPATH"] = str(repo_root / "src")

    result = subprocess.run(
        ["./scripts/run-pytest.sh", "-q", "tests/test_preflight_script.py"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "3 passed" in result.stdout


def test_run_pytest_script_fails_with_clear_message_when_no_runner_exists(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    env = os.environ.copy()
    env["OPENPRECEDENT_PYTHON_BIN"] = str(tmp_path / "missing-python")
    env["OPENPRECEDENT_VENV_PYTHON"] = str(tmp_path / "missing-venv-python")
    env["OPENPRECEDENT_VENV_PYTEST"] = str(tmp_path / "missing-venv-pytest")
    env["OPENPRECEDENT_SYSTEM_PYTHON"] = "missing-python3"
    env["OPENPRECEDENT_ALT_SYSTEM_PYTHON"] = "missing-python"
    env["OPENPRECEDENT_SYSTEM_PYTEST"] = "missing-pytest"

    result = subprocess.run(
        ["/bin/bash", "./scripts/run-pytest.sh", "-q", "tests/test_preflight_script.py"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Unable to locate a usable pytest runner." in result.stderr
    assert "./scripts/run-pytest.sh <pytest args>" in result.stderr
