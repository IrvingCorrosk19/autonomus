"""
FLUJO 11: IA Closer (Cierre de Ventas)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.ai_closer import AICloser
from app.api.deps import get_database
from app.core.logging import get_logger
from typing import Dict, Any

router = APIRouter()
logger = get_logger(__name__)


@router.post("/close")
async def close_sale(
    message: str,
    customer_context: Dict[str, Any],
    product_interest: Dict[str, Any],
    db: AsyncSession = Depends(get_database)
):
    """
    Genera respuesta optimizada para cierre de venta usando IA Closer.
    """
    try:
        closer = AICloser()
        response = await closer.respond_to_sales_opportunity(
            message=message,
            customer_context=customer_context,
            product_interest=product_interest
        )
        return {"response": response, "status": "success"}
    except Exception as e:
        logger.error("ai_closer_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

