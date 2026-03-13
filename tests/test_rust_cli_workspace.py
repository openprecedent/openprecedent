from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def test_rust_workspace_declares_expected_members() -> None:
    cargo_toml = (ROOT / "Cargo.toml").read_text(encoding="utf-8")

    for member in (
        'rust/openprecedent-cli',
        'rust/openprecedent-contracts',
        'rust/openprecedent-core',
        'rust/openprecedent-store-sqlite',
        'rust/openprecedent-capture-openclaw',
        'rust/openprecedent-capture-codex',
    ):
        assert f'"{member}"' in cargo_toml


def test_rust_cli_skeleton_declares_public_command_roots() -> None:
    main_rs = (ROOT / "rust" / "openprecedent-cli" / "src" / "main.rs").read_text(encoding="utf-8")

    for token in (
        "Case(",
        "Event(",
        "Decision(",
        "Replay(",
        "Precedent(",
        "Capture(",
        "Lineage(",
        "Eval(",
        "Doctor(",
        "Version",
    ):
        assert token in main_rs


def test_rust_cli_skeleton_uses_openprecedent_binary_name() -> None:
    cli_cargo_toml = (ROOT / "rust" / "openprecedent-cli" / "Cargo.toml").read_text(encoding="utf-8")
    contracts_rs = (ROOT / "rust" / "openprecedent-contracts" / "src" / "lib.rs").read_text(
        encoding="utf-8"
    )

    assert 'name = "openprecedent"' in cli_cargo_toml
    assert 'pub const CLI_BINARY_NAME: &str = "openprecedent";' in contracts_rs


def test_pyproject_no_longer_exposes_python_openprecedent_console_script() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")

    assert 'openprecedent = "openprecedent.cli:run"' not in pyproject
    assert 'openprecedent-pm = "openprecedent.codex_pm:run"' in pyproject


def test_python_ci_workflow_includes_dedicated_rust_ci_job() -> None:
    workflow = (ROOT / ".github" / "workflows" / "python-ci.yml").read_text(encoding="utf-8")

    assert "rust-ci:" in workflow
    assert "name: rust-ci" in workflow
    assert "run: cargo test" in workflow
