use chrono::{DateTime, Utc};
use clap::ValueEnum;
use serde::{Deserialize, Serialize};

use crate::{Decision, Event};

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize, ValueEnum)]
#[serde(rename_all = "snake_case")]
pub enum DecisionLineageQueryReason {
    #[value(name = "initial_planning")]
    InitialPlanning,
    #[value(name = "before_file_write")]
    BeforeFileWrite,
    #[value(name = "after_failure")]
    AfterFailure,
    #[value(name = "manual")]
    Manual,
}

impl std::fmt::Display for DecisionLineageQueryReason {
    fn fmt(&self, formatter: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        formatter.write_str(match self {
            Self::InitialPlanning => "initial_planning",
            Self::BeforeFileWrite => "before_file_write",
            Self::AfterFailure => "after_failure",
            Self::Manual => "manual",
        })
    }
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DecisionLineageMatchedCase {
    pub case_id: String,
    pub title: String,
    pub similarity_score: i64,
    pub summary: String,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DecisionLineageBrief {
    pub query_reason: DecisionLineageQueryReason,
    pub task_summary: String,
    pub suggested_focus: Option<String>,
    pub matched_cases: Vec<DecisionLineageMatchedCase>,
    pub task_frame: Option<String>,
    #[serde(default)]
    pub accepted_constraints: Vec<String>,
    #[serde(default)]
    pub success_criteria: Vec<String>,
    #[serde(default)]
    pub rejected_options: Vec<String>,
    #[serde(default)]
    pub authority_signals: Vec<String>,
    #[serde(default)]
    pub cautions: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct RuntimeDecisionLineageInvocation {
    pub invocation_id: String,
    pub recorded_at: DateTime<Utc>,
    pub query_reason: DecisionLineageQueryReason,
    pub task_summary: String,
    pub current_plan: Option<String>,
    pub candidate_action: Option<String>,
    #[serde(default)]
    pub known_files: Vec<String>,
    pub case_id: Option<String>,
    pub session_id: Option<String>,
    #[serde(default)]
    pub matched_case_ids: Vec<String>,
    pub task_frame: Option<String>,
    #[serde(default)]
    pub accepted_constraints: Vec<String>,
    #[serde(default)]
    pub success_criteria: Vec<String>,
    #[serde(default)]
    pub rejected_options: Vec<String>,
    #[serde(default)]
    pub authority_signals: Vec<String>,
    #[serde(default)]
    pub cautions: Vec<String>,
    pub suggested_focus: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct RuntimeDecisionLineageInspection {
    pub invocation: RuntimeDecisionLineageInvocation,
    #[serde(default)]
    pub downstream_events: Vec<Event>,
    #[serde(default)]
    pub downstream_decisions: Vec<Decision>,
}
