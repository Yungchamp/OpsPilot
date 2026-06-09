from fastapi import APIRouter
from ..services.analytics_service import AnalyticsService

router = APIRouter()

@router.get('/analytics/summary')
def summary():
    svc = AnalyticsService()
    return svc.summary()
