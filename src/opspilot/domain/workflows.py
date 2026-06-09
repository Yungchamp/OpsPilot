from pydantic import BaseModel
from typing import Any

class Job(BaseModel):
    job_id: str
    job_type: str
    payload: dict
    status: str = 'queued'
    attempts: int = 0
    next_run_at: str | None = None
    last_error: str | None = None
