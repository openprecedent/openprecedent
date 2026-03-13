use std::fs;

use assert_cmd::Command;
use serde_json::Value;
use tempfile::tempdir;

fn cli() -> Command {
    Command::cargo_bin("openprecedent").expect("cargo bin")
}

#[test]
fn capture_openclaw_list_sessions_reads_sessions_index() {
    let runtime = tempdir().expect("runtime");
    let fixture_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../tests/fixtures/openclaw_sessions");
    let sessions_dir = runtime.path().join("sessions");
    fs::create_dir_all(&sessions_dir).expect("sessions dir");
    fs::copy(
        fixture_dir.join("sample-session.jsonl"),
        sessions_dir.join("sample-session.jsonl"),
    )
    .expect("copy transcript");
    fs::write(
        sessions_dir.join("sessions.json"),
        fs::read_to_string(fixture_dir.join("sessions.json"))
            .expect("read sessions")
            .replace(
                "__FIXTURE_DIR__",
                sessions_dir.to_str().expect("sessions path"),
            ),
    )
    .expect("write sessions");

    let output = cli()
        .args([
            "--format",
            "json",
            "capture",
            "openclaw",
            "list-sessions",
            "--sessions-root",
            sessions_dir.to_str().expect("sessions dir"),
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let sessions: Value = serde_json::from_slice(&output).expect("sessions");
    let sessions = sessions.as_array().expect("array");
    assert_eq!(sessions.len(), 1);
    assert_eq!(sessions[0]["session_id"], "sample-session");
    assert_eq!(sessions[0]["is_active"], true);
    assert_eq!(
        sessions[0]["transcript_path"],
        sessions_dir
            .join("sample-session.jsonl")
            .display()
            .to_string()
    );
}

#[test]
fn capture_openclaw_list_sessions_falls_back_to_jsonl_directory_listing() {
    let runtime = tempdir().expect("runtime");
    let sessions_dir = runtime.path().join("sessions");
    fs::create_dir_all(&sessions_dir).expect("sessions dir");
    fs::write(sessions_dir.join("zeta.jsonl"), "{}\n").expect("write zeta");
    fs::write(sessions_dir.join("alpha.jsonl"), "{}\n").expect("write alpha");

    let output = cli()
        .args([
            "--format",
            "json",
            "capture",
            "openclaw",
            "list-sessions",
            "--sessions-root",
            sessions_dir.to_str().expect("sessions dir"),
            "--limit",
            "2",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let sessions: Value = serde_json::from_slice(&output).expect("sessions");
    let sessions = sessions.as_array().expect("array");
    assert_eq!(sessions.len(), 2);
    let ids = sessions
        .iter()
        .map(|item| item["session_id"].as_str().expect("session id"))
        .collect::<Vec<_>>();
    assert!(ids.contains(&"alpha"));
    assert!(ids.contains(&"zeta"));
}

#[test]
fn capture_openclaw_import_jsonl_imports_trace_and_replay_reads_it() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    let fixture_path = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../tests/fixtures/openclaw_trace.jsonl");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "capture",
            "openclaw",
            "import-jsonl",
            fixture_path.to_str().expect("fixture path"),
            "--case-id",
            "case_openclaw_rust",
            "--title",
            "OpenClaw imported trace",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let imported: Value = serde_json::from_slice(&output).expect("imported");
    assert_eq!(imported["case"]["case_id"], "case_openclaw_rust");
    assert_eq!(imported["imported_event_count"], 6);

    let replay_output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "replay",
            "case",
            "case_openclaw_rust",
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
        "Provided the context-graph document summary."
    );
}

#[test]
fn capture_openclaw_import_session_imports_sample_transcript() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    let fixture_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../tests/fixtures/openclaw_sessions");
    let session_path = fixture_dir.join("sample-session.jsonl");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "capture",
            "openclaw",
            "import-session",
            "--session-file",
            session_path.to_str().expect("session path"),
            "--case-id",
            "case_session_sample_rust",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let imported: Value = serde_json::from_slice(&output).expect("imported");
    assert_eq!(imported["case"]["case_id"], "case_session_sample_rust");
    assert_eq!(imported["imported_event_count"], 9);
    assert_eq!(
        imported["unsupported_record_type_counts"],
        serde_json::json!({})
    );
}

#[test]
fn capture_openclaw_collect_sessions_tracks_state_and_skips_duplicates() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    let fixture_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../tests/fixtures/openclaw_sessions");
    let sessions_dir = runtime.path().join("sessions");
    fs::create_dir_all(&sessions_dir).expect("sessions dir");
    fs::copy(
        fixture_dir.join("sample-session.jsonl"),
        sessions_dir.join("sample-session.jsonl"),
    )
    .expect("copy transcript");
    fs::write(
        sessions_dir.join("sessions.json"),
        fs::read_to_string(fixture_dir.join("sessions.json"))
            .expect("read sessions")
            .replace(
                "__FIXTURE_DIR__",
                sessions_dir.to_str().expect("sessions path"),
            ),
    )
    .expect("write sessions");
    let state_path = runtime.path().join("collector-state.json");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "capture",
            "openclaw",
            "collect-sessions",
            "--sessions-root",
            sessions_dir.to_str().expect("sessions dir"),
            "--state-file",
            state_path.to_str().expect("state path"),
            "--limit",
            "1",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let collected: Value = serde_json::from_slice(&output).expect("collected");
    assert_eq!(collected["imported"][0]["session_id"], "sample-session");
    assert_eq!(collected["imported"][0]["imported_event_count"], 9);

    let output_again = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "capture",
            "openclaw",
            "collect-sessions",
            "--sessions-root",
            sessions_dir.to_str().expect("sessions dir"),
            "--state-file",
            state_path.to_str().expect("state path"),
            "--limit",
            "1",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let collected_again: Value = serde_json::from_slice(&output_again).expect("collected again");
    assert_eq!(collected_again["imported"], serde_json::json!([]));
    assert_eq!(
        collected_again["skipped_session_ids"],
        serde_json::json!(["sample-session"])
    );
}
