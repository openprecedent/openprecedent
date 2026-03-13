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

fn append_event(
    db_path: &std::path::Path,
    case_id: &str,
    event_type: &str,
    actor: &str,
    payload: &str,
) {
    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "event",
            "append",
            case_id,
            event_type,
            actor,
            "--payload",
            payload,
        ])
        .assert()
        .success();
}

fn seed_decision_case(db_path: &std::path::Path, case_id: &str) {
    create_case(db_path, case_id, "Decision extraction");
    append_event(
        db_path,
        case_id,
        "message.user",
        "user",
        "{\"message\":\"Do not edit code. Provide a short written recommendation only.\"}",
    );
    append_event(
        db_path,
        case_id,
        "message.agent",
        "agent",
        "{\"message\":\"I will stay within docs-only scope and provide a short recommendation.\"}",
    );
    append_event(
        db_path,
        case_id,
        "message.user",
        "user",
        "{\"message\":\"Rather than implementation, focus on a docs-only recommendation and nothing else.\"}",
    );
    append_event(
        db_path,
        case_id,
        "user.confirmed",
        "user",
        "{\"message\":\"Approved. Continue within docs-only scope.\"}",
    );
}

#[test]
fn decision_extract_derives_expected_decision_types() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    seed_decision_case(&db_path, "case_decision_extract");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "decision",
            "extract",
            "case_decision_extract",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let decisions: Value = serde_json::from_slice(&output).expect("decisions");
    let decisions = decisions.as_array().expect("array");
    let decision_types = decisions
        .iter()
        .map(|item| item["decision_type"].as_str().expect("decision type"))
        .collect::<Vec<_>>();

    assert!(decision_types.contains(&"task_frame_defined"));
    assert!(decision_types.contains(&"constraint_adopted"));
    assert!(decision_types.contains(&"success_criteria_set"));
    assert!(decision_types.contains(&"clarification_resolved"));
    assert!(decision_types.contains(&"option_rejected"));
    assert!(decision_types.contains(&"authority_confirmed"));
}

#[test]
fn decision_list_renders_text_after_extract() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    seed_decision_case(&db_path, "case_decision_list");

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "decision",
            "extract",
            "case_decision_list",
        ])
        .assert()
        .success();

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "decision",
            "list",
            "case_decision_list",
        ])
        .assert()
        .success()
        .stdout(predicates::str::contains("question:"))
        .stdout(predicates::str::contains("confidence:"))
        .stdout(predicates::str::contains("why:"));
}

#[test]
fn decision_extract_reports_missing_case() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "decision",
            "extract",
            "missing-case",
        ])
        .assert()
        .failure()
        .stderr(predicates::str::contains("case not found: missing-case"));
}
