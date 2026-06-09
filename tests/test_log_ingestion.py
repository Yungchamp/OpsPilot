from opspilot.storage.migrations import run_migrations
from opspilot.services.log_ingestion_service import LogIngestionService


def test_log_ingest_malformed(tmp_path):
    db = tmp_path / 'l.db'
    run_migrations(str(db))
    svc = LogIngestionService(db_path=str(db))
    lines = ['{"timestamp":"2026-06-01T12:00:00Z","level":"INFO","service":"service-a"}', 'not-json']
    results = svc.ingest_lines(lines)
    assert results[0]['ok'] is True
    assert results[1]['ok'] is False
