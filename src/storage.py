
import sqlite3
import uuid
import json

from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "submissions.db"


def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_db():

    with _connect() as conn:

        conn.execute("""
            CREATE TABLE IF NOT EXISTS bug_reports (
                bug_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                stack_trace TEXT,
                error_logs TEXT,
                attachment_name TEXT,
                status TEXT NOT NULL,
                category TEXT,
                priority TEXT,
                created_at TEXT NOT NULL,
                severity TEXT,
                affected_component TEXT,
                confidence_score INTEGER,
                diagnosis_json TEXT
            )
        """)

        existing_columns = {
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(bug_reports)"
            ).fetchall()
        }

        new_columns = {
            "severity": "TEXT",
            "affected_component": "TEXT",
            "confidence_score": "INTEGER",
            "diagnosis_json": "TEXT"
        }

        for column, data_type in new_columns.items():

            if column not in existing_columns:

                conn.execute(
                    f"ALTER TABLE bug_reports "
                    f"ADD COLUMN {column} {data_type}"
                )


def save_report(
    title,
    description,
    stack_trace="",
    error_logs="",
    attachment_name="",
    triage_result=None,
    diagnosis=None
):

    bug_id = str(uuid.uuid4())

    created_at = datetime.now(timezone.utc).isoformat()

    triage_result = triage_result or {}

    severity = triage_result.get("severity")
    component = triage_result.get("affected_component")
    priority = triage_result.get("priority")
    confidence = triage_result.get("confidence_score")

    diagnosis_json = json.dumps(
        diagnosis,
        ensure_ascii=False,
        default=str
    ) if diagnosis is not None else None

    with _connect() as conn:

        conn.execute("""
            INSERT INTO bug_reports (
                bug_id,
                title,
                description,
                stack_trace,
                error_logs,
                attachment_name,
                status,
                category,
                priority,
                created_at,
                severity,
                affected_component,
                confidence_score,
                diagnosis_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            bug_id,
            title,
            description,
            stack_trace,
            error_logs,
            attachment_name,
            "diagnosed",
            component,
            priority,
            created_at,
            severity,
            component,
            confidence,
            diagnosis_json
        ))

    return bug_id


def list_reports(limit=100):

    with _connect() as conn:

        conn.row_factory = sqlite3.Row

        rows = conn.execute("""
            SELECT
                bug_id,
                title,
                description,
                status,
                created_at,
                severity,
                category,
                affected_component,
                priority,
                confidence_score,
                (diagnosis_json IS NOT NULL) AS has_diagnosis
            FROM bug_reports
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,)).fetchall()

    return [dict(row) for row in rows]


def get_report(bug_id):

    with _connect() as conn:

        conn.row_factory = sqlite3.Row

        row = conn.execute("""
            SELECT *
            FROM bug_reports
            WHERE bug_id = ?
        """, (bug_id,)).fetchone()

    if row is None:
        return None

    report = dict(row)

    stored_diagnosis = report.get("diagnosis_json")

    if stored_diagnosis:

        try:
            report["diagnosis"] = json.loads(stored_diagnosis)

        except json.JSONDecodeError:
            report["diagnosis"] = None

    else:
        report["diagnosis"] = None

    return report
