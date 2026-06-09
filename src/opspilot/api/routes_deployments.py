from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.deployment_service import DeploymentService

router = APIRouter()

class DeploymentIn(BaseModel):
    deployment_id: str
    service: str
    version: str
    environment: str


@router.get('/deployments')
def list_deployments():
    svc = DeploymentService()
    return svc.list()


@router.post('/deployments')
def create_deployment(payload: DeploymentIn):
    svc = DeploymentService()
    return svc.create(payload.dict())
