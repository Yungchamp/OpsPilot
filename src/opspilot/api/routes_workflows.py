from fastapi import APIRouter
from ..services.workflow_service import WorkflowService
from pydantic import BaseModel

router = APIRouter()

class RunIn(BaseModel):
    job_type: str
    payload: dict


@router.post('/workflows/run')
def run_workflow(payload: RunIn):
    svc = WorkflowService()
    job = svc.enqueue(payload.job_type, payload.payload)
    return job
