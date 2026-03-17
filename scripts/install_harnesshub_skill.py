#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
from pathlib import Path


PLACEHOLDERS = ("{{OPENPRECEDENT_REPO_ROOT}}",)
SKILL_ROOT_NAMES = (
    "openprecedent-harnesshub-composition",
    "openprecedent-harnesshub-validation",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the OpenPrecedent-maintained private HarnessHub skill bundle into a target HarnessHub workspace."
    )
    parser.add_argument(
        "--target-repo-root",
        required=True,
        help="Path to the local HarnessHub repository root where the private skill should be installed.",
    )
    parser.add_argument(
        "--source-skill-root",
        help="Override one source skill root inside the private HarnessHub bundle. Defaults to <repo>/skills/openprecedent-harnesshub-validation and installs the sibling composition skill too.",
    )
    return parser.parse_args()


def replace_placeholders(path: Path, *, repo_root: Path) -> None:
    content = path.read_text(encoding="utf-8")
    if any(marker in content for marker in PLACEHOLDERS):
        content = content.replace("{{OPENPRECEDENT_REPO_ROOT}}", str(repo_root))
        path.write_text(content, encoding="utf-8")


def install_skill_bundle(*, repo_root: Path, target_repo_root: Path, source_skill_root: Path) -> Path:
    target_skills_root = target_repo_root / ".codex" / "skills"

    for skill_root_name in SKILL_ROOT_NAMES:
        source_bundle_root = source_skill_root.parent / skill_root_name
        if not source_bundle_root.exists():
            raise SystemExit(f"source skill bundle root not found: {source_bundle_root}")
        target_bundle_root = target_skills_root / skill_root_name
        if target_bundle_root.exists():
            shutil.rmtree(target_bundle_root)
        shutil.copytree(source_bundle_root, target_bundle_root)

        for path in target_bundle_root.rglob("*"):
            if path.is_file() and path.suffix.lower() == ".md":
                replace_placeholders(path, repo_root=repo_root)

    return target_skills_root / "openprecedent-harnesshub-validation"


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    source_skill_root = (
        Path(args.source_skill_root).expanduser().resolve()
        if args.source_skill_root
        else repo_root / "skills" / "openprecedent-harnesshub-validation"
    )
    target_repo_root = Path(args.target_repo_root).expanduser().resolve()

    if not source_skill_root.exists():
        raise SystemExit(f"source skill root not found: {source_skill_root}")
    if not (target_repo_root / ".git").exists():
        raise SystemExit(f"target repo root does not look like a git repository: {target_repo_root}")

    target_skill_root = install_skill_bundle(
        repo_root=repo_root,
        target_repo_root=target_repo_root,
        source_skill_root=source_skill_root,
    )
    print(target_skill_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
