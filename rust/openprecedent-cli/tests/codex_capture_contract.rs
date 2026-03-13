use std::path::Path;

use assert_cmd::Command;
use serde_json::Value;
use tempfile::tempdir;

fn cli() -> Command {
    Command::cargo_bin("openprecedent").expect("cargo bin")
}

fn fixture(name: &str) -> String {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../tests/fixtures")
        .join(name)
        .display()
        .to_string()
}

#[test]
fn capture_codex_import_rollout_imports_trace_and_replay_reads_it() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "capture",
            "codex",
            "import-rollout",
            &fixture("codex_rollout.jsonl"),
            "--case-id",
            "case_codex_rollout_rust",
            "--title",
            "Codex imported rollout",
            "--user-id",
            "u1",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let imported: Value = serde_json::from_slice(&output).expect("imported");
    assert_eq!(imported["case"]["case_id"], "case_codex_rollout_rust");
    assert_eq!(imported["imported_event_count"], 6);
    assert_eq!(
        imported["unsupported_record_type_counts"],
        serde_json::json!({"event_msg:task_started": 1})
    );

    let replay_output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "replay",
            "case",
            "case_codex_rollout_rust",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let replay: Value = serde_json::from_slice(&replay_output).expect("replay");
    assert_eq!(replay["case"]["status"], "completed");
    assert_eq!(
        replay["summary"],
        "Codex runtime research should stay Codex-specific and avoid generic multi-runtime abstraction for now."
    );
}

#[test]
fn capture_codex_import_rollout_strips_noise_and_preserves_semantic_tool_payloads() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "capture",
            "codex",
            "import-rollout",
            &fixture("codex_rollout_noisy.jsonl"),
            "--case-id",
            "case_codex_noise_rust",
            "--title",
            "Codex noisy rollout",
            "--user-id",
            "u1",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let imported: Value = serde_json::from_slice(&output).expect("imported");
    assert_eq!(imported["imported_event_count"], 6);
    assert_eq!(
        imported["unsupported_record_type_counts"],
        serde_json::json!({
            "event_msg:task_started": 1,
            "event_msg:token_count": 1,
            "response_item:message": 2,
            "response_item:reasoning": 1,
            "turn_context": 1
        })
    );

    let replay_output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "replay",
            "case",
            "case_codex_noise_rust",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let replay: Value = serde_json::from_slice(&replay_output).expect("replay");
    assert_eq!(
        replay["summary"],
        "Codex replay should show semantic evidence without transport wrappers."
    );

    let tool_called = replay["events"]
        .as_array()
        .expect("events")
        .iter()
        .find(|event| event["event_type"] == "tool.called")
        .expect("tool called");
    let tool_completed = replay["events"]
        .as_array()
        .expect("events")
        .iter()
        .find(|event| event["event_type"] == "tool.completed")
        .expect("tool completed");

    assert_eq!(
        tool_called["payload"]["arguments"],
        serde_json::json!({
            "cmd": "sed -n '1,40p' docs/engineering/codex-runtime-boundary.md",
            "workdir": "/workspace/02-projects/incubation/openprecedent"
        })
    );
    assert_eq!(
        tool_completed["payload"]["output"],
        "# Codex Runtime Boundary For Research\nThe goal is not to make OpenPrecedent generic."
    );
}

#[test]
fn capture_codex_import_rollout_feeds_precedent_ranking() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    let imports = [
        (
            "case_codex_precedent_current_rust",
            "Current Codex docs-only recommendation",
            "codex_rollout_precedent_current.jsonl",
        ),
        (
            "case_codex_precedent_semantic_rust",
            "Semantic Codex docs-only precedent",
            "codex_rollout_precedent_semantic_match.jsonl",
        ),
        (
            "case_codex_precedent_operational_rust",
            "Operationally similar Codex summary",
            "codex_rollout_precedent_operational_overlap.jsonl",
        ),
    ];

    for (case_id, title, filename) in imports {
        cli()
            .args([
                "--db",
                db_path.to_str().expect("db path"),
                "capture",
                "codex",
                "import-rollout",
                &fixture(filename),
                "--case-id",
                case_id,
                "--title",
                title,
                "--user-id",
                "u1",
            ])
            .assert()
            .success();
        cli()
            .args([
                "--db",
                db_path.to_str().expect("db path"),
                "--format",
                "json",
                "decision",
                "extract",
                case_id,
            ])
            .assert()
            .success();
    }

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "precedent",
            "find",
            "case_codex_precedent_current_rust",
            "--limit",
            "2",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let precedents: Value = serde_json::from_slice(&output).expect("precedents");
    let precedents = precedents.as_array().expect("precedents array");
    assert_eq!(precedents.len(), 2);
    assert_eq!(
        precedents[0]["case_id"],
        "case_codex_precedent_semantic_rust"
    );
    assert_eq!(
        precedents[1]["case_id"],
        "case_codex_precedent_operational_rust"
    );
}
