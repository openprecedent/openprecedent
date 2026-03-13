use std::fs;

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
fn lineage_invocation_list_reads_logged_entries() {
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
        .success();

    let output = cli()
        .args([
            "--invocation-log",
            log_path.to_str().expect("log path"),
            "--format",
            "json",
            "lineage",
            "invocation",
            "list",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let invocations: Value = serde_json::from_slice(&output).expect("invocations");
    let invocations = invocations.as_array().expect("array");
    assert_eq!(invocations.len(), 1);
    assert_eq!(invocations[0]["query_reason"], "initial_planning");
    assert_eq!(invocations[0]["session_id"], "session_runtime_scope");
    assert_eq!(
        invocations[0]["matched_case_ids"],
        serde_json::json!(["case_cli_brief_guidance"])
    );
}

#[test]
fn lineage_invocation_inspect_returns_downstream_events_and_decisions() {
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

    cli()
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
        ])
        .assert()
        .success();

    let logged = fs::read_to_string(&log_path).expect("log file");
    let invocation_id = logged
        .lines()
        .filter(|line| !line.trim().is_empty())
        .map(|line| serde_json::from_str::<Value>(line).expect("json line"))
        .last()
        .and_then(|row| row["invocation_id"].as_str().map(ToString::to_string))
        .expect("invocation id");

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "event",
            "append",
            "case_runtime_scope",
            "message.agent",
            "agent",
            "--payload",
            "{\"message\":\"I will keep this docs-only and avoid code edits.\"}",
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
            "case_runtime_scope",
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
            "invocation",
            "inspect",
            "--invocation-id",
            &invocation_id,
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let inspection: Value = serde_json::from_slice(&output).expect("inspection");
    assert_eq!(
        inspection["invocation"]["matched_case_ids"],
        serde_json::json!(["case_cli_brief_guidance"])
    );
    assert!(
        inspection["downstream_events"]
            .as_array()
            .expect("events")
            .len()
            >= 1
    );
    assert!(
        inspection["downstream_decisions"]
            .as_array()
            .expect("decisions")
            .len()
            >= 1
    );
}
