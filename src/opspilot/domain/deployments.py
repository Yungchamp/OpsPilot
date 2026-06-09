from pydantic import BaseModel, Field
from datetime import datetime

class Deployment(BaseModel):
    deployment_id: str
    service: str
    version: str
    environment: str
    status: str = 'queued'
    started_at: str | None = None
    finished_at: str | None = None
    commit_sha: str | None = None
    actor: str | None = None
    rollback_of: str | None = None

    def validate_status(self):
        if self.status not in ('queued','running','succeeded','failed','rolled_back','cancelled'):
            raise ValueError('invalid status')
        return self
