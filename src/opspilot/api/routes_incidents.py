from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..services.incident_service import IncidentService

router = APIRouter()

class IncidentIn(BaseModel):
    incident_id: str
    title: str
    description: str
    severity: str
    service: str


@router.get('/incidents')
def list_incidents():
    svc = IncidentService()
    return svc.list()


@router.post('/incidents')
def create_incident(payload: IncidentIn):
    svc = IncidentService()
    try:
        inc = svc.create(payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return inc


@router.get('/incidents/{incident_id}')
def get_incident(incident_id: str):
    svc = IncidentService()
    inc = svc.get(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail='not found')
    return inc


class TransitionIn(BaseModel):
    status: str


@router.post('/incidents/{incident_id}/transition')
def transition(incident_id: str, payload: TransitionIn):
    svc = IncidentService()
    try:
        svc.transition(incident_id, payload.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'ok': True}
