from ..storage.repositories import IncidentRepository
from ..domain.incidents import Incident
from ..domain.risk import compute_risk
from ..domain.ai_triage import MockAIProvider
from datetime import datetime
import json

class IncidentService:
    def __init__(self, db_path: str | None = None):
        self.repo = IncidentRepository(db_path=db_path)
        self.ai = MockAIProvider()

    def list(self):
        return self.repo.list_all()

    def create(self, data: dict):
        inc = Incident(**data)
        inc.normalize()
        if self.repo.get(inc.incident_id):
            raise ValueError('duplicate incident_id')
        inc.created_at = datetime.utcnow().isoformat() + 'Z'
        inc.updated_at = inc.created_at
        self.repo.insert(dict(inc))
        return dict(inc)

    def get(self, incident_id: str):
        return self.repo.get(incident_id)

    def transition(self, incident_id: str, new_status: str):
        inc = self.repo.get(incident_id)
        if not inc:
            raise ValueError('not found')
        allowed = {
            'new': ['triaging','closed'],
            'triaging': ['investigating','resolved'],
            'investigating': ['mitigated','resolved'],
            'mitigated': ['resolved','closed'],
            'resolved': ['closed'],
            'closed': []
        }
        cur = inc['status']
        if new_status not in allowed.get(cur, []):
            raise ValueError('invalid transition')
        inc['status'] = new_status
        inc['updated_at'] = datetime.utcnow().isoformat() + 'Z'
        self.repo.update(incident_id, inc)
        return inc

    def triage(self, incident_id: str):
        inc = self.repo.get(incident_id)
        if not inc:
            raise ValueError('not found')
        return self.ai.triage(inc['description'] or '')

    def score(self, incident_id: str):
        inc = self.repo.get(incident_id)
        if not inc:
            raise ValueError('not found')
        # simple aggregated metrics: placeholders
        score, reasons = compute_risk(inc.get('severity','medium'), 3, True, 0, 1, 24, 1)
        inc['risk_score'] = score
        self.repo.update(incident_id, inc)
        return {'score': score, 'reasons': reasons}
