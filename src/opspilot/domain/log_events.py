from pydantic import BaseModel
from datetime import datetime

class LogEvent(BaseModel):
    timestamp: str
    level: str
    service: str
    client_id: str | None = None
    message: str | None = None
    trace_id: str | None = None
    status_code: int | None = None
    latency_ms: float | None = None

    def normalize(self):
        # ensure ISO timestamp
        return self
