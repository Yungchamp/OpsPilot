from opspilot.storage.migrations import run_migrations
from opspilot.storage.repositories import IncidentRepository


def test_incident_repo(tmp_path):
    db = tmp_path / 'r.db'
    run_migrations(str(db))
    repo = IncidentRepository(db_path=str(db))
    inc = {'incident_id':'I1','title':'t','description':'d','severity':'low','service':'s','status':'new','created_at':'t','updated_at':'t','assigned_team':None,'tags':[],'source':'x','risk_score':0}
    repo.insert(inc)
    got = repo.get('I1')
    assert got['incident_id']=='I1'
