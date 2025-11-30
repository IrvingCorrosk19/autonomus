"""
FLUJO 12: Recuperación de Carrito Abandonado
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.cart_recovery import CartRecoveryService
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/recover")
async def recover_carts(
    db: AsyncSession = Depends(get_database)
):
    """
    Detecta y procesa carritos abandonados.
    Este endpoint puede ser llamado por un job scheduler.
    """
    try:
        service = CartRecoveryService()
        await service.detect_abandoned_carts(db)
        return {"status": "completed", "message": "Cart recovery process completed"}
    except Exception as e:
        logger.error("cart_recovery_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

