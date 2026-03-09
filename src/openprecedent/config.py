from __future__ import annotations

import os
from pathlib import Path


DEFAULT_DB_NAME = "openprecedent.db"
DB_ENV_VAR = "OPENPRECEDENT_DB"


def get_db_path() -> Path:
    configured = os.environ.get(DB_ENV_VAR)
    if configured:
        return Path(configured).expanduser().resolve()

    return Path.cwd() / DEFAULT_DB_NAME
