import uuid
from datetime import datetime, timedelta
from ..storage.repositories import EscalationRepository, IncidentRepository, DeploymentRepository, JobRepository
from ..domain.escalations import Escalation
from ..services.notification_service import NotificationService
from ..config import settings

class EscalationService:
    def __init__(self, db_path: str | None = None):
        self.escalation_repo = EscalationRepository(db_path=db_path)
        self.inc_repo = IncidentRepository(db_path=db_path)
        self.dep_repo = DeploymentRepository(db_path=db_path)
        self.job_repo = JobRepository(db_path=db_path)
        self.notification = NotificationService()

    def list(self):
        return self.escalation_repo.list_all()

    def get(self, escalation_id: str):
        return self.escalation_repo.get(escalation_id)

    def acknowledge(self, escalation_id: str):
        esc = self.escalation_repo.get(escalation_id)
        if not esc:
            raise ValueError('not found')
        if esc['status'] not in ('pending','notified'):
            raise ValueError('cannot acknowledge')
        esc['status'] = 'acknowledged'
        esc['acknowledged_at'] = datetime.utcnow().isoformat() + 'Z'
        self.escalation_repo.update(escalation_id, esc)
        return esc

    def resolve(self, escalation_id: str):
        esc = self.escalation_repo.get(escalation_id)
        if not esc:
            raise ValueError('not found')
        if esc['status'] == 'resolved':
            return esc
        esc['status'] = 'resolved'
        esc['resolved_at'] = datetime.utcnow().isoformat() + 'Z'
        self.escalation_repo.update(escalation_id, esc)
        return esc

    def create_for_incident(self, incident_id: str, reason: str | None = None):
        inc = self.inc_repo.get(incident_id)
        if not inc:
            raise ValueError('incident not found')
        if inc['status'] in ('resolved', 'closed'):
            raise ValueError('resolved incidents cannot be escalated')
        active = self.escalation_repo.active_for_incident(incident_id)
        if active:
            raise ValueError('active escalation exists')
        escalation_needed, reason_text = self._evaluate_escalation_rules(inc, reason)
        if not escalation_needed:
            raise ValueError('no escalation criteria met')
        esc_id = f"ESC-{uuid.uuid4()}"
        esc = Escalation(
            escalation_id=esc_id,
            incident_id=incident_id,
            severity=inc['severity'],
            assigned_team=self._assign_team(inc),
            reason=reason_text,
            status='pending',
            notification_targets=self._build_targets(inc),
            service=inc.get('service'),
        )
        self.escalation_repo.insert(dict(esc))
        payload = self.notification.prepare_escalation_payload(dict(esc))
        job = {
            'job_id': str(uuid.uuid4()),
            'job_type': 'escalation_notification',
            'payload': payload,
            'status': 'queued',
            'attempts': 0,
            'next_run_at': None,
            'last_error': None,
            'idempotency_key': f"notification:{esc_id}",
        }
        self.job_repo.insert(job)
        return {'escalation': dict(esc), 'notification_payload': payload}

    def evaluate_and_escalate(self, incident_id: str):
        try:
            return self.create_for_incident(incident_id)
        except ValueError:
            return None

    def _assign_team(self, incident: dict) -> str:
        severity = incident.get('severity', '').lower()
        if severity == 'critical':
            return 'oncall'
        if severity == 'high':
            return 'devops'
        if severity == 'medium':
            return 'engineering'
        return 'operations'

    def _build_targets(self, incident: dict) -> list:
        team = self._assign_team(incident)
        primary = f"{team}@ops.example.com"
        return [primary]

    def _incident_age_minutes(self, incident: dict) -> float:
        created = datetime.fromisoformat(incident['created_at'].replace('Z',''))
        return (datetime.utcnow() - created).total_seconds() / 60.0

    def _evaluate_escalation_rules(self, incident: dict, explicit_reason: str | None) -> tuple[bool,str]:
        if incident['severity'].lower() == 'critical':
            return True, explicit_reason or 'critical incident requires immediate escalation'
        if self._failed_deployments_for_service(incident.get('service')) >= settings.ESCALATION_REPEATED_FAILURES:
            return True, explicit_reason or 'repeated failed deployments for service'
        if incident.get('risk_score', 0.0) >= settings.ESCALATION_HIGH_RISK_SCORE:
            age_min = self._incident_age_minutes(incident)
            if age_min >= settings.ESCALATION_HIGH_RISK_DELAY_MINUTES:
                return True, explicit_reason or 'high-risk incident exceeded escalation threshold'
        return False, explicit_reason or 'no escalation threshold met'

    def _failed_deployments_for_service(self, service: str | None) -> int:
        if not service:
            return 0
        deployments = self.dep_repo.list_all()
        return sum(1 for d in deployments if d.get('service') == service and d.get('status') == 'failed')
