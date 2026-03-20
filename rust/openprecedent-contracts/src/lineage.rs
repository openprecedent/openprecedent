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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn query_reason_display_matches_cli_values() {
        assert_eq!(
            DecisionLineageQueryReason::InitialPlanning.to_string(),
            "initial_planning"
        );
        assert_eq!(
            DecisionLineageQueryReason::BeforeFileWrite.to_string(),
            "before_file_write"
        );
        assert_eq!(
            DecisionLineageQueryReason::AfterFailure.to_string(),
            "after_failure"
        );
        assert_eq!(DecisionLineageQueryReason::Manual.to_string(), "manual");
    }

    #[test]
    fn lineage_structs_round_trip_through_json() {
        let brief = DecisionLineageBrief {
            query_reason: DecisionLineageQueryReason::InitialPlanning,
            task_summary: "Plan the MVP release".to_string(),
            suggested_focus: Some("release scope".to_string()),
            matched_cases: vec![DecisionLineageMatchedCase {
                case_id: "case_release".to_string(),
                title: "Release baseline".to_string(),
                similarity_score: 7,
                summary: "A prior release baseline".to_string(),
            }],
            task_frame: Some("Define the release scope".to_string()),
            accepted_constraints: vec!["stay local-first".to_string()],
            success_criteria: vec!["release docs are aligned".to_string()],
            rejected_options: vec!["do not broaden runtime support".to_string()],
            authority_signals: vec!["MVP status note".to_string()],
            cautions: vec!["do not overstate maturity".to_string()],
        };

        let serialized = serde_json::to_string(&brief).expect("serialize brief");
        let restored: DecisionLineageBrief =
            serde_json::from_str(&serialized).expect("deserialize brief");

        assert_eq!(restored, brief);
    }
}
