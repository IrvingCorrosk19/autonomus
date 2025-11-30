"""
FLUJO 13: Recordatorios de Pago
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.payment_reminder import PaymentReminderService
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/remind")
async def send_payment_reminders(
    db: AsyncSession = Depends(get_database)
):
    """
    Envía recordatorios de pago pendientes.
    Este endpoint puede ser llamado por un job scheduler.
    """
    try:
        service = PaymentReminderService()
        await service.send_reminders(db)
        return {"status": "completed", "message": "Payment reminders sent"}
    except Exception as e:
        logger.error("payment_reminder_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

