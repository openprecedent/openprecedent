use std::fs;
use std::path::Path;

use assert_cmd::Command;
use tempfile::tempdir;

fn cli() -> Command {
    Command::cargo_bin("openprecedent").expect("cargo bin")
}

#[test]
fn eval_fixtures_reports_expected_case_results() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    let suite_path =
        Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/evaluation/suite.json");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "eval",
            "fixtures",
            suite_path.to_str().expect("suite path"),
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let report: serde_json::Value = serde_json::from_slice(&output).expect("report");
    assert_eq!(report["total_cases"], 5);
    assert_eq!(report["failed_cases"], 0);
    assert_eq!(report["passed_cases"], 5);

    let authority_result = report["results"]
        .as_array()
        .expect("results")
        .iter()
        .find(|item| item["case_id"] == "eval_authority_scope")
        .expect("authority result");
    assert_eq!(
        authority_result["actual_decision_types"],
        serde_json::json!([
            "constraint_adopted",
            "success_criteria_set",
            "option_rejected",
            "task_frame_defined",
            "authority_confirmed"
        ])
    );
}

#[test]
fn eval_captured_openclaw_sessions_writes_report_and_renders_counts() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    let fixture_dir =
        Path::new(env!("CARGO_MANIFEST_DIR")).join("../../tests/fixtures/openclaw_sessions");
    let sessions_dir = runtime.path().join("sessions");
    fs::create_dir_all(&sessions_dir).expect("sessions dir");
    for name in [
        "sample-session.jsonl",
        "failing-command-session.jsonl",
        "unsupported-record-session.jsonl",
    ] {
        fs::copy(fixture_dir.join(name), sessions_dir.join(name)).expect("copy fixture");
    }
    fs::write(
        sessions_dir.join("sessions.json"),
        serde_json::to_string_pretty(&serde_json::json!([
            {
                "sessionId": "sample-session",
                "sessionFile": sessions_dir.join("sample-session.jsonl").display().to_string(),
                "updatedAt": 1741497000000_i64,
                "label": "User session: summarize context graph"
            },
            {
                "sessionId": "failing-command-session",
                "sessionFile": sessions_dir.join("failing-command-session.jsonl").display().to_string(),
                "updatedAt": 1741498000000_i64,
                "label": "User session: failing command"
            },
            {
                "sessionId": "unsupported-record-session",
                "sessionFile": sessions_dir.join("unsupported-record-session.jsonl").display().to_string(),
                "updatedAt": 1741499000000_i64,
                "label": "User session: unsupported record"
            }
        ]))
        .expect("sessions json"),
    )
    .expect("write sessions index");
    let state_path = runtime.path().join("collector-state.json");
    fs::write(
        &state_path,
        serde_json::to_string_pretty(&serde_json::json!({
            "imported_session_ids": [
                "failing-command-session",
                "sample-session",
                "unsupported-record-session"
            ]
        }))
        .expect("state json"),
    )
    .expect("write state");
    let report_path = runtime.path().join("collected-report.json");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "eval",
            "captured-openclaw-sessions",
            "--sessions-root",
            sessions_dir.to_str().expect("sessions dir"),
            "--state-file",
            state_path.to_str().expect("state path"),
            "--report-file",
            report_path.to_str().expect("report path"),
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let report: serde_json::Value = serde_json::from_slice(&output).expect("report");
    assert_eq!(report["total_sessions"], 3);
    assert_eq!(report["evaluated_cases"], 3);
    assert_eq!(
        report["unsupported_record_type_counts"],
        serde_json::json!({"audit_marker": 1})
    );
    assert!(report_path.exists());
}
