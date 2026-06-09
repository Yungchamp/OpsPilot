from ..storage.repositories import DeploymentRepository
from ..domain.deployments import Deployment
from datetime import datetime

class DeploymentService:
    def __init__(self, db_path: str | None = None):
        self.repo = DeploymentRepository(db_path=db_path)

    def list(self):
        return self.repo.list_all()

    def create(self, data: dict):
        d = Deployment(**data)
        d.validate_status()
        d.started_at = datetime.utcnow().isoformat() + 'Z'
        d.finished_at = datetime.utcnow().isoformat() + 'Z'
        self.repo.insert(dict(d))
        return dict(d)
