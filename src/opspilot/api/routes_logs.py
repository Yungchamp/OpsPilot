from fastapi import APIRouter
from pydantic import BaseModel
from ..services.log_ingestion_service import LogIngestionService

router = APIRouter()

class LogIngestIn(BaseModel):
    lines: list[str]


@router.post('/logs/ingest')
def ingest(payload: LogIngestIn):
    svc = LogIngestionService()
    results = svc.ingest_lines(payload.lines)
    return {'ingested': len(results), 'results': results}
