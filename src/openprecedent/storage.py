from __future__ import annotations

import json
import sqlite3
from collections.abc import Iterable
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

from openprecedent.schemas import (
    Artifact,
    ArtifactType,
    Case,
    CaseStatus,
    Decision,
    DecisionType,
    Event,
    EventActor,
    EventType,
)


def utc_now() -> datetime:
    return datetime.now(UTC)


def _serialize_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def _parse_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


class SQLiteStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def connect(self) -> Iterable[sqlite3.Connection]:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self.connect() as connection:
            connection.executescript(
                """
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
                """
            )

    def create_case(self, case: Case) -> Case:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO cases (
                    case_id, title, status, user_id, agent_id, started_at, ended_at, final_summary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    case.case_id,
                    case.title,
                    case.status.value,
                    case.user_id,
                    case.agent_id,
                    case.started_at.isoformat(),
                    case.ended_at.isoformat() if case.ended_at else None,
                    case.final_summary,
                ),
            )
        return case

    def list_cases(self) -> list[Case]:
        with self.connect() as connection:
            rows = connection.execute(
                "SELECT * FROM cases ORDER BY started_at DESC, case_id DESC"
            ).fetchall()
        return [self._row_to_case(row) for row in rows]

    def get_case(self, case_id: str) -> Case | None:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT * FROM cases WHERE case_id = ?",
                (case_id,),
            ).fetchone()
        if row is None:
            return None
        return self._row_to_case(row)

    def append_event(self, event: Event) -> Event:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO events (
                    event_id, case_id, event_type, actor, timestamp, sequence_no,
                    parent_event_id, payload_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.case_id,
                    event.event_type.value,
                    event.actor.value,
                    event.timestamp.isoformat(),
                    event.sequence_no,
                    event.parent_event_id,
                    _serialize_json(event.payload),
                ),
            )

            if event.event_type == EventType.CASE_COMPLETED:
                connection.execute(
                    """
                    UPDATE cases
                    SET status = ?, ended_at = ?, final_summary = COALESCE(?, final_summary)
                    WHERE case_id = ?
                    """,
                    (
                        CaseStatus.COMPLETED.value,
                        event.timestamp.isoformat(),
                        _payload_summary(event.payload),
                        event.case_id,
                    ),
                )
            elif event.event_type == EventType.CASE_FAILED:
                connection.execute(
                    """
                    UPDATE cases
                    SET status = ?, ended_at = ?, final_summary = COALESCE(?, final_summary)
                    WHERE case_id = ?
                    """,
                    (
                        CaseStatus.FAILED.value,
                        event.timestamp.isoformat(),
                        _payload_summary(event.payload),
                        event.case_id,
                    ),
                )
        return event

    def list_events(self, case_id: str) -> list[Event]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM events
                WHERE case_id = ?
                ORDER BY sequence_no ASC, timestamp ASC, event_id ASC
                """,
                (case_id,),
            ).fetchall()
        return [self._row_to_event(row) for row in rows]

    def next_event_sequence(self, case_id: str) -> int:
        with self.connect() as connection:
            row = connection.execute(
                "SELECT COALESCE(MAX(sequence_no), 0) AS max_sequence FROM events WHERE case_id = ?",
                (case_id,),
            ).fetchone()
        return int(row["max_sequence"]) + 1

    def replace_decisions(self, case_id: str, decisions: list[Decision]) -> None:
        with self.connect() as connection:
            connection.execute("DELETE FROM decisions WHERE case_id = ?", (case_id,))
            for decision in decisions:
                connection.execute(
                    """
                    INSERT INTO decisions (
                        decision_id, case_id, decision_type, title, question, chosen_action,
                        alternatives_json, evidence_event_ids_json, constraint_summary,
                        requires_human_confirmation, outcome, sequence_no
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        decision.decision_id,
                        decision.case_id,
                        decision.decision_type.value,
                        decision.title,
                        decision.question,
                        decision.chosen_action,
                        _serialize_json(decision.alternatives),
                        _serialize_json(decision.evidence_event_ids),
                        decision.constraint_summary,
                        int(decision.requires_human_confirmation),
                        decision.outcome,
                        decision.sequence_no,
                    ),
                )

    def list_decisions(self, case_id: str) -> list[Decision]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM decisions
                WHERE case_id = ?
                ORDER BY sequence_no ASC, decision_id ASC
                """,
                (case_id,),
            ).fetchall()
        return [self._row_to_decision(row) for row in rows]

    def list_artifacts(self, case_id: str) -> list[Artifact]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM artifacts
                WHERE case_id = ?
                ORDER BY artifact_id ASC
                """,
                (case_id,),
            ).fetchall()
        return [self._row_to_artifact(row) for row in rows]

    def upsert_artifact(self, artifact: Artifact) -> Artifact:
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO artifacts (artifact_id, case_id, artifact_type, uri_or_path, summary)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(artifact_id) DO UPDATE SET
                    case_id = excluded.case_id,
                    artifact_type = excluded.artifact_type,
                    uri_or_path = excluded.uri_or_path,
                    summary = excluded.summary
                """,
                (
                    artifact.artifact_id,
                    artifact.case_id,
                    artifact.artifact_type.value,
                    artifact.uri_or_path,
                    artifact.summary,
                ),
            )
        return artifact

    def _row_to_case(self, row: sqlite3.Row) -> Case:
        return Case(
            case_id=row["case_id"],
            title=row["title"],
            status=CaseStatus(row["status"]),
            user_id=row["user_id"],
            agent_id=row["agent_id"],
            started_at=_parse_datetime(row["started_at"]),
            ended_at=_parse_datetime(row["ended_at"]),
            final_summary=row["final_summary"],
        )

    def _row_to_event(self, row: sqlite3.Row) -> Event:
        return Event(
            event_id=row["event_id"],
            case_id=row["case_id"],
            event_type=EventType(row["event_type"]),
            actor=EventActor(row["actor"]),
            timestamp=_parse_datetime(row["timestamp"]),
            sequence_no=row["sequence_no"],
            parent_event_id=row["parent_event_id"],
            payload=json.loads(row["payload_json"]),
        )

    def _row_to_decision(self, row: sqlite3.Row) -> Decision:
        return Decision(
            decision_id=row["decision_id"],
            case_id=row["case_id"],
            decision_type=DecisionType(row["decision_type"]),
            title=row["title"],
            question=row["question"],
            chosen_action=row["chosen_action"],
            alternatives=json.loads(row["alternatives_json"]),
            evidence_event_ids=json.loads(row["evidence_event_ids_json"]),
            constraint_summary=row["constraint_summary"],
            requires_human_confirmation=bool(row["requires_human_confirmation"]),
            outcome=row["outcome"],
            sequence_no=row["sequence_no"],
        )

    def _row_to_artifact(self, row: sqlite3.Row) -> Artifact:
        return Artifact(
            artifact_id=row["artifact_id"],
            case_id=row["case_id"],
            artifact_type=ArtifactType(row["artifact_type"]),
            uri_or_path=row["uri_or_path"],
            summary=row["summary"],
        )


def _payload_summary(payload: dict[str, object]) -> str | None:
    summary = payload.get("summary")
    if isinstance(summary, str) and summary.strip():
        return summary
    return None
