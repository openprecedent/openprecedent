use std::fs;
use std::path::Path;

use assert_cmd::Command;
use serde_json::Value;
use tempfile::tempdir;

fn cli() -> Command {
    Command::cargo_bin("openprecedent").expect("cargo bin")
}

fn seed_guidance_case(db_path: &std::path::Path, case_id: &str, title: &str) {
    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "case",
            "create",
            "--case-id",
            case_id,
            "--title",
            title,
        ])
        .assert()
        .success();

    for payload in [
        (
            "message.user",
            "user",
            "{\"message\":\"Do not edit code. Provide a short written recommendation only.\"}",
        ),
        (
            "message.agent",
            "agent",
            "{\"message\":\"I will stay within docs-only scope and provide a short recommendation.\"}",
        ),
        (
            "user.confirmed",
            "user",
            "{\"message\":\"Approved. Stay within docs-only scope.\"}",
        ),
    ] {
        cli()
            .args([
                "--db",
                db_path.to_str().expect("db path"),
                "event",
                "append",
                case_id,
                payload.0,
                payload.1,
                "--payload",
                payload.2,
            ])
            .assert()
            .success();
    }

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

#[test]
fn lineage_brief_returns_json_and_records_runtime_invocation() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    let log_path = runtime.path().join("runtime-invocations.jsonl");

    seed_guidance_case(
        &db_path,
        "case_cli_brief_guidance",
        "Docs-only recommendation",
    );

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "case",
            "create",
            "--case-id",
            "case_runtime_scope",
            "--title",
            "Runtime scope case",
        ])
        .assert()
        .success();

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--invocation-log",
            log_path.to_str().expect("log path"),
            "--format",
            "json",
            "lineage",
            "brief",
            "--query-reason",
            "initial_planning",
            "--task-summary",
            "Do not edit code. Provide a short written recommendation only.",
            "--case-id",
            "case_runtime_scope",
            "--session-id",
            "session_runtime_scope",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let brief: Value = serde_json::from_slice(&output).expect("brief");
    assert_eq!(brief["query_reason"], "initial_planning");
    assert_eq!(
        brief["matched_cases"][0]["case_id"],
        "case_cli_brief_guidance"
    );
    assert!(
        brief["authority_signals"]
            .as_array()
            .expect("authority")
            .len()
            >= 1
    );

    let logged = fs::read_to_string(&log_path).expect("log file");
    let rows = logged
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| serde_json::from_str::<Value>(line).expect("json line"))
        .collect::<Vec<_>>();
    assert_eq!(rows.len(), 1);
    assert_eq!(rows[0]["query_reason"], "initial_planning");
    assert_eq!(rows[0]["case_id"], "case_runtime_scope");
    assert_eq!(rows[0]["session_id"], "session_runtime_scope");
    assert_eq!(
        rows[0]["matched_case_ids"],
        serde_json::json!(["case_cli_brief_guidance"])
    );
}

#[test]
fn lineage_brief_uses_plan_action_and_known_file_context() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    let log_path = runtime.path().join("runtime-invocations.jsonl");
    let fixture_root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures");

    for (case_id, title, filename) in [
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
    ] {
        cli()
            .args([
                "--db",
                db_path.to_str().expect("db path"),
                "capture",
                "codex",
                "import-rollout",
                fixture_root.join(filename).to_str().expect("fixture"),
                "--case-id",
                case_id,
                "--title",
                title,
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
            "--invocation-log",
            log_path.to_str().expect("log path"),
            "--format",
            "json",
            "lineage",
            "brief",
            "--query-reason",
            "before_file_write",
            "--task-summary",
            "Do not edit code. Give me a brief recommendation about the Codex runtime boundary docs only.",
            "--current-plan",
            "Prepare a brief docs-only recommendation about the Codex runtime boundary docs.",
            "--candidate-action",
            "Edit docs/engineering/codex-runtime-boundary.md",
            "--known-file",
            "docs/engineering/codex-runtime-boundary.md",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let brief: Value = serde_json::from_slice(&output).expect("brief");
    assert_eq!(brief["query_reason"], "before_file_write");
    assert_eq!(
        brief["matched_cases"][0]["case_id"],
        "case_codex_precedent_semantic_rust"
    );

    let logged = fs::read_to_string(&log_path).expect("log file");
    let row = logged
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| serde_json::from_str::<Value>(line).expect("json line"))
        .last()
        .expect("logged row");
    assert_eq!(
        row["current_plan"],
        "Prepare a brief docs-only recommendation about the Codex runtime boundary docs."
    );
    assert_eq!(
        row["candidate_action"],
        "Edit docs/engineering/codex-runtime-boundary.md"
    );
    assert_eq!(
        row["known_files"],
        serde_json::json!(["docs/engineering/codex-runtime-boundary.md"])
    );
}
