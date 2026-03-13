use std::fs;
use std::path::{Path, PathBuf};

use chrono::{DateTime, TimeZone, Utc};
use serde::{Deserialize, Serialize};
use serde_json::Value;

pub const CAPTURE_RUNTIME_NAME: &str = "openclaw";

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct OpenClawSessionReference {
    pub session_id: String,
    pub transcript_path: String,
    pub updated_at: Option<DateTime<Utc>>,
    pub label: Option<String>,
    pub key: Option<String>,
    pub model: Option<String>,
    pub is_active: bool,
}

#[derive(Clone, Debug, Default, PartialEq, Eq, Serialize, Deserialize)]
pub struct OpenClawCollectionState {
    #[serde(default)]
    pub imported_session_ids: Vec<String>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct CollectedSessionResult {
    pub session_id: String,
    pub transcript_path: String,
    pub case_id: String,
    pub title: String,
    pub imported_event_count: usize,
    #[serde(default)]
    pub unsupported_record_type_counts: std::collections::BTreeMap<String, usize>,
}

#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize)]
pub struct OpenClawCollectionResult {
    pub imported: Vec<CollectedSessionResult>,
    #[serde(default)]
    pub skipped_session_ids: Vec<String>,
    pub state_path: String,
}

#[derive(Debug, thiserror::Error)]
pub enum OpenClawCaptureError {
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error(transparent)]
    Json(#[from] serde_json::Error),
}

pub fn default_sessions_root() -> PathBuf {
    let home = std::env::var_os("HOME")
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("."));
    home.join(".openclaw")
        .join("agents")
        .join("main")
        .join("sessions")
}

pub fn list_sessions(
    sessions_root: &Path,
    limit: usize,
) -> Result<Vec<OpenClawSessionReference>, OpenClawCaptureError> {
    let index_path = sessions_root.join("sessions.json");
    let mut references = Vec::new();

    if index_path.exists() {
        let raw = fs::read_to_string(&index_path)?;
        let parsed: Value = serde_json::from_str(&raw)?;
        let entries: Vec<Value> = match parsed {
            Value::Array(items) => items,
            Value::Object(map) => map.into_values().collect(),
            _ => Vec::new(),
        };

        for item in entries {
            let Value::Object(item) = item else {
                continue;
            };

            let session_id = item.get("sessionId").and_then(value_as_nonempty_string);
            let transcript_path = item
                .get("sessionFile")
                .and_then(value_as_nonempty_string)
                .or_else(|| {
                    item.get("transcriptPath")
                        .and_then(value_as_nonempty_string)
                });
            let (Some(session_id), Some(transcript_path)) = (session_id, transcript_path) else {
                continue;
            };

            let mut resolved_path = PathBuf::from(&transcript_path);
            if !resolved_path.is_absolute() {
                resolved_path = sessions_root.join(resolved_path);
            }

            references.push(OpenClawSessionReference {
                session_id,
                transcript_path: resolved_path.display().to_string(),
                updated_at: item.get("updatedAt").and_then(value_as_epoch_millis),
                label: item
                    .get("label")
                    .and_then(value_as_nonempty_string)
                    .or_else(|| item.get("displayName").and_then(value_as_nonempty_string)),
                key: item.get("key").and_then(value_as_nonempty_string),
                model: item.get("model").and_then(value_as_nonempty_string),
                is_active: item
                    .get("isActive")
                    .and_then(|value| value.as_bool())
                    .unwrap_or(false),
            });
        }
    } else {
        let mut paths = fs::read_dir(sessions_root)?
            .filter_map(Result::ok)
            .map(|entry| entry.path())
            .filter(|path| path.extension().and_then(|item| item.to_str()) == Some("jsonl"))
            .collect::<Vec<_>>();
        paths.sort();
        for transcript_path in paths {
            let metadata = fs::metadata(&transcript_path)?;
            let updated_at = metadata.modified().ok().map(DateTime::<Utc>::from);
            let session_id = transcript_path
                .file_stem()
                .and_then(|item| item.to_str())
                .unwrap_or_default()
                .to_string();
            references.push(OpenClawSessionReference {
                session_id: session_id.clone(),
                transcript_path: transcript_path.display().to_string(),
                updated_at,
                label: Some(session_id),
                key: None,
                model: None,
                is_active: false,
            });
        }
    }

    references.sort_by(|left, right| {
        right
            .updated_at
            .unwrap_or_else(epoch)
            .cmp(&left.updated_at.unwrap_or_else(epoch))
            .then_with(|| right.session_id.cmp(&left.session_id))
    });
    if references.len() > limit {
        references.truncate(limit);
    }
    Ok(references)
}

pub fn load_collection_state(
    state_path: &Path,
) -> Result<OpenClawCollectionState, OpenClawCaptureError> {
    if !state_path.exists() {
        return Ok(OpenClawCollectionState::default());
    }
    Ok(serde_json::from_str(&fs::read_to_string(state_path)?)?)
}

pub fn write_collection_state(
    state_path: &Path,
    state: &OpenClawCollectionState,
) -> Result<(), OpenClawCaptureError> {
    if let Some(parent) = state_path.parent() {
        fs::create_dir_all(parent)?;
    }
    fs::write(state_path, serde_json::to_string_pretty(state)?)?;
    Ok(())
}

pub fn case_id_for_session(session_id: &str) -> String {
    let normalized = session_id
        .chars()
        .filter(|ch| ch.is_ascii_alphanumeric())
        .collect::<String>()
        .to_ascii_lowercase();
    format!("openclaw_{}", &normalized[..normalized.len().min(24)])
}

fn value_as_nonempty_string(value: &Value) -> Option<String> {
    match value {
        Value::String(value) if !value.trim().is_empty() => Some(value.clone()),
        _ => None,
    }
}

fn value_as_epoch_millis(value: &Value) -> Option<DateTime<Utc>> {
    value
        .as_i64()
        .and_then(|millis| Utc.timestamp_millis_opt(millis).single())
}

fn epoch() -> DateTime<Utc> {
    Utc.timestamp_opt(0, 0).single().expect("unix epoch")
}
