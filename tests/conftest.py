from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def db_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "openprecedent.db"
    monkeypatch.setenv("OPENPRECEDENT_DB", str(path))
    return path
