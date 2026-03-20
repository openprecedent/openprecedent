from __future__ import annotations

from pathlib import Path

from openprecedent import config


def test_get_home_path_uses_env(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv(config.HOME_ENV_VAR, str(tmp_path / "runtime-home"))

    assert config.get_home_path() == (tmp_path / "runtime-home").resolve()


def test_get_home_path_returns_none_without_env(monkeypatch) -> None:
    monkeypatch.delenv(config.HOME_ENV_VAR, raising=False)

    assert config.get_home_path() is None


def test_get_db_path_falls_back_to_current_workdir(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv(config.DB_ENV_VAR, raising=False)
    monkeypatch.delenv(config.HOME_ENV_VAR, raising=False)
    monkeypatch.chdir(tmp_path)

    assert config.get_db_path() == tmp_path / config.DEFAULT_DB_NAME


def test_collector_and_invocation_paths_honor_env_overrides(monkeypatch, tmp_path: Path) -> None:
    collector_path = tmp_path / "collector-state.json"
    invocation_path = tmp_path / "runtime-invocations.jsonl"
    monkeypatch.setenv(config.COLLECTOR_STATE_ENV_VAR, str(collector_path))
    monkeypatch.setenv(config.RUNTIME_INVOCATION_LOG_ENV_VAR, str(invocation_path))

    assert config.get_collector_state_path() == collector_path.resolve()
    assert config.get_runtime_invocation_log_path() == invocation_path.resolve()


def test_collector_and_invocation_paths_derive_from_home(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv(config.COLLECTOR_STATE_ENV_VAR, raising=False)
    monkeypatch.delenv(config.RUNTIME_INVOCATION_LOG_ENV_VAR, raising=False)
    monkeypatch.setenv(config.HOME_ENV_VAR, str(tmp_path / "runtime-home"))

    home = (tmp_path / "runtime-home").resolve()
    assert config.get_collector_state_path() == home / config.DEFAULT_COLLECTOR_STATE_NAME
    assert config.get_runtime_invocation_log_path() == home / config.DEFAULT_RUNTIME_INVOCATION_LOG_NAME

