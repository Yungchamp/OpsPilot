# API

- GET /health
- GET /incidents
- POST /incidents
- GET /incidents/{incident_id}
- POST /incidents/{incident_id}/transition
- POST /logs/ingest
- GET /analytics/summary
- GET /deployments
- POST /deployments
- POST /workflows/run

All endpoints return JSON and use Pydantic validation.
