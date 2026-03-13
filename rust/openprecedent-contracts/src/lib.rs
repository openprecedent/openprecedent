mod artifact;
mod case;
mod decision;
mod eval;
mod event;
mod lineage;
mod precedent;
mod replay;

use std::path::PathBuf;

use clap::ValueEnum;
use serde::{Deserialize, Serialize};

pub use artifact::{Artifact, ArtifactType};
pub use case::{Case, CaseStatus};
pub use decision::{Decision, DecisionExplanation, DecisionType};
pub use eval::{
    CollectedSessionEvaluationReport, CollectedSessionEvaluationResult, EvaluationCaseResult,
    EvaluationReport,
};
pub use event::{Event, EventActor, EventType};
pub use lineage::{
    DecisionLineageBrief, DecisionLineageMatchedCase, DecisionLineageQueryReason,
    RuntimeDecisionLineageInspection, RuntimeDecisionLineageInvocation,
};
pub use precedent::Precedent;
pub use replay::ReplayResponse;

pub const CLI_BINARY_NAME: &str = "openprecedent";
pub const CONTRACT_PHASE: &str = "bootstrap";
pub const DEFAULT_DB_NAME: &str = "openprecedent.db";
pub const DEFAULT_COLLECTOR_STATE_NAME: &str = "openprecedent-collector-state.json";
pub const DEFAULT_RUNTIME_INVOCATION_LOG_NAME: &str = "openprecedent-runtime-invocations.jsonl";
pub const HOME_ENV_VAR: &str = "OPENPRECEDENT_HOME";
pub const DB_ENV_VAR: &str = "OPENPRECEDENT_DB";
pub const COLLECTOR_STATE_ENV_VAR: &str = "OPENPRECEDENT_COLLECTOR_STATE";
pub const RUNTIME_INVOCATION_LOG_ENV_VAR: &str = "OPENPRECEDENT_RUNTIME_INVOCATION_LOG";
pub const FORMAT_ENV_VAR: &str = "OPENPRECEDENT_FORMAT";
pub const NO_COLOR_ENV_VAR: &str = "OPENPRECEDENT_NO_COLOR";

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize, ValueEnum)]
#[serde(rename_all = "snake_case")]
pub enum OutputFormat {
    Json,
    Text,
}

impl std::fmt::Display for OutputFormat {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Json => formatter.write_str("json"),
            Self::Text => formatter.write_str("text"),
        }
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum ConfigSource {
    Flag,
    Env,
    ConfigFile,
    Default,
}

#[derive(Clone, Debug, Serialize)]
pub struct ResolvedValue<T> {
    pub value: T,
    pub source: ConfigSource,
}

#[derive(Clone, Debug, Serialize)]
pub struct ResolvedPath {
    pub path: PathBuf,
    pub source: ConfigSource,
    pub derived_from: Option<&'static str>,
}

#[derive(Clone, Debug, Serialize)]
pub struct ConfigFileReport {
    pub path: PathBuf,
    pub exists: bool,
}

#[derive(Clone, Debug, Serialize)]
pub struct PathsDoctorReport {
    pub config_file: Option<ConfigFileReport>,
    pub home: ResolvedPath,
    pub db: ResolvedPath,
    pub invocation_log: ResolvedPath,
    pub state_file: ResolvedPath,
}

#[derive(Clone, Debug, Serialize)]
pub struct StoragePathReport {
    pub path: PathBuf,
    pub source: ConfigSource,
    pub derived_from: Option<&'static str>,
    pub exists: bool,
    pub parent_exists: bool,
}

#[derive(Clone, Debug, Serialize)]
pub struct StorageDoctorReport {
    pub db: StoragePathReport,
    pub invocation_log: StoragePathReport,
    pub state_file: StoragePathReport,
}

#[derive(Clone, Debug, Serialize)]
pub struct EnvironmentVariableReport {
    pub name: &'static str,
    pub value: Option<String>,
    pub is_set: bool,
}

#[derive(Clone, Debug, Serialize)]
pub struct EnvironmentDoctorReport {
    pub format: ResolvedValue<OutputFormat>,
    pub no_color: ResolvedValue<bool>,
    pub config_file: Option<ConfigFileReport>,
    pub variables: Vec<EnvironmentVariableReport>,
}

#[derive(Clone, Debug, Serialize)]
pub struct VersionReport {
    pub name: &'static str,
    pub version: &'static str,
    pub contract_phase: &'static str,
}
