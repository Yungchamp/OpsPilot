from opspilot.storage.migrations import run_migrations
from opspilot.services.deployment_service import DeploymentService
from pathlib import Path
import tempfile


def test_deployment_create(tmp_path):
    db = tmp_path / 'd.db'
    run_migrations(str(db))
    svc = DeploymentService(db_path=str(db))
    d = {'deployment_id':'DEP-1','service':'svc','version':'v1','environment':'prod'}
    out = svc.create(d)
    assert out['deployment_id']=='DEP-1'
