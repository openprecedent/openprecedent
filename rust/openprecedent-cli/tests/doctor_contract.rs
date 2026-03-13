use std::fs;

use assert_cmd::Command;
use serde_json::Value;
use tempfile::tempdir;

fn cli() -> Command {
    Command::cargo_bin("openprecedent").expect("cargo bin")
}

#[test]
fn version_supports_json_output() {
    let output = cli()
        .args(["version", "--format", "json"])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let payload: Value = serde_json::from_slice(&output).expect("json");
    assert_eq!(payload["name"], "openprecedent");
    assert_eq!(payload["contract_phase"], "bootstrap");
}

#[test]
fn doctor_paths_uses_default_runtime_home() {
    let home = tempdir().expect("home");

    let output = cli()
        .env("HOME", home.path())
        .env_remove("OPENPRECEDENT_HOME")
        .env_remove("OPENPRECEDENT_DB")
        .env_remove("OPENPRECEDENT_RUNTIME_INVOCATION_LOG")
        .env_remove("OPENPRECEDENT_COLLECTOR_STATE")
        .args(["doctor", "paths", "--format", "json"])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let payload: Value = serde_json::from_slice(&output).expect("json");
    assert_eq!(
        payload["home"]["path"],
        home.path()
            .join(".openprecedent")
            .join("runtime")
            .display()
            .to_string()
    );
    assert_eq!(payload["home"]["source"], "default");
    assert_eq!(payload["db"]["derived_from"], "home");
}

#[test]
fn doctor_paths_honors_flag_over_env_over_config() {
    let home = tempdir().expect("home");
    let config_dir = tempdir().expect("config");
    let config_path = config_dir.path().join("openprecedent.toml");
    fs::write(
        &config_path,
        "home = \"./configured-home\"\ndb = \"./configured-home/from-config.db\"\nformat = \"json\"\nno_color = true\n",
    )
    .expect("write config");

    let flag_db = home.path().join("from-flag.db");
    let env_home = home.path().join("from-env-home");

    let output = cli()
        .env("HOME", home.path())
        .env("OPENPRECEDENT_HOME", &env_home)
        .args([
            "doctor",
            "paths",
            "--config",
            config_path.to_str().expect("config path"),
            "--db",
            flag_db.to_str().expect("db path"),
            "--format",
            "json",
        ])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let payload: Value = serde_json::from_slice(&output).expect("json");
    assert_eq!(payload["home"]["path"], env_home.display().to_string());
    assert_eq!(payload["home"]["source"], "env");
    assert_eq!(payload["db"]["path"], flag_db.display().to_string());
    assert_eq!(payload["db"]["source"], "flag");
    assert_eq!(payload["config_file"]["exists"], true);
}

#[test]
fn doctor_environment_reports_resolved_globals_and_env_vars() {
    let home = tempdir().expect("home");
    let output = cli()
        .env("HOME", home.path())
        .env("OPENPRECEDENT_HOME", home.path().join("runtime-home"))
        .env("OPENPRECEDENT_NO_COLOR", "true")
        .args(["doctor", "environment", "--format", "json"])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let payload: Value = serde_json::from_slice(&output).expect("json");
    assert_eq!(payload["format"]["value"], "json");
    assert_eq!(payload["format"]["source"], "flag");
    assert_eq!(payload["no_color"]["value"], true);
    assert_eq!(payload["no_color"]["source"], "env");
    assert!(payload["variables"]
        .as_array()
        .expect("array")
        .iter()
        .any(|entry| entry["name"] == "OPENPRECEDENT_HOME" && entry["is_set"] == true));
}

#[test]
fn doctor_storage_reports_existing_and_missing_paths() {
    let home = tempdir().expect("home");
    let runtime_home = home.path().join("runtime-home");
    fs::create_dir_all(&runtime_home).expect("runtime home");
    let db_path = runtime_home.join("openprecedent.db");
    fs::write(&db_path, b"sqlite placeholder").expect("db");

    let output = cli()
        .env("HOME", home.path())
        .env("OPENPRECEDENT_HOME", &runtime_home)
        .args(["doctor", "storage", "--format", "json"])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();

    let payload: Value = serde_json::from_slice(&output).expect("json");
    assert_eq!(payload["db"]["exists"], true);
    assert_eq!(payload["invocation_log"]["exists"], false);
    assert_eq!(payload["state_file"]["parent_exists"], true);
}
