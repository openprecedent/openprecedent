from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


def _openprecedent_bin(repo_root: Path) -> Path:
    release_candidate = repo_root / "target" / "release" / "openprecedent"
    if release_candidate.exists():
        return release_candidate

    debug_candidate = repo_root / "target" / "debug" / "openprecedent"
    if debug_candidate.exists():
        return debug_candidate

    subprocess.run(
        ["cargo", "build", "-q", "-p", "openprecedent-cli"],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return debug_candidate


def test_harnesshub_matched_case_validation_produces_non_empty_matches(tmp_path: Path) -> None:
    repo_root = Path(__file__).parent.parent
    python_bin = repo_root / ".venv" / "bin" / "python"
    openprecedent_bin = _openprecedent_bin(repo_root)
    if not python_bin.exists():
        python_bin = repo_root.parent / "openprecedent" / ".venv" / "bin" / "python"

    bundle_dir = tmp_path / "bundle"
    bundle_dir.mkdir()
    case_id = "case_harnesshub_issue_53_readiness"
    (bundle_dir / "round-manifest.json").write_text(
        json.dumps(
            {
                "case_id": case_id,
                "case_title": "HarnessHub issue #53: Refine verification into explicit readiness classes",
                "import_hints": {
                    "agent_id": "codex",
                    "event_import_path": "events.jsonl",
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (bundle_dir / "events.jsonl").write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "case_id": case_id,
                        "event_id": f"{case_id}-1",
                        "event_type": "case.started",
                        "actor": "system",
                        "timestamp": "2026-03-12T07:41:00Z",
                        "sequence_no": 1,
                        "payload": {"source": "test"},
                    }
                ),
                json.dumps(
                    {
                        "case_id": case_id,
                        "event_id": f"{case_id}-2",
                        "event_type": "message.user",
                        "actor": "user",
                        "timestamp": "2026-03-12T07:41:30Z",
                        "sequence_no": 2,
                        "payload": {
                            "message": "Issue #53: refine verification into explicit readiness classes. Focus only on verification output, imported images, runtime-readiness issues, and tests."
                        },
                    }
                ),
                json.dumps(
                    {
                        "case_id": case_id,
                        "event_id": f"{case_id}-3",
                        "event_type": "message.agent",
                        "actor": "agent",
                        "timestamp": "2026-03-12T07:42:00Z",
                        "sequence_no": 3,
                        "payload": {
                            "message": "I will keep the verification scope narrow and map runtime-readiness issues into explicit readiness classes for imported images."
                        },
                    }
                ),
                json.dumps(
                    {
                        "case_id": case_id,
                        "event_id": f"{case_id}-4",
                        "event_type": "case.completed",
                        "actor": "system",
                        "timestamp": "2026-03-12T07:46:00Z",
                        "sequence_no": 4,
                        "payload": {"message": "Completed HarnessHub issue #53."},
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    live_root = tmp_path / "live"
    env = os.environ.copy()
    env["OPENPRECEDENT_HARNESSHUB_MATCH_ROOT"] = str(live_root)
    env["OPENPRECEDENT_HARNESSHUB_MATCH_RESET"] = "1"
    env["OPENPRECEDENT_HARNESSHUB_BUNDLE_DIR"] = str(bundle_dir)
    env["OPENPRECEDENT_BIN"] = str(openprecedent_bin)
    env["OPENPRECEDENT_PYTHON_BIN"] = str(python_bin)
    env["PYTHONPATH"] = str(repo_root / "src")

    result = subprocess.run(
        ["./scripts/run-harnesshub-matched-case-validation.sh"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    output_root = live_root / "output"
    brief = json.loads((output_root / "10-brief.json").read_text(encoding="utf-8"))
    summary = json.loads((output_root / "21-latest-invocation-summary.json").read_text(encoding="utf-8"))
    inspection = json.loads((output_root / "22-latest-invocation-inspection.json").read_text(encoding="utf-8"))

    assert brief["matched_cases"][0]["case_id"] == case_id
    assert summary["latest_matched_case_ids"] == [case_id]
    assert inspection["invocation"]["matched_case_ids"] == [case_id]
