import json
from pathlib import Path
from .migrations import run_migrations
from ..storage.repositories import IncidentRepository, DeploymentRepository, EscalationRepository

ROOT = Path(__file__).resolve().parents[3]


def seed_demo(db_path: str):
    run_migrations(db_path)
    repo = IncidentRepository(db_path=db_path)
    dep_repo = DeploymentRepository(db_path=db_path)
    data_dir = ROOT / 'data' / 'samples'
    try:
        with open(data_dir / 'incidents.json') as f:
            incs = json.load(f)
        for i in incs:
            try:
                repo.insert(i)
            except Exception:
                pass
    except FileNotFoundError:
        pass
    try:
        with open(data_dir / 'deployments.json') as f:
            deps = json.load(f)
        for d in deps:
            try:
                dep_repo.insert(d)
            except Exception:
                pass
    except FileNotFoundError:
        pass
    try:
        with open(data_dir / 'escalations.json') as f:
            escs = json.load(f)
        esc_repo = EscalationRepository(db_path=db_path)
        for e in escs:
            try:
                esc_repo.insert(e)
            except Exception:
                pass
    except FileNotFoundError:
        pass
