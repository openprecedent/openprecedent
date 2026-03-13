use assert_cmd::Command;
use serde_json::Value;
use tempfile::tempdir;

fn cli() -> Command {
    Command::cargo_bin("openprecedent").expect("cargo bin")
}

#[test]
fn case_create_list_and_show_work_in_json_mode() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    let create_output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "case",
            "create",
            "--case-id",
            "case_rust_cli",
            "--title",
            "Rust case",
            "--user-id",
            "user-1",
            "--agent-id",
            "agent-1",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let created: Value = serde_json::from_slice(&create_output).expect("created");
    assert_eq!(created["case_id"], "case_rust_cli");
    assert_eq!(created["status"], "started");

    let list_output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "case",
            "list",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let listed: Value = serde_json::from_slice(&list_output).expect("list");
    assert_eq!(listed.as_array().expect("array").len(), 1);

    let show_output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "case",
            "show",
            "case_rust_cli",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let shown: Value = serde_json::from_slice(&show_output).expect("show");
    assert_eq!(shown["title"], "Rust case");
}

#[test]
fn case_create_generates_case_id_when_omitted() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    let output = cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "--format",
            "json",
            "case",
            "create",
            "--title",
            "Generated id case",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let created: Value = serde_json::from_slice(&output).expect("created");
    let case_id = created["case_id"].as_str().expect("case id");
    assert!(case_id.starts_with("case_"));
    assert_eq!(case_id.len(), 17);
}

#[test]
fn case_show_reports_missing_case() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "case",
            "show",
            "missing-case",
        ])
        .assert()
        .failure()
        .stderr(predicates::str::contains("case not found: missing-case"));
}

#[test]
fn case_create_reports_duplicate_case_id() {
    let runtime = tempdir().expect("runtime");
    let db_path = runtime.path().join("openprecedent.db");

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "case",
            "create",
            "--case-id",
            "duplicate-case",
            "--title",
            "first",
        ])
        .assert()
        .success();

    cli()
        .args([
            "--db",
            db_path.to_str().expect("db path"),
            "case",
            "create",
            "--case-id",
            "duplicate-case",
            "--title",
            "second",
        ])
        .assert()
        .failure()
        .stderr(predicates::str::contains(
            "case already exists: duplicate-case",
        ));
}
