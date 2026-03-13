use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use strum::{Display, EnumString};

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize, Display, EnumString)]
pub enum EventType {
    #[serde(rename = "case.started")]
    #[strum(serialize = "case.started")]
    CaseStarted,
    #[serde(rename = "checkpoint.saved")]
    #[strum(serialize = "checkpoint.saved")]
    CheckpointSaved,
    #[serde(rename = "message.user")]
    #[strum(serialize = "message.user")]
    MessageUser,
    #[serde(rename = "message.agent")]
    #[strum(serialize = "message.agent")]
    MessageAgent,
    #[serde(rename = "model.invoked")]
    #[strum(serialize = "model.invoked")]
    ModelInvoked,
    #[serde(rename = "model.completed")]
    #[strum(serialize = "model.completed")]
    ModelCompleted,
    #[serde(rename = "tool.called")]
    #[strum(serialize = "tool.called")]
    ToolCalled,
    #[serde(rename = "tool.completed")]
    #[strum(serialize = "tool.completed")]
    ToolCompleted,
    #[serde(rename = "command.started")]
    #[strum(serialize = "command.started")]
    CommandStarted,
    #[serde(rename = "command.completed")]
    #[strum(serialize = "command.completed")]
    CommandCompleted,
    #[serde(rename = "file.read")]
    #[strum(serialize = "file.read")]
    FileRead,
    #[serde(rename = "file.write")]
    #[strum(serialize = "file.write")]
    FileWrite,
    #[serde(rename = "user.confirmed")]
    #[strum(serialize = "user.confirmed")]
    UserConfirmed,
    #[serde(rename = "case.completed")]
    #[strum(serialize = "case.completed")]
    CaseCompleted,
    #[serde(rename = "case.failed")]
    #[strum(serialize = "case.failed")]
    CaseFailed,
}

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize, Display, EnumString)]
#[serde(rename_all = "snake_case")]
#[strum(serialize_all = "snake_case")]
pub enum EventActor {
    User,
    Agent,
    System,
    Tool,
}

#[derive(Clone, Debug, PartialEq, Serialize, Deserialize)]
pub struct Event {
    pub event_id: String,
    pub case_id: String,
    pub event_type: EventType,
    pub actor: EventActor,
    pub timestamp: DateTime<Utc>,
    pub sequence_no: i64,
    pub parent_event_id: Option<String>,
    pub payload: Value,
}
