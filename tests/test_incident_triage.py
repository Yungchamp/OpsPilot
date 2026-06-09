import tempfile
from opspilot.storage.migrations import run_migrations
from opspilot.services.incident_service import IncidentService
from opspilot.domain.ai_triage import MockAIProvider


def test_ai_triage_mock():
    prov = MockAIProvider()
    out = prov.triage('Service returns 500 error with exception')
    assert 'summary' in out
    assert out['confidence'] > 0


def test_incident_create_and_transition(tmp_path):
    db = tmp_path / 'test.db'
    run_migrations(str(db))
    svc = IncidentService(db_path=str(db))
    inc = {'incident_id':'INC-100','title':'t','description':'error 500','severity':'HIGH','service':'svc'}
    svc.create(inc)
    got = svc.get('INC-100')
    assert got['incident_id']=='INC-100'
    try:
        svc.transition('INC-100', 'resolved')
        assert False, 'should not allow direct new->resolved'
    except Exception:
        pass
    svc.transition('INC-100', 'triaging')
    svc.transition('INC-100', 'investigating')
