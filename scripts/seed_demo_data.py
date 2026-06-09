import sqlite3
import json
import os

ROOT = os.path.dirname(os.path.dirname(__file__))
DB = os.environ.get('OPSPILOT_DB', os.path.join(ROOT, 'data', 'opspilot.db'))

with open(os.path.join(ROOT, 'data', 'samples', 'incidents.json')) as f:
    incidents = json.load(f)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS incidents (
    incident_id TEXT PRIMARY KEY,
    title TEXT,
    description TEXT,
    severity TEXT,
    service TEXT,
    status TEXT,
    created_at TEXT,
    updated_at TEXT,
    assigned_team TEXT,
    tags TEXT,
    source TEXT,
    risk_score REAL
)
''')

for inc in incidents:
    cur.execute('INSERT OR IGNORE INTO incidents (incident_id,title,description,severity,service,status,created_at,updated_at,assigned_team,tags,source,risk_score) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', (
        inc.get('incident_id'), inc.get('title'), inc.get('description'), inc.get('severity'), inc.get('service'), inc.get('status'), inc.get('created_at'), inc.get('updated_at'), inc.get('assigned_team'), json.dumps(inc.get('tags') or []), inc.get('source'), inc.get('risk_score', 0.0)
    ))

conn.commit()
conn.close()
print('seeded:', len(incidents))
