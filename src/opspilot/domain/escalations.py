from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime

class Escalation(BaseModel):
    escalation_id: str
    incident_id: str
    severity: str
    assigned_team: str
    reason: str
    status: str = 'pending'
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    acknowledged_at: str | None = None
    resolved_at: str | None = None
    notification_targets: List[str] = []
    service: str | None = None

    @validator('severity', pre=True, always=True)
    def normalize_severity(cls, value):
        return (value or '').lower()

    @validator('status', pre=True, always=True)
    def validate_status(cls, value):
        if value not in ('pending', 'notified', 'acknowledged', 'resolved', 'cancelled'):
            raise ValueError('invalid escalation status')
        return value

    def is_active(self):
        return self.status in ('pending', 'notified', 'acknowledged')
