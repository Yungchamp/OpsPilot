import json
from ..domain.log_events import LogEvent
from ..storage.repositories import LogRepository
from datetime import datetime

class LogIngestionService:
    def __init__(self, db_path: str | None = None):
        self.repo = LogRepository(db_path=db_path)

    def ingest_lines(self, lines: list[str]):
        results = []
        for i, line in enumerate(lines):
            try:
                obj = json.loads(line)
                if 'timestamp' not in obj:
                    raise ValueError('missing timestamp')
                if 'level' not in obj or 'service' not in obj:
                    raise ValueError('missing required fields')
                event = LogEvent(**obj)
                self.repo.insert(event.model_dump())
                results.append({'line': i, 'ok': True})
            except Exception as e:
                results.append({'line': i, 'ok': False, 'error': str(e)})
        return results

    def ingest_file(self, path: str):
        with open(path) as f:
            lines = [l.strip() for l in f if l.strip()]
        return self.ingest_lines(lines)
