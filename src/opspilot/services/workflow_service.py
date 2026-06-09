import uuid
from ..storage.repositories import JobRepository, IncidentRepository, DeploymentRepository, EscalationRepository
from datetime import datetime, timedelta

class WorkflowService:
    def __init__(self, db_path: str | None = None):
        self.job_repo = JobRepository(db_path=db_path)
        self.inc_repo = IncidentRepository(db_path=db_path)
        self.dep_repo = DeploymentRepository(db_path=db_path)
        self.esc_repo = EscalationRepository(db_path=db_path)

    def enqueue(self, job_type: str, payload: dict):
        job = {
            'job_id': str(uuid.uuid4()),
            'job_type': job_type,
            'payload': payload,
            'status': 'queued',
            'attempts': 0,
            'next_run_at': None,
            'last_error': None,
            'idempotency_key': payload.get('idempotency_key')
        }
        self.job_repo.insert(job)
        return job

    def run_once(self):
        job = self.job_repo.next_job()
        if not job:
            return None
        try:
            # simple handlers
            if job['job_type'] == 'escalate':
                inc = self.inc_repo.get(job['payload'].get('incident_id'))
                if inc:
                    inc['assigned_team'] = 'oncall'
                    self.inc_repo.update(inc['incident_id'], inc)
            elif job['job_type'] == 'escalation_notification':
                payload = job['payload']
                escalation_id = payload.get('escalation_id')
                esc = self.esc_repo.get(escalation_id)
                if esc and esc['status'] == 'pending':
                    esc['status'] = 'notified'
                    self.esc_repo.update(escalation_id, esc)
            self.job_repo.mark_done(job['job_id'])
            return job
        except Exception as e:
            self.job_repo.mark_failed(job['job_id'], str(e))
            return None
