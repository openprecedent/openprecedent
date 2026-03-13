use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use strum::{Display, EnumString};

#[derive(Clone, Copy, Debug, Eq, PartialEq, Serialize, Deserialize, Display, EnumString)]
#[serde(rename_all = "kebab-case")]
pub enum EventType {
    #[strum(serialize = "case.started")]
    CaseStarted,
    #[strum(serialize = "checkpoint.saved")]
    CheckpointSaved,
    #[strum(serialize = "message.user")]
    MessageUser,
    #[strum(serialize = "message.agent")]
    MessageAgent,
    #[strum(serialize = "model.invoked")]
    ModelInvoked,
    #[strum(serialize = "model.completed")]
    ModelCompleted,
    #[strum(serialize = "tool.called")]
    ToolCalled,
    #[strum(serialize = "tool.completed")]
    ToolCompleted,
    #[strum(serialize = "command.started")]
    CommandStarted,
    #[strum(serialize = "command.completed")]
    CommandCompleted,
    #[strum(serialize = "file.read")]
    FileRead,
    #[strum(serialize = "file.write")]
    FileWrite,
    #[strum(serialize = "user.confirmed")]
    UserConfirmed,
    #[strum(serialize = "case.completed")]
    CaseCompleted,
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
