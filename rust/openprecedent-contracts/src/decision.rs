use serde::{Deserialize, Serialize};
use strum::{Display, EnumString};

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize, Display, EnumString)]
#[serde(rename_all = "snake_case")]
#[strum(serialize_all = "snake_case")]
pub enum DecisionType {
    TaskFrameDefined,
    ConstraintAdopted,
    SuccessCriteriaSet,
    ClarificationResolved,
    OptionRejected,
    AuthorityConfirmed,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct DecisionExplanation {
    pub goal: String,
    pub evidence: Vec<String>,
    pub constraints: Vec<String>,
    pub selection_reason: String,
    pub result: Option<String>,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Decision {
    pub decision_id: String,
    pub case_id: String,
    pub decision_type: DecisionType,
    pub title: String,
    pub question: String,
    pub chosen_action: String,
    pub alternatives: Vec<String>,
    pub evidence_event_ids: Vec<String>,
    pub constraint_summary: Option<String>,
    pub requires_human_confirmation: bool,
    pub outcome: Option<String>,
    pub confidence: f64,
    pub explanation: DecisionExplanation,
    pub sequence_no: i64,
}
