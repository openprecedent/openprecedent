from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_install_harnesshub_skill_copies_bundle_and_rewrites_repo_root(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    harnesshub_root = tmp_path / "HarnessHub"
    (harnesshub_root / ".git").mkdir(parents=True)

    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "install_harnesshub_skill.py"),
            "--target-repo-root",
            str(harnesshub_root),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    skills_root = harnesshub_root / ".codex" / "skills"
    skill_root = skills_root / "openprecedent-harnesshub-validation"
    composition_root = skills_root / "openprecedent-harnesshub-composition"
    assert result.stdout.strip() == str(skill_root)

    skill_content = (skill_root / "SKILL.md").read_text(encoding="utf-8")
    reference_content = (skill_root / "references" / "harnesshub-validation.md").read_text(encoding="utf-8")
    composition_content = (composition_root / "SKILL.md").read_text(encoding="utf-8")

    assert "{{OPENPRECEDENT_REPO_ROOT}}" not in skill_content
    assert "{{OPENPRECEDENT_REPO_ROOT}}" not in reference_content
    assert str(repo_root) in skill_content
    assert str(repo_root) in reference_content
    assert composition_root.exists()
    assert "default companion" in composition_content
    assert "harness-issue-execution" in composition_content
    assert "openprecedent-harnesshub-validation" in composition_content
    assert "compose it with `harness-issue-execution`" in skill_content
    assert "Step 0: Probe Availability" in skill_content
    assert "--format json lineage brief" in skill_content
    assert "command -v openprecedent" in skill_content
    assert "continue the task normally" in reference_content


def test_install_harnesshub_skill_replaces_existing_bundle(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    harnesshub_root = tmp_path / "HarnessHub"
    stale_root = harnesshub_root / ".codex" / "skills" / "openprecedent-harnesshub-validation"
    stale_composition_root = harnesshub_root / ".codex" / "skills" / "openprecedent-harnesshub-composition"
    (harnesshub_root / ".git").mkdir(parents=True)
    stale_root.mkdir(parents=True)
    stale_composition_root.mkdir(parents=True)
    (stale_root / "obsolete.txt").write_text("stale\n", encoding="utf-8")
    (stale_composition_root / "obsolete.txt").write_text("stale\n", encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "install_harnesshub_skill.py"),
            "--target-repo-root",
            str(harnesshub_root),
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert not (stale_root / "obsolete.txt").exists()
    assert not (stale_composition_root / "obsolete.txt").exists()
