from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path


def _load_module():
    script_path = Path(__file__).parent.parent / "scripts" / "archive_research_artifacts.py"
    spec = importlib.util.spec_from_file_location("archive_research_artifacts", script_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_sanitize_known_path_preserves_relative_repo_context(tmp_path: Path) -> None:
    module = _load_module()
    harnesshub_root = tmp_path / "HarnessHub"
    (harnesshub_root / "src" / "core").mkdir(parents=True)
    (harnesshub_root / "src" / "core" / "packer.ts").write_text("// fixture\n", encoding="utf-8")

    repo_roots = module.load_repo_roots([str(harnesshub_root)])

    sanitized = module.sanitize_known_path("src/core/packer.ts", repo_roots)

    assert sanitized == "HarnessHub/src/core/packer.ts"


def test_archive_script_keeps_relative_known_files_under_target_repo(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    runtime_home = tmp_path / "runtime-home"
    runtime_home.mkdir()
    harnesshub_root = tmp_path / "HarnessHub"
    (harnesshub_root / "src" / "core").mkdir(parents=True)
    (harnesshub_root / "src" / "core" / "packer.ts").write_text("// fixture\n", encoding="utf-8")

    invocation_log = runtime_home / "openprecedent-runtime-invocations.jsonl"
    invocation_log.write_text(
        json.dumps(
            {
                "invocation_id": "rtinv_test_relative",
                "recorded_at": "2026-03-12T07:03:17.437612Z",
                "query_reason": "before_file_write",
                "task_summary": "HarnessHub issue #47: define explicit template vs instance image contract",
                "current_plan": None,
                "candidate_action": "Introduce pack-type component policy and enforce it across export and verify",
                "known_files": ["src/core/packer.ts"],
                "case_id": None,
                "session_id": None,
                "matched_case_ids": [],
                "task_frame": None,
                "accepted_constraints": [],
                "success_criteria": [],
                "rejected_options": [],
                "authority_signals": [],
                "cautions": [],
                "suggested_focus": None,
            }
        )
        + "\n",
        encoding="utf-8",
    )

    output_root = tmp_path / "archives"
    subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "archive_research_artifacts.py"),
            "--study",
            "harnesshub",
            "--query",
            "HarnessHub",
            "--repo-root",
            str(harnesshub_root),
            "--runtime-home",
            str(runtime_home),
            "--output-root",
            str(output_root),
        ],
        cwd=repo_root,
        check=True,
    )

    study_root = output_root / "harnesshub"
    archive_dirs = sorted(study_root.iterdir())
    assert archive_dirs

    rows = [
        json.loads(line)
        for line in (archive_dirs[-1] / "runtime-invocations-sanitized.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]
    assert rows[0]["known_files"] == ["HarnessHub/src/core/packer.ts"]
