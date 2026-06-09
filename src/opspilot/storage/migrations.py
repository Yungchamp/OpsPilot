import sqlite3
from pathlib import Path

SCHEMA = {
    'incidents': '''CREATE TABLE IF NOT EXISTS incidents (
        incident_id TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        severity TEXT,
        service TEXT,
        status TEXT,
        created_at TEXT,
        updated_at TEXT,
        assigned_team TEXT,
        tags TEXT,
        source TEXT,
        risk_score REAL
    )''',
    'deployments': '''CREATE TABLE IF NOT EXISTS deployments (
        deployment_id TEXT PRIMARY KEY,
        service TEXT,
        version TEXT,
        environment TEXT,
        status TEXT,
        started_at TEXT,
        finished_at TEXT,
        commit_sha TEXT,
        actor TEXT,
        rollback_of TEXT
    )''',
    'logs': '''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        level TEXT,
        service TEXT,
        client_id TEXT,
        message TEXT,
        trace_id TEXT,
        status_code INTEGER,
        latency_ms REAL
    )''',
    'jobs': '''CREATE TABLE IF NOT EXISTS jobs (
        job_id TEXT PRIMARY KEY,
        job_type TEXT,
        payload TEXT,
        status TEXT,
        attempts INTEGER,
        next_run_at TEXT,
        last_error TEXT
    )''',
    'users': '''CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT,
        role TEXT
    )'''
}


def run_migrations(db_path: str):
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for name, sql in SCHEMA.items():
        cur.execute(sql)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    import sys
    run_migrations(sys.argv[1] if len(sys.argv) > 1 else 'data/opspilot.db')
