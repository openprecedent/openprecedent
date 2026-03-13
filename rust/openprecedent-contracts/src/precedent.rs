use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Precedent {
    pub case_id: String,
    pub title: String,
    pub summary: String,
    pub similarity_score: i64,
    pub similarities: Vec<String>,
    pub differences: Vec<String>,
    pub reusable_takeaway: Option<String>,
    pub historical_outcome: Option<String>,
}
