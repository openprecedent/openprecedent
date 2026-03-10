from __future__ import annotations

import os
from pathlib import Path


DEFAULT_DB_NAME = "openprecedent.db"
HOME_ENV_VAR = "OPENPRECEDENT_HOME"
DB_ENV_VAR = "OPENPRECEDENT_DB"
DEFAULT_COLLECTOR_STATE_NAME = "openprecedent-collector-state.json"
COLLECTOR_STATE_ENV_VAR = "OPENPRECEDENT_COLLECTOR_STATE"
DEFAULT_RUNTIME_INVOCATION_LOG_NAME = "openprecedent-runtime-invocations.jsonl"
RUNTIME_INVOCATION_LOG_ENV_VAR = "OPENPRECEDENT_RUNTIME_INVOCATION_LOG"


def get_home_path() -> Path | None:
    configured = os.environ.get(HOME_ENV_VAR)
    if configured:
        return Path(configured).expanduser().resolve()

    return None


def get_db_path() -> Path:
    configured = os.environ.get(DB_ENV_VAR)
    if configured:
        return Path(configured).expanduser().resolve()

    home_path = get_home_path()
    if home_path is not None:
        return home_path / DEFAULT_DB_NAME

    return Path.cwd() / DEFAULT_DB_NAME


def get_collector_state_path() -> Path:
    configured = os.environ.get(COLLECTOR_STATE_ENV_VAR)
    if configured:
        return Path(configured).expanduser().resolve()

    home_path = get_home_path()
    if home_path is not None:
        return home_path / DEFAULT_COLLECTOR_STATE_NAME

    return get_db_path().with_name(DEFAULT_COLLECTOR_STATE_NAME)


def get_runtime_invocation_log_path() -> Path:
    configured = os.environ.get(RUNTIME_INVOCATION_LOG_ENV_VAR)
    if configured:
        return Path(configured).expanduser().resolve()

    home_path = get_home_path()
    if home_path is not None:
        return home_path / DEFAULT_RUNTIME_INVOCATION_LOG_NAME

    return get_db_path().with_name(DEFAULT_RUNTIME_INVOCATION_LOG_NAME)
