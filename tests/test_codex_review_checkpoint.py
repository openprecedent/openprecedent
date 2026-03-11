import os
import subprocess
from pathlib import Path


def _run_checkpoint(tmp_path: Path, repo_root: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["OPENPRECEDENT_REVIEW_FILE"] = str(tmp_path / ".codex-review")
    env["OPENPRECEDENT_REVIEW_PROOF_FILE"] = str(tmp_path / ".codex-review-proof")
    env["OPENPRECEDENT_REVIEW_BASE_REF"] = "HEAD"
    return subprocess.run(
        ["./scripts/run-codex-review-checkpoint.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )


def test_review_checkpoint_creates_template(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    review_file = tmp_path / ".codex-review"
    proof_file = tmp_path / ".codex-review-proof"

    result = _run_checkpoint(tmp_path, repo_root)

    assert result.returncode == 0
    assert "Created review checkpoint template" in result.stdout
    assert "Refreshed review proof" in result.stdout
    content = review_file.read_text()
    assert "scope reviewed:" in content
    assert "findings: no findings" in content
    assert "remaining risks: native /review has not been run yet" in content
    assert "diff summary:" in content
    proof = proof_file.read_text()
    assert "head_sha=" in proof
    assert "branch=" in proof


def test_review_checkpoint_preserves_existing_note(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    review_file = tmp_path / ".codex-review"
    proof_file = tmp_path / ".codex-review-proof"
    review_file.write_text(
        "scope reviewed: existing\nfindings: no findings\nremaining risks: low\n"
    )

    result = _run_checkpoint(tmp_path, repo_root)

    assert result.returncode == 0
    assert "Review checkpoint already exists" in result.stdout
    assert proof_file.exists()
    assert review_file.read_text() == (
        "scope reviewed: existing\nfindings: no findings\nremaining risks: low\n"
    )
