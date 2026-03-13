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

fn seed_case_with_decisions(
    db_path: &std::path::Path,
    case_id: &str,
    title: &str,
    user_message: &str,
    agent_message: &str,
    completion_summary: &str,
) {
    create_case(db_path, case_id, title);
    append_event(
        db_path,
        case_id,
        "message.user",
        "user",
        &format!("{{\"message\":\"{user_message}\"}}"),
    );
    append_event(
        db_path,
        case_id,
        "message.agent",
        "agent",
        &format!("{{\"message\":\"{agent_message}\"}}"),
    );
    append_event(
        db_path,
        case_id,
        "tool.called",
        "agent",
        "{\"tool_name\":\"rg\",\"reason\":\"search\"}",
    );
    append_event(
        db_path,
        case_id,
        "file.write",
        "agent",
        "{\"path\":\"docs/plan.md\",\"summary\":\"updated plan\"}",
    );
    append_event(
        db_path,
        case_id,
        "case.completed",
        "system",
        &format!("{{\"summary\":\"{completion_summary}\"}}"),
    );

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "decision",
            "extract",
            case_id,
        ])
        .assert()
        .success();
}

#[test]
fn replay_case_returns_json_with_summary_and_artifacts() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    seed_case_with_decisions(
        &db_path,
        "case_replay",
        "Replay case",
        "Provide a short summary only.",
        "I will inspect the docs and provide a short summary.",
        "summary complete",
    );

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "replay",
            "case",
            "case_replay",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let replay: Value = serde_json::from_slice(&output).expect("replay");
    assert_eq!(replay["case"]["case_id"], "case_replay");
    assert_eq!(replay["summary"], "summary complete");
    assert!(replay["events"].as_array().expect("events").len() >= 5);
    assert!(replay["decisions"].as_array().expect("decisions").len() >= 1);
    assert!(replay["artifacts"].as_array().expect("artifacts").len() >= 2);
}

#[test]
fn replay_case_renders_text_output() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");
    seed_case_with_decisions(
        &db_path,
        "case_replay_text",
        "Replay text case",
        "Do not edit code. Provide a short written recommendation only.",
        "I will stay within docs-only scope and provide a short recommendation.",
        "done",
    );

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "replay",
            "case",
            "case_replay_text",
        ])
        .assert()
        .success()
        .stdout(predicates::str::contains("Events:"))
        .stdout(predicates::str::contains("Decisions:"))
        .stdout(predicates::str::contains("Artifacts:"))
        .stdout(predicates::str::contains("Summary: done"));
}

#[test]
fn precedent_find_returns_ranked_similar_cases() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    seed_case_with_decisions(
        &db_path,
        "case_prev_a",
        "Previous A",
        "Provide a short docs summary only.",
        "I will inspect docs and provide a short summary.",
        "done a",
    );
    seed_case_with_decisions(
        &db_path,
        "case_prev_b",
        "Previous B",
        "Provide a short docs summary only.",
        "I will inspect docs and provide a short summary.",
        "done b",
    );
    seed_case_with_decisions(
        &db_path,
        "case_other",
        "Other case",
        "Implement a shipping dashboard with charts.",
        "I will build the dashboard implementation.",
        "dashboard done",
    );

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "precedent",
            "find",
            "case_prev_a",
            "--limit",
            "2",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let precedents: Value = serde_json::from_slice(&output).expect("precedents");
    let precedents = precedents.as_array().expect("array");
    assert!(!precedents.is_empty());
    assert_eq!(precedents[0]["case_id"], "case_prev_b");
    assert!(precedents[0]["similarity_score"].as_i64().expect("score") > 0);
    assert!(!precedents[0]["similarities"]
        .as_array()
        .expect("similarities")
        .is_empty());
}

#[test]
fn replay_and_precedent_report_missing_case() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "replay",
            "case",
            "missing-case",
        ])
        .assert()
        .failure()
        .stderr(predicates::str::contains("case not found: missing-case"));

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "precedent",
            "find",
            "missing-case",
        ])
        .assert()
        .failure()
        .stderr(predicates::str::contains("case not found: missing-case"));
}
