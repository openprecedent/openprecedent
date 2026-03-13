from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_import_harnesshub_round_bundle_populates_runtime_and_extracts_decisions(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[1]
    openprecedent_bin = repo_root / "target" / "debug" / "openprecedent"
    if not openprecedent_bin.exists():
        subprocess.run(
            ["cargo", "build", "-q", "-p", "openprecedent-cli"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )

    bundle_dir = tmp_path / "bundle"
    bundle_dir.mkdir()

    case_id = "case_harnesshub_issue_53_readiness"
    case_title = "HarnessHub issue #53: Refine verification into explicit readiness classes"
    (bundle_dir / "round-manifest.json").write_text(
        json.dumps(
            {
                "case_id": case_id,
                "case_title": case_title,
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
                        "payload": {"message": "Issue #53: Refine verification into explicit readiness classes. Focus only on verification output and tests."},
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
                        "payload": {"message": "I will refine verification into explicit readiness classes and keep the scope narrow."},
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

    runtime_home = tmp_path / "runtime-home"
    runtime_home.mkdir()
    env = os.environ.copy()
    env["OPENPRECEDENT_HOME"] = str(runtime_home)
    env["PYTHONPATH"] = str(repo_root / "src")

    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "import_harnesshub_codex_round.py"),
            "--bundle-dir",
            str(bundle_dir),
            "--runtime-home",
            str(runtime_home),
            "--openprecedent-bin",
            str(openprecedent_bin),
        ],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )

    summary = json.loads(result.stdout)
    assert summary["case_id"] == case_id
    assert summary["imported_event_count"] == 4
    assert summary["decision_count"] >= 1

    list_result = subprocess.run(
        [str(openprecedent_bin), "--home", str(runtime_home), "--format", "json", "case", "list"],
        cwd=repo_root,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    cases = json.loads(list_result.stdout)
    assert any(item["case_id"] == case_id for item in cases)
