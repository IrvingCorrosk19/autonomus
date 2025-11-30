"""
FLUJO 22: Alertas Inteligentes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.alerts import IntelligentAlerts
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/check")
async def check_alerts(
    db: AsyncSession = Depends(get_database)
):
    """
    Verifica condiciones de alerta y genera notificaciones.
    Este endpoint puede ser llamado por un job scheduler.
    """
    try:
        alerts_service = IntelligentAlerts()
        await alerts_service.check_all_alerts(db)
        return {"status": "completed", "message": "Alerts checked"}
    except Exception as e:
        logger.error("alerts_check_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

