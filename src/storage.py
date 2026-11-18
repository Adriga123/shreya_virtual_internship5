import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "submissions.db"

def _connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)

def initialize_db():
    with _connect() as conn:
        conn.execute('''
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
                created_at TEXT NOT NULL
            )
        ''')

def save_report(title, description, stack_trace="", error_logs="", attachment_name=""):
    bug_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    with _connect() as conn:
        conn.execute('''
            INSERT INTO bug_reports
            (bug_id, title, description, stack_trace, error_logs, attachment_name,
             status, category, priority, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (bug_id, title, description, stack_trace, error_logs, attachment_name,
              "diagnosed", None, None, created_at))
    return bug_id

def list_reports(limit=10):
    with _connect() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT bug_id, title, status, created_at FROM bug_reports ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [dict(row) for row in rows]
