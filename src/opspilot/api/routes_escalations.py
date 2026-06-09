from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.escalation_service import EscalationService

router = APIRouter()

class EscalationIn(BaseModel):
    reason: str | None = None


@router.get('/escalations')
def list_escalations():
    svc = EscalationService()
    return svc.list()


@router.post('/incidents/{incident_id}/escalate')
def escalate_incident(incident_id: str, payload: EscalationIn | None = None):
    svc = EscalationService()
    try:
        output = svc.create_for_incident(incident_id, payload.reason if payload else None)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return output


@router.post('/escalations/{escalation_id}/acknowledge')
def acknowledge_escalation(escalation_id: str):
    svc = EscalationService()
    try:
        esc = svc.acknowledge(escalation_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return esc


@router.post('/escalations/{escalation_id}/resolve')
def resolve_escalation(escalation_id: str):
    svc = EscalationService()
    try:
        esc = svc.resolve(escalation_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return esc
