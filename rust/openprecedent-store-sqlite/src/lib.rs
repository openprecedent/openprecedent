use std::fs;
use std::path::{Path, PathBuf};
use std::str::FromStr;

use chrono::{DateTime, Utc};
use openprecedent_contracts::{
    Artifact, Case, CaseStatus, Decision, DecisionExplanation, Event, EventType,
};
use rusqlite::{Connection, OptionalExtension, Row};
use serde_json::Value;

#[derive(Debug, thiserror::Error)]
pub enum SqliteStoreError {
    #[error(transparent)]
    Sqlite(#[from] rusqlite::Error),
    #[error(transparent)]
    Io(#[from] std::io::Error),
    #[error(transparent)]
    Json(#[from] serde_json::Error),
    #[error("invalid RFC3339 timestamp: {0}")]
    DateTime(String),
    #[error("invalid enum value for {kind}: {value}")]
    EnumValue { kind: &'static str, value: String },
}

pub struct SqliteStore {
    db_path: PathBuf,
}

impl SqliteStore {
    pub fn new(path: impl AsRef<Path>) -> Result<Self, SqliteStoreError> {
        let db_path = path.as_ref().to_path_buf();
        if let Some(parent) = db_path.parent() {
            fs::create_dir_all(parent)?;
        }

        let store = Self { db_path };
        store.initialize()?;
        Ok(store)
    }

    pub fn db_path(&self) -> &Path {
        &self.db_path
    }

    pub fn create_case(&self, case: &Case) -> Result<(), SqliteStoreError> {
        let connection = self.connect()?;
        connection.execute(
            "
            INSERT INTO cases (
                case_id, title, status, user_id, agent_id, started_at, ended_at, final_summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ",
            (
                &case.case_id,
                &case.title,
                case.status.to_string(),
                &case.user_id,
                &case.agent_id,
                case.started_at.to_rfc3339(),
                case.ended_at.map(|value| value.to_rfc3339()),
                &case.final_summary,
            ),
        )?;
        Ok(())
    }

    pub fn list_cases(&self) -> Result<Vec<Case>, SqliteStoreError> {
        let connection = self.connect()?;
        let mut statement =
            connection.prepare("SELECT * FROM cases ORDER BY started_at DESC, case_id DESC")?;
        let rows = statement.query_map([], Self::row_to_case)?;
        rows.collect::<Result<Vec<_>, _>>().map_err(Into::into)
    }

    pub fn get_case(&self, case_id: &str) -> Result<Option<Case>, SqliteStoreError> {
        let connection = self.connect()?;
        connection
            .query_row(
                "SELECT * FROM cases WHERE case_id = ?",
                [case_id],
                Self::row_to_case,
            )
            .optional()
            .map_err(Into::into)
    }

    pub fn find_case_id_by_openclaw_session_id(
        &self,
        session_id: &str,
    ) -> Result<Option<String>, SqliteStoreError> {
        let connection = self.connect()?;
        connection
            .query_row(
                "
                SELECT case_id
                FROM events
                WHERE event_type = ?
                  AND json_extract(payload_json, '$.session_id') = ?
                ORDER BY sequence_no ASC, event_id ASC
                LIMIT 1
                ",
                [EventType::CaseStarted.to_string(), session_id.to_string()],
                |row| row.get::<_, String>(0),
            )
            .optional()
            .map_err(Into::into)
    }

    pub fn append_event(&self, event: &Event) -> Result<(), SqliteStoreError> {
        let connection = self.connect()?;
        connection.execute(
            "
            INSERT INTO events (
                event_id, case_id, event_type, actor, timestamp, sequence_no,
                parent_event_id, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ",
            (
                &event.event_id,
                &event.case_id,
                event.event_type.to_string(),
                event.actor.to_string(),
                event.timestamp.to_rfc3339(),
                event.sequence_no,
                &event.parent_event_id,
                serde_json::to_string(&event.payload)?,
            ),
        )?;

        if matches!(
            event.event_type,
            EventType::CaseCompleted | EventType::CaseFailed
        ) {
            let status = match event.event_type {
                EventType::CaseCompleted => CaseStatus::Completed,
                EventType::CaseFailed => CaseStatus::Failed,
                _ => unreachable!(),
            };
            connection.execute(
                "
                UPDATE cases
                SET status = ?, ended_at = ?, final_summary = COALESCE(?, final_summary)
                WHERE case_id = ?
                ",
                (
                    status.to_string(),
                    event.timestamp.to_rfc3339(),
                    payload_summary(&event.payload),
                    &event.case_id,
                ),
            )?;
        }
        Ok(())
    }

    pub fn list_events(&self, case_id: &str) -> Result<Vec<Event>, SqliteStoreError> {
        let connection = self.connect()?;
        let mut statement = connection.prepare(
            "
            SELECT * FROM events
            WHERE case_id = ?
            ORDER BY sequence_no ASC, timestamp ASC, event_id ASC
            ",
        )?;
        let rows = statement.query_map([case_id], Self::row_to_event)?;
        rows.collect::<Result<Vec<_>, _>>().map_err(Into::into)
    }

    pub fn next_event_sequence(&self, case_id: &str) -> Result<i64, SqliteStoreError> {
        let connection = self.connect()?;
        let value = connection.query_row(
            "SELECT COALESCE(MAX(sequence_no), 0) AS max_sequence FROM events WHERE case_id = ?",
            [case_id],
            |row| row.get::<_, i64>(0),
        )?;
        Ok(value + 1)
    }

    pub fn replace_decisions(
        &self,
        case_id: &str,
        decisions: &[Decision],
    ) -> Result<(), SqliteStoreError> {
        let mut connection = self.connect()?;
        let transaction = connection.transaction()?;
        transaction.execute("DELETE FROM decisions WHERE case_id = ?", [case_id])?;

        for decision in decisions {
            transaction.execute(
                "
                INSERT INTO decisions (
                    decision_id, case_id, decision_type, title, question, chosen_action,
                    alternatives_json, evidence_event_ids_json, constraint_summary,
                    requires_human_confirmation, outcome, confidence, explanation_json, sequence_no
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ",
                (
                    &decision.decision_id,
                    &decision.case_id,
                    decision.decision_type.to_string(),
                    &decision.title,
                    &decision.question,
                    &decision.chosen_action,
                    serde_json::to_string(&decision.alternatives)?,
                    serde_json::to_string(&decision.evidence_event_ids)?,
                    &decision.constraint_summary,
                    decision.requires_human_confirmation as i64,
                    &decision.outcome,
                    decision.confidence,
                    serde_json::to_string(&decision.explanation)?,
                    decision.sequence_no,
                ),
            )?;
        }

        transaction.commit()?;
        Ok(())
    }

    pub fn list_decisions(&self, case_id: &str) -> Result<Vec<Decision>, SqliteStoreError> {
        let connection = self.connect()?;
        let mut statement = connection.prepare(
            "
            SELECT * FROM decisions
            WHERE case_id = ?
            ORDER BY sequence_no ASC, decision_id ASC
            ",
        )?;
        let rows = statement.query_map([case_id], Self::row_to_decision)?;
        rows.collect::<Result<Vec<_>, _>>().map_err(Into::into)
    }

    pub fn list_artifacts(&self, case_id: &str) -> Result<Vec<Artifact>, SqliteStoreError> {
        let connection = self.connect()?;
        let mut statement = connection.prepare(
            "
            SELECT * FROM artifacts
            WHERE case_id = ?
            ORDER BY artifact_id ASC
            ",
        )?;
        let rows = statement.query_map([case_id], Self::row_to_artifact)?;
        rows.collect::<Result<Vec<_>, _>>().map_err(Into::into)
    }

    pub fn upsert_artifact(&self, artifact: &Artifact) -> Result<(), SqliteStoreError> {
        let connection = self.connect()?;
        connection.execute(
            "
            INSERT INTO artifacts (artifact_id, case_id, artifact_type, uri_or_path, summary)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(artifact_id) DO UPDATE SET
                case_id = excluded.case_id,
                artifact_type = excluded.artifact_type,
                uri_or_path = excluded.uri_or_path,
                summary = excluded.summary
            ",
            (
                &artifact.artifact_id,
                &artifact.case_id,
                artifact.artifact_type.to_string(),
                &artifact.uri_or_path,
                &artifact.summary,
            ),
        )?;
        Ok(())
    }

    fn connect(&self) -> Result<Connection, SqliteStoreError> {
        let connection = Connection::open(&self.db_path)?;
        connection.execute_batch("PRAGMA foreign_keys = ON;")?;
        Ok(connection)
    }

    fn initialize(&self) -> Result<(), SqliteStoreError> {
        let connection = self.connect()?;
        connection.execute_batch(
            "
            CREATE TABLE IF NOT EXISTS cases (
                case_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                user_id TEXT,
                agent_id TEXT,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                final_summary TEXT
            );

            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                actor TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                sequence_no INTEGER NOT NULL,
                parent_event_id TEXT,
                payload_json TEXT NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(case_id)
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_events_case_sequence
            ON events(case_id, sequence_no);

            CREATE TABLE IF NOT EXISTS decisions (
                decision_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                decision_type TEXT NOT NULL,
                title TEXT NOT NULL,
                question TEXT NOT NULL,
                chosen_action TEXT NOT NULL,
                alternatives_json TEXT NOT NULL,
                evidence_event_ids_json TEXT NOT NULL,
                constraint_summary TEXT,
                requires_human_confirmation INTEGER NOT NULL,
                outcome TEXT,
                confidence REAL NOT NULL,
                explanation_json TEXT NOT NULL,
                sequence_no INTEGER NOT NULL,
                FOREIGN KEY(case_id) REFERENCES cases(case_id)
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_decisions_case_sequence
            ON decisions(case_id, sequence_no);

            CREATE TABLE IF NOT EXISTS artifacts (
                artifact_id TEXT PRIMARY KEY,
                case_id TEXT NOT NULL,
                artifact_type TEXT NOT NULL,
                uri_or_path TEXT NOT NULL,
                summary TEXT,
                FOREIGN KEY(case_id) REFERENCES cases(case_id)
            );
            ",
        )?;
        Self::ensure_column(
            &connection,
            "decisions",
            "confidence",
            "REAL NOT NULL DEFAULT 0.5",
        )?;
        Self::ensure_column(
            &connection,
            "decisions",
            "explanation_json",
            "TEXT NOT NULL DEFAULT '{}'",
        )?;
        Ok(())
    }

    fn ensure_column(
        connection: &Connection,
        table: &str,
        column: &str,
        ddl: &str,
    ) -> Result<(), SqliteStoreError> {
        let mut statement = connection.prepare(&format!("PRAGMA table_info({table})"))?;
        let rows = statement.query_map([], |row| row.get::<_, String>(1))?;
        let existing = rows.collect::<Result<Vec<_>, _>>()?;
        if existing.iter().any(|value| value == column) {
            return Ok(());
        }
        connection.execute(
            &format!("ALTER TABLE {table} ADD COLUMN {column} {ddl}"),
            [],
        )?;
        Ok(())
    }

    fn row_to_case(row: &Row<'_>) -> Result<Case, rusqlite::Error> {
        Ok(Case {
            case_id: row.get("case_id")?,
            title: row.get("title")?,
            status: parse_enum("case status", &row.get::<_, String>("status")?)?,
            user_id: row.get("user_id")?,
            agent_id: row.get("agent_id")?,
            started_at: parse_datetime(&row.get::<_, String>("started_at")?)?,
            ended_at: row
                .get::<_, Option<String>>("ended_at")?
                .map(|value| parse_datetime(&value))
                .transpose()?,
            final_summary: row.get("final_summary")?,
        })
    }

    fn row_to_event(row: &Row<'_>) -> Result<Event, rusqlite::Error> {
        Ok(Event {
            event_id: row.get("event_id")?,
            case_id: row.get("case_id")?,
            event_type: parse_enum("event type", &row.get::<_, String>("event_type")?)?,
            actor: parse_enum("event actor", &row.get::<_, String>("actor")?)?,
            timestamp: parse_datetime(&row.get::<_, String>("timestamp")?)?,
            sequence_no: row.get("sequence_no")?,
            parent_event_id: row.get("parent_event_id")?,
            payload: serde_json::from_str(&row.get::<_, String>("payload_json")?)
                .map_err(json_to_sqlite_error)?,
        })
    }

    fn row_to_decision(row: &Row<'_>) -> Result<Decision, rusqlite::Error> {
        Ok(Decision {
            decision_id: row.get("decision_id")?,
            case_id: row.get("case_id")?,
            decision_type: parse_enum("decision type", &row.get::<_, String>("decision_type")?)?,
            title: row.get("title")?,
            question: row.get("question")?,
            chosen_action: row.get("chosen_action")?,
            alternatives: serde_json::from_str(&row.get::<_, String>("alternatives_json")?)
                .map_err(json_to_sqlite_error)?,
            evidence_event_ids: serde_json::from_str(
                &row.get::<_, String>("evidence_event_ids_json")?,
            )
            .map_err(json_to_sqlite_error)?,
            constraint_summary: row.get("constraint_summary")?,
            requires_human_confirmation: row.get::<_, i64>("requires_human_confirmation")? != 0,
            outcome: row.get("outcome")?,
            confidence: row.get("confidence")?,
            explanation: serde_json::from_str::<DecisionExplanation>(
                &row.get::<_, String>("explanation_json")?,
            )
            .map_err(json_to_sqlite_error)?,
            sequence_no: row.get("sequence_no")?,
        })
    }

    fn row_to_artifact(row: &Row<'_>) -> Result<Artifact, rusqlite::Error> {
        Ok(Artifact {
            artifact_id: row.get("artifact_id")?,
            case_id: row.get("case_id")?,
            artifact_type: parse_enum("artifact type", &row.get::<_, String>("artifact_type")?)?,
            uri_or_path: row.get("uri_or_path")?,
            summary: row.get("summary")?,
        })
    }
}

fn payload_summary(payload: &Value) -> Option<String> {
    let summary = payload.get("summary")?.as_str()?;
    if summary.trim().is_empty() {
        None
    } else {
        Some(summary.to_string())
    }
}

fn parse_datetime(value: &str) -> Result<DateTime<Utc>, rusqlite::Error> {
    DateTime::parse_from_rfc3339(value)
        .map(|value| value.with_timezone(&Utc))
        .map_err(|error| {
            rusqlite::Error::FromSqlConversionFailure(
                0,
                rusqlite::types::Type::Text,
                Box::new(SqliteStoreError::DateTime(error.to_string())),
            )
        })
}

fn parse_enum<T>(kind: &'static str, value: &str) -> Result<T, rusqlite::Error>
where
    T: FromStr,
{
    T::from_str(value).map_err(|_| {
        rusqlite::Error::FromSqlConversionFailure(
            0,
            rusqlite::types::Type::Text,
            Box::new(SqliteStoreError::EnumValue {
                kind,
                value: value.to_string(),
            }),
        )
    })
}

fn json_to_sqlite_error(error: serde_json::Error) -> rusqlite::Error {
    rusqlite::Error::FromSqlConversionFailure(0, rusqlite::types::Type::Text, Box::new(error))
}

#[cfg(test)]
mod tests {
    use chrono::{TimeZone, Utc};
    use openprecedent_contracts::{
        Case, CaseStatus, Decision, DecisionExplanation, DecisionType, Event, EventType,
    };
    use rusqlite::Connection;
    use serde_json::json;
    use tempfile::tempdir;

    use super::SqliteStore;

    #[test]
    fn initializes_schema_and_roundtrips_core_records() {
        let tmp = tempdir().expect("tmp");
        let store =
            SqliteStore::new(tmp.path().join("runtime").join("openprecedent.db")).expect("store");

        let case = Case {
            case_id: "case-1".to_string(),
            title: "Rust store".to_string(),
            status: CaseStatus::Started,
            user_id: Some("user-1".to_string()),
            agent_id: Some("agent-1".to_string()),
            started_at: Utc.with_ymd_and_hms(2026, 3, 13, 10, 0, 0).unwrap(),
            ended_at: None,
            final_summary: None,
        };
        store.create_case(&case).expect("create case");

        let started_event = Event {
            event_id: "event-0".to_string(),
            case_id: case.case_id.clone(),
            event_type: EventType::CaseStarted,
            actor: openprecedent_contracts::EventActor::System,
            timestamp: Utc.with_ymd_and_hms(2026, 3, 13, 10, 0, 0).unwrap(),
            sequence_no: 1,
            parent_event_id: None,
            payload: json!({"session_id": "session-1"}),
        };
        store.append_event(&started_event).expect("append start");

        let event = Event {
            event_id: "event-1".to_string(),
            case_id: case.case_id.clone(),
            event_type: EventType::CaseCompleted,
            actor: openprecedent_contracts::EventActor::System,
            timestamp: Utc.with_ymd_and_hms(2026, 3, 13, 10, 5, 0).unwrap(),
            sequence_no: 2,
            parent_event_id: None,
            payload: json!({"summary": "done", "session_id": "session-1"}),
        };
        store.append_event(&event).expect("append event");

        let decision = Decision {
            decision_id: "decision-1".to_string(),
            case_id: case.case_id.clone(),
            decision_type: DecisionType::TaskFrameDefined,
            title: "Frame the task".to_string(),
            question: "What should be done?".to_string(),
            chosen_action: "Bootstrap the workspace".to_string(),
            alternatives: vec!["Do nothing".to_string()],
            evidence_event_ids: vec![started_event.event_id.clone(), event.event_id.clone()],
            constraint_summary: Some("Keep the CLI stable".to_string()),
            requires_human_confirmation: false,
            outcome: Some("accepted".to_string()),
            confidence: 0.9,
            explanation: DecisionExplanation {
                goal: "create the initial CLI".to_string(),
                evidence: vec!["issue scope".to_string()],
                constraints: vec!["long-term contract".to_string()],
                selection_reason: "best first slice".to_string(),
                result: Some("workspace created".to_string()),
            },
            sequence_no: 1,
        };
        store
            .replace_decisions(&case.case_id, &[decision.clone()])
            .expect("replace decisions");

        let artifact = openprecedent_contracts::Artifact {
            artifact_id: "artifact-1".to_string(),
            case_id: case.case_id.clone(),
            artifact_type: openprecedent_contracts::ArtifactType::Report,
            uri_or_path: "docs/report.md".to_string(),
            summary: Some("bootstrap report".to_string()),
        };
        store.upsert_artifact(&artifact).expect("artifact");

        assert_eq!(
            store
                .get_case(&case.case_id)
                .expect("get case")
                .unwrap()
                .status,
            CaseStatus::Completed
        );
        assert_eq!(
            store.list_events(&case.case_id).expect("events"),
            vec![started_event, event]
        );
        assert_eq!(
            store.list_decisions(&case.case_id).expect("decisions"),
            vec![decision]
        );
        assert_eq!(
            store.list_artifacts(&case.case_id).expect("artifacts"),
            vec![artifact]
        );
        assert_eq!(
            store
                .find_case_id_by_openclaw_session_id("session-1")
                .expect("session lookup"),
            Some(case.case_id.clone())
        );
        assert_eq!(
            store.next_event_sequence(&case.case_id).expect("sequence"),
            3
        );
    }

    #[test]
    fn adds_missing_decision_columns_for_legacy_schema() {
        let tmp = tempdir().expect("tmp");
        let db_path = tmp.path().join("legacy.db");
        let connection = Connection::open(&db_path).expect("legacy db");
        connection
            .execute_batch(
                "
                CREATE TABLE decisions (
                    decision_id TEXT PRIMARY KEY,
                    case_id TEXT NOT NULL,
                    decision_type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    question TEXT NOT NULL,
                    chosen_action TEXT NOT NULL,
                    alternatives_json TEXT NOT NULL,
                    evidence_event_ids_json TEXT NOT NULL,
                    constraint_summary TEXT,
                    requires_human_confirmation INTEGER NOT NULL,
                    outcome TEXT,
                    sequence_no INTEGER NOT NULL
                );
                ",
            )
            .expect("legacy schema");
        drop(connection);

        let _store = SqliteStore::new(&db_path).expect("migrated store");
        let connection = Connection::open(&db_path).expect("db");
        let mut statement = connection
            .prepare("PRAGMA table_info(decisions)")
            .expect("pragma");
        let rows = statement
            .query_map([], |row| row.get::<_, String>(1))
            .expect("rows")
            .collect::<Result<Vec<_>, _>>()
            .expect("columns");

        assert!(rows.contains(&"confidence".to_string()));
        assert!(rows.contains(&"explanation_json".to_string()));
    }
}
