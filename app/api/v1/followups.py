"""
FLUJO 8: Seguimiento Inteligente
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.follow_up import FollowUpService
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/check")
async def check_followups(
    db: AsyncSession = Depends(get_database)
):
    """
    Verifica y envía follow-ups pendientes.
    Este endpoint puede ser llamado por un job scheduler.
    """
    try:
        service = FollowUpService()
        await service.check_and_send_followups(db)
        return {"status": "completed", "message": "Follow-ups checked and sent"}
    except Exception as e:
        logger.error("followup_check_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

