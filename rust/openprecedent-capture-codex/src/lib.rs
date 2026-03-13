use std::path::Path;

use chrono::{DateTime, Utc};
use openprecedent_contracts::{Event, EventActor, EventType};
use serde_json::{Map, Value};

pub const CAPTURE_RUNTIME_NAME: &str = "codex";

#[derive(Debug, thiserror::Error)]
pub enum CodexCaptureError {
    #[error("line {line_no}: {message}")]
    InvalidRecord { line_no: usize, message: String },
}

pub fn rollout_id_prefix(path: &Path) -> String {
    let mut slug = String::new();
    for ch in path
        .file_stem()
        .and_then(|item| item.to_str())
        .unwrap_or_default()
        .chars()
    {
        if ch.is_ascii_alphanumeric() {
            slug.push(ch.to_ascii_lowercase());
        } else if !slug.ends_with('-') {
            slug.push('-');
        }
    }
    let slug = slug.trim_matches('-').to_string();
    if slug.is_empty() {
        "codex-rollout".to_string()
    } else {
        slug
    }
}

pub fn record_type(raw_item: &Map<String, Value>) -> String {
    let kind = raw_item
        .get("type")
        .and_then(Value::as_str)
        .unwrap_or("unknown");
    let subtype = raw_item
        .get("payload")
        .and_then(Value::as_object)
        .and_then(|payload| payload.get("type"))
        .and_then(Value::as_str);
    match subtype {
        Some(subtype) => format!("{kind}:{subtype}"),
        None => kind.to_string(),
    }
}

pub fn normalize_rollout_line(
    raw_item: Map<String, Value>,
    line_no: usize,
    rollout_id_prefix: &str,
) -> Result<Option<Event>, CodexCaptureError> {
    let kind = raw_item
        .get("type")
        .and_then(Value::as_str)
        .ok_or_else(|| invalid(line_no, "type is required for codex rollout import"))?;
    let timestamp = parse_optional_timestamp(raw_item.get("timestamp"), line_no)?;
    let payload = raw_item
        .get("payload")
        .and_then(Value::as_object)
        .cloned()
        .unwrap_or_default();

    match kind {
        "session_meta" => Ok(Some(Event {
            event_id: payload
                .get("id")
                .and_then(value_as_nonempty_string)
                .unwrap_or_else(|| format!("{rollout_id_prefix}-session-{line_no}")),
            case_id: String::new(),
            event_type: EventType::CaseStarted,
            actor: EventActor::System,
            timestamp: timestamp.unwrap_or_else(Utc::now),
            sequence_no: 0,
            parent_event_id: None,
            payload: json_object([
                ("source", Value::String(CAPTURE_RUNTIME_NAME.to_string())),
                (
                    "session_id",
                    payload
                        .get("id")
                        .and_then(value_as_nonempty_string)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                (
                    "cwd",
                    payload
                        .get("cwd")
                        .and_then(value_as_nonempty_string)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                (
                    "originator",
                    payload
                        .get("originator")
                        .and_then(value_as_nonempty_string)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                (
                    "cli_version",
                    payload
                        .get("cli_version")
                        .and_then(value_as_nonempty_string)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
                (
                    "model_provider",
                    payload
                        .get("model_provider")
                        .and_then(value_as_nonempty_string)
                        .map(Value::String)
                        .unwrap_or(Value::Null),
                ),
            ]),
        })),
        "event_msg" => match payload
            .get("type")
            .and_then(value_as_nonempty_string)
            .as_deref()
        {
            Some("user_message") => Ok(Some(Event {
                event_id: format!("{rollout_id_prefix}-user-{line_no}"),
                case_id: String::new(),
                event_type: EventType::MessageUser,
                actor: EventActor::User,
                timestamp: timestamp.unwrap_or_else(Utc::now),
                sequence_no: 0,
                parent_event_id: None,
                payload: json_object([
                    (
                        "message",
                        Value::String(
                            payload
                                .get("message")
                                .and_then(Value::as_str)
                                .unwrap_or_default()
                                .to_string(),
                        ),
                    ),
                    ("source", Value::String(CAPTURE_RUNTIME_NAME.to_string())),
                ]),
            })),
            Some("agent_message") => Ok(Some(Event {
                event_id: format!("{rollout_id_prefix}-agent-{line_no}"),
                case_id: String::new(),
                event_type: EventType::MessageAgent,
                actor: EventActor::Agent,
                timestamp: timestamp.unwrap_or_else(Utc::now),
                sequence_no: 0,
                parent_event_id: None,
                payload: json_object([
                    (
                        "message",
                        Value::String(
                            payload
                                .get("message")
                                .and_then(Value::as_str)
                                .unwrap_or_default()
                                .to_string(),
                        ),
                    ),
                    (
                        "phase",
                        payload
                            .get("phase")
                            .and_then(value_as_nonempty_string)
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    ("source", Value::String(CAPTURE_RUNTIME_NAME.to_string())),
                ]),
            })),
            Some("task_complete") => Ok(Some(Event {
                event_id: format!("{rollout_id_prefix}-complete-{line_no}"),
                case_id: String::new(),
                event_type: EventType::CaseCompleted,
                actor: EventActor::System,
                timestamp: timestamp.unwrap_or_else(Utc::now),
                sequence_no: 0,
                parent_event_id: None,
                payload: json_object([
                    (
                        "summary",
                        Value::String(
                            payload
                                .get("last_agent_message")
                                .and_then(value_as_nonempty_string)
                                .unwrap_or_else(|| "Codex task completed".to_string()),
                        ),
                    ),
                    (
                        "turn_id",
                        payload
                            .get("turn_id")
                            .and_then(value_as_nonempty_string)
                            .map(Value::String)
                            .unwrap_or(Value::Null),
                    ),
                    ("source", Value::String(CAPTURE_RUNTIME_NAME.to_string())),
                ]),
            })),
            _ => Ok(None),
        },
        "response_item" => match payload
            .get("type")
            .and_then(value_as_nonempty_string)
            .as_deref()
        {
            Some("function_call") | Some("custom_tool_call") | Some("web_search_call") => {
                let subtype = payload
                    .get("type")
                    .and_then(value_as_nonempty_string)
                    .unwrap_or_else(|| "function_call".to_string());
                let tool_name = payload
                    .get("name")
                    .and_then(value_as_nonempty_string)
                    .unwrap_or(subtype);
                let call_id = payload.get("call_id").and_then(value_as_nonempty_string);
                Ok(Some(Event {
                    event_id: call_id
                        .clone()
                        .unwrap_or_else(|| format!("{rollout_id_prefix}-tool-call-{line_no}")),
                    case_id: String::new(),
                    event_type: EventType::ToolCalled,
                    actor: EventActor::Agent,
                    timestamp: timestamp.unwrap_or_else(Utc::now),
                    sequence_no: 0,
                    parent_event_id: None,
                    payload: json_object([
                        ("tool_name", Value::String(tool_name.clone())),
                        (
                            "arguments",
                            normalize_tool_arguments(
                                &tool_name,
                                arguments_to_payload(payload.get("arguments")),
                            ),
                        ),
                        ("call_id", call_id.map(Value::String).unwrap_or(Value::Null)),
                        ("source", Value::String(CAPTURE_RUNTIME_NAME.to_string())),
                    ]),
                }))
            }
            Some("function_call_output") | Some("custom_tool_call_output") => {
                let call_id = payload.get("call_id").and_then(value_as_nonempty_string);
                Ok(Some(Event {
                    event_id: format!(
                        "{}-output",
                        call_id.clone().unwrap_or_else(|| format!(
                            "{rollout_id_prefix}-tool-output-{line_no}"
                        ))
                    ),
                    case_id: String::new(),
                    event_type: EventType::ToolCompleted,
                    actor: EventActor::Tool,
                    timestamp: timestamp.unwrap_or_else(Utc::now),
                    sequence_no: 0,
                    parent_event_id: None,
                    payload: json_object([
                        ("call_id", call_id.map(Value::String).unwrap_or(Value::Null)),
                        (
                            "output",
                            Value::String(strip_tool_output_noise(
                                payload
                                    .get("output")
                                    .and_then(Value::as_str)
                                    .unwrap_or_default(),
                            )),
                        ),
                        ("source", Value::String(CAPTURE_RUNTIME_NAME.to_string())),
                    ]),
                }))
            }
            _ => Ok(None),
        },
        _ => Ok(None),
    }
}

fn invalid(line_no: usize, message: impl Into<String>) -> CodexCaptureError {
    CodexCaptureError::InvalidRecord {
        line_no,
        message: message.into(),
    }
}

fn parse_optional_timestamp(
    value: Option<&Value>,
    line_no: usize,
) -> Result<Option<DateTime<Utc>>, CodexCaptureError> {
    let Some(value) = value else {
        return Ok(None);
    };
    let Some(value) = value.as_str() else {
        return Err(invalid(line_no, "timestamp must be an ISO-8601 string"));
    };
    DateTime::parse_from_rfc3339(value)
        .map(|value| Some(value.with_timezone(&Utc)))
        .map_err(|error| invalid(line_no, error.to_string()))
}

fn arguments_to_payload(value: Option<&Value>) -> Map<String, Value> {
    match value {
        Some(Value::Object(value)) => value.clone(),
        Some(Value::String(value)) if !value.trim().is_empty() => {
            match serde_json::from_str::<Value>(value) {
                Ok(Value::Object(parsed)) => parsed,
                _ => {
                    let mut map = Map::new();
                    map.insert("raw".to_string(), Value::String(value.clone()));
                    map
                }
            }
        }
        _ => Map::new(),
    }
}

fn normalize_tool_arguments(tool_name: &str, arguments: Map<String, Value>) -> Value {
    if arguments.is_empty() {
        return Value::Object(Map::new());
    }

    let mut cleaned = arguments;
    for key in [
        "yield_time_ms",
        "max_output_tokens",
        "sandbox_permissions",
        "justification",
        "prefix_rule",
        "login",
        "tty",
        "shell",
    ] {
        cleaned.remove(key);
    }

    if tool_name == "exec_command" {
        return Value::Object(cleaned);
    }
    Value::Object(cleaned)
}

fn strip_tool_output_noise(output: &str) -> String {
    if output.trim().is_empty() {
        return output.to_string();
    }

    let mut lines = output.lines().collect::<Vec<_>>();
    while lines.first().is_some_and(|line| {
        line.starts_with("Chunk ID:")
            || line.starts_with("Wall time:")
            || line.starts_with("Process exited with code")
            || line.starts_with("Original token count:")
    }) {
        lines.remove(0);
    }
    if lines.first().is_some_and(|line| *line == "Output:") {
        lines.remove(0);
    }
    lines.join("\n").trim().to_string()
}

fn value_as_nonempty_string(value: &Value) -> Option<String> {
    match value {
        Value::String(value) if !value.trim().is_empty() => Some(value.clone()),
        _ => None,
    }
}

fn json_object<const N: usize>(pairs: [(&str, Value); N]) -> Value {
    let mut map = Map::new();
    for (key, value) in pairs {
        map.insert(key.to_string(), value);
    }
    Value::Object(map)
}
