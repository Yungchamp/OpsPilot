import uuid
from fastapi.testclient import TestClient
from opspilot.app import app

client = TestClient(app)

def test_health():
    r = client.get('/health')
    assert r.status_code == 200

def test_create_incident():
    incident_id = f"API-{uuid.uuid4()}"
    payload = {'incident_id': incident_id, 'title': 't', 'description': 'd', 'severity': 'low', 'service': 's'}
    r = client.post('/incidents', json=payload)
    assert r.status_code == 200
    r2 = client.get(f'/incidents/{incident_id}')
    assert r2.status_code == 200
