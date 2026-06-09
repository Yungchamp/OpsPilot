from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Incident(BaseModel):
    incident_id: str
    title: str
    description: str
    severity: str
    service: str
    status: str = 'new'
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    updated_at: str | None = None
    assigned_team: str | None = None
    tags: List[str] = []
    source: str | None = None
    risk_score: float = 0.0

    def normalize(self):
        self.severity = self.severity.lower()
        if self.status not in ('new','triaging','investigating','mitigated','resolved','closed'):
            raise ValueError('invalid status')
        return self
