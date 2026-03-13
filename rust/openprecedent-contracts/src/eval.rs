use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

use crate::DecisionType;

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct EvaluationCaseResult {
    pub case_id: String,
    pub expected_decision_types: Vec<DecisionType>,
    pub actual_decision_types: Vec<DecisionType>,
    pub missing_decision_types: Vec<DecisionType>,
    pub extra_decision_types: Vec<DecisionType>,
    pub expected_precedent_case_ids: Vec<String>,
    pub actual_precedent_case_ids: Vec<String>,
    pub missing_precedent_case_ids: Vec<String>,
    pub passed: bool,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct EvaluationReport {
    pub total_cases: usize,
    pub passed_cases: usize,
    pub failed_cases: usize,
    pub results: Vec<EvaluationCaseResult>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct CollectedSessionEvaluationResult {
    pub session_id: String,
    pub case_id: String,
    pub title: String,
    pub transcript_path: String,
    pub status: String,
    pub event_count: usize,
    pub decision_count: usize,
    pub precedent_count: usize,
    pub top_precedent_case_id: Option<String>,
    pub top_precedent_score: Option<i64>,
    pub has_file_write: bool,
    pub has_recovery: bool,
    pub final_summary: Option<String>,
    #[serde(default)]
    pub unsupported_record_type_counts: std::collections::BTreeMap<String, usize>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct CollectedSessionEvaluationReport {
    pub generated_at: DateTime<Utc>,
    pub sessions_root: String,
    pub state_path: String,
    pub total_sessions: usize,
    pub evaluated_cases: usize,
    pub completed_cases: usize,
    pub failed_cases: usize,
    pub cases_with_precedents: usize,
    pub cases_with_file_writes: usize,
    pub cases_with_recovery: usize,
    pub average_event_count: f64,
    pub average_decision_count: f64,
    pub decision_type_counts: std::collections::BTreeMap<String, usize>,
    #[serde(default)]
    pub unsupported_record_type_counts: std::collections::BTreeMap<String, usize>,
    #[serde(default)]
    pub missing_session_ids: Vec<String>,
    pub results: Vec<CollectedSessionEvaluationResult>,
}
