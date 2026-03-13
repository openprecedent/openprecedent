use std::fs;

use assert_cmd::Command;
use serde_json::Value;
use tempfile::tempdir;

fn cli() -> Command {
    Command::cargo_bin("openprecedent").expect("cargo bin")
}

fn create_case(db_path: &std::path::Path, case_id: &str, title: &str) {
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
}

#[test]
fn event_append_writes_event_and_returns_json() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    create_case(&db_path, "case_event_append", "Event append");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "event",
            "append",
            "case_event_append",
            "message.agent",
            "agent",
            "--payload",
            "{\"message\":\"inspect files first\"}",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let event: Value = serde_json::from_slice(&output).expect("event");
    assert_eq!(event["case_id"], "case_event_append");
    assert_eq!(event["event_type"], "message.agent");
    assert_eq!(event["actor"], "agent");
    assert_eq!(event["sequence_no"], 1);
    assert_eq!(event["payload"]["message"], "inspect files first");
}

#[test]
fn event_import_jsonl_ingests_events_and_preserves_case_completion_summary() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    create_case(&db_path, "case_event_import", "Event import");

    let jsonl_path = runtime.path().join("events.jsonl");
    fs::write(
        &jsonl_path,
        concat!(
            "{\"case_id\":\"case_event_import\",\"event_type\":\"message.user\",\"actor\":\"user\",\"payload\":{\"message\":\"hello\"}}\n",
            "{\"case_id\":\"case_event_import\",\"event_type\":\"case.completed\",\"actor\":\"system\",\"payload\":{\"summary\":\"imported summary\"}}\n"
        ),
    )
    .expect("write jsonl");

    let import_output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "event",
            "import-jsonl",
            jsonl_path.to_str().expect("jsonl path"),
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let imported: Value = serde_json::from_slice(&import_output).expect("import");
    let imported = imported.as_array().expect("array");
    assert_eq!(imported.len(), 2);
    assert_eq!(imported[0]["sequence_no"], 1);
    assert_eq!(imported[1]["event_type"], "case.completed");

    let case_output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "case",
            "show",
            "case_event_import",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let case: Value = serde_json::from_slice(&case_output).expect("case");
    assert_eq!(case["status"], "completed");
    assert_eq!(case["final_summary"], "imported summary");
}

#[test]
fn event_append_reports_missing_case() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "event",
            "append",
            "missing-case",
            "message.user",
            "user",
        ])
        .assert()
        .failure()
        .stderr(predicates::str::contains("case not found: missing-case"));
}

#[test]
fn event_import_jsonl_requires_case_id_when_missing_from_record_and_flag() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    let jsonl_path = runtime.path().join("events.jsonl");
    fs::write(
        &jsonl_path,
        "{\"event_type\":\"message.user\",\"actor\":\"user\",\"payload\":{\"message\":\"hello\"}}\n",
    )
    .expect("write jsonl");

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "event",
            "import-jsonl",
            jsonl_path.to_str().expect("jsonl path"),
        ])
        .assert()
        .failure()
        .stderr(predicates::str::contains("line 1: case_id is required"));
}
