use serde::{Deserialize, Serialize};

use crate::{Artifact, Case, Decision, Event};

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct ReplayResponse {
    pub case: Case,
    pub events: Vec<Event>,
    pub decisions: Vec<Decision>,
    pub artifacts: Vec<Artifact>,
    pub summary: Option<String>,
}
