import sqlite3
import json
from pathlib import Path
from ..database import get_conn
from ..config import settings
from .migrations import run_migrations

class BaseRepo:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or settings.DB_PATH
        path = Path(self.db_path)
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            run_migrations(self.db_path)

    def conn(self):
        return get_conn(self.db_path)

class IncidentRepository(BaseRepo):
    def insert(self, inc: dict):
        with self.conn() as c:
            c.execute('INSERT INTO incidents (incident_id,title,description,severity,service,status,created_at,updated_at,assigned_team,tags,source,risk_score) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (
                inc['incident_id'], inc.get('title'), inc.get('description'), inc.get('severity'), inc.get('service'), inc.get('status'), inc.get('created_at'), inc.get('updated_at'), inc.get('assigned_team'), json.dumps(inc.get('tags') or []), inc.get('source'), inc.get('risk_score', 0.0)
            ))

    def get(self, incident_id: str):
        with self.conn() as c:
            r = c.execute('SELECT * FROM incidents WHERE incident_id = ?', (incident_id,)).fetchone()
            return dict(r) if r else None

    def list_all(self):
        with self.conn() as c:
            rows = c.execute('SELECT * FROM incidents ORDER BY created_at DESC').fetchall()
            return [dict(r) for r in rows]

    def update(self, incident_id: str, data: dict):
        with self.conn() as c:
            c.execute('UPDATE incidents SET title=?,description=?,severity=?,service=?,status=?,created_at=?,updated_at=?,assigned_team=?,tags=?,source=?,risk_score=? WHERE incident_id=?', (
                data.get('title'), data.get('description'), data.get('severity'), data.get('service'), data.get('status'), data.get('created_at'), data.get('updated_at'), data.get('assigned_team'), json.dumps(data.get('tags') or []), data.get('source'), data.get('risk_score',0.0), incident_id
            ))

class DeploymentRepository(BaseRepo):
    def insert(self, d: dict):
        with self.conn() as c:
            c.execute('INSERT INTO deployments (deployment_id,service,version,environment,status,started_at,finished_at,commit_sha,actor,rollback_of) VALUES (?,?,?,?,?,?,?,?,?,?)', (
                d['deployment_id'], d.get('service'), d.get('version'), d.get('environment'), d.get('status'), d.get('started_at'), d.get('finished_at'), d.get('commit_sha'), d.get('actor'), d.get('rollback_of')
            ))

    def list_all(self):
        with self.conn() as c:
            rows = c.execute('SELECT * FROM deployments ORDER BY started_at DESC').fetchall()
            return [dict(r) for r in rows]

    def get(self, deployment_id: str):
        with self.conn() as c:
            r = c.execute('SELECT * FROM deployments WHERE deployment_id = ?', (deployment_id,)).fetchone()
            return dict(r) if r else None

class LogRepository(BaseRepo):
    def insert(self, e: dict):
        with self.conn() as c:
            c.execute('INSERT INTO logs (timestamp,level,service,client_id,message,trace_id,status_code,latency_ms) VALUES (?,?,?,?,?,?,?,?)', (
                e.get('timestamp'), e.get('level'), e.get('service'), e.get('client_id'), e.get('message'), e.get('trace_id'), e.get('status_code'), e.get('latency_ms')
            ))

    def list_all(self, limit:int=100):
        with self.conn() as c:
            rows = c.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT ?', (limit,)).fetchall()
            return [dict(r) for r in rows]

class JobRepository(BaseRepo):
    def insert(self, job: dict):
        with self.conn() as c:
            c.execute('INSERT INTO jobs (job_id,job_type,payload,status,attempts,next_run_at,last_error) VALUES (?,?,?,?,?,?,?)', (
                job['job_id'], job['job_type'], json.dumps(job.get('payload') or {}), job.get('status'), job.get('attempts',0), job.get('next_run_at'), job.get('last_error')
            ))

    def next_job(self):
        with self.conn() as c:
            r = c.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY rowid ASC LIMIT 1").fetchone()
            return dict(r) if r else None

    def mark_done(self, job_id: str):
        with self.conn() as c:
            c.execute("UPDATE jobs SET status='done' WHERE job_id=?", (job_id,))

    def mark_failed(self, job_id: str, error: str):
        with self.conn() as c:
            c.execute("UPDATE jobs SET status='failed', last_error=? WHERE job_id=?", (error, job_id))

class UserRepository(BaseRepo):
    def insert(self, user: dict):
        with self.conn() as c:
            c.execute('INSERT OR REPLACE INTO users (user_id,username,role) VALUES (?,?,?)', (
                user.get('user_id'), user.get('username'), user.get('role')
            ))
