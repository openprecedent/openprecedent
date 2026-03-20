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


def test_retired_python_public_cli_module_is_removed() -> None:
    assert not (ROOT / "src" / "openprecedent" / "cli.py").exists()


def test_rust_ci_workflow_exists_as_a_dedicated_workflow() -> None:
    python_workflow = (ROOT / ".github" / "workflows" / "python-ci.yml").read_text(encoding="utf-8")
    rust_workflow = (ROOT / ".github" / "workflows" / "rust-ci.yml").read_text(encoding="utf-8")

    assert "rust-ci:" not in python_workflow
    assert "name: rust-ci" in rust_workflow
    assert "rust-ci:" in rust_workflow
    assert "run: cargo test" in rust_workflow


def test_coverage_workflow_reports_python_and_rust_coverage() -> None:
    coverage_workflow = (ROOT / ".github" / "workflows" / "coverage.yml").read_text(encoding="utf-8")

    assert "name: coverage" in coverage_workflow
    assert "taiki-e/install-action@cargo-llvm-cov" in coverage_workflow
    assert "./scripts/run-coverage.sh" in coverage_workflow
    assert "scripts/check_mvp_coverage_gate.py" in coverage_workflow
    assert "coverage/coverage-summary.md" in coverage_workflow
    assert "coverage-report" in coverage_workflow

def test_readme_and_usage_guide_point_to_mvp_quickstart() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    usage_guide = (ROOT / "docs" / "engineering" / "cli" / "using-openprecedent.md").read_text(
        encoding="utf-8"
    )
    quickstart = ROOT / "docs" / "engineering" / "cli" / "mvp-quickstart.md"

    assert quickstart.exists()
    assert "docs/engineering/cli/mvp-quickstart.md" in readme
    assert "mvp-quickstart.md" in usage_guide


def test_release_docs_link_quickstart_scope_and_validation_checklist() -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    release_scope = (ROOT / "docs" / "product" / "mvp-release-scope.md").read_text(encoding="utf-8")
    validation_checklist = (
        ROOT / "docs" / "product" / "mvp-release-validation-checklist.md"
    ).read_text(encoding="utf-8")
    tooling_setup = (ROOT / "docs" / "engineering" / "runtime" / "tooling-setup.md").read_text(
        encoding="utf-8"
    )

    assert "docs/engineering/cli/mvp-quickstart.md" in readme
    assert "docs/product/mvp-release-validation-checklist.md" in readme
    assert "mvp-release-validation-checklist.md" in release_scope
    assert "docs/engineering/cli/mvp-quickstart.md" in validation_checklist
    assert "scripts/check_mvp_coverage_gate.py" in validation_checklist
    assert "mvp-release-validation-checklist.md" in tooling_setup
