use serde::{Deserialize, Serialize};
use strum::{Display, EnumString};

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize, Display, EnumString)]
#[serde(rename_all = "snake_case")]
#[strum(serialize_all = "snake_case")]
pub enum ArtifactType {
    File,
    CommandOutput,
    Message,
    Report,
    Patch,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Artifact {
    pub artifact_id: String,
    pub case_id: String,
    pub artifact_type: ArtifactType,
    pub uri_or_path: String,
    pub summary: Option<String>,
}
