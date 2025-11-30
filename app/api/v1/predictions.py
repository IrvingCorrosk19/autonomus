"""
FLUJO 21: Predicción de Cierre de Venta
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.sales_predictor import SalesPredictor
from app.api.deps import get_database
from app.core.logging import get_logger
from typing import Dict, Any

router = APIRouter()
logger = get_logger(__name__)


@router.post("/close-probability")
async def predict_close_probability(
    opportunity: Dict[str, Any],
    db: AsyncSession = Depends(get_database)
):
    """
    Predice la probabilidad de cierre de una oportunidad de venta.
    """
    try:
        predictor = SalesPredictor()
        prediction = await predictor.predict_close_probability(opportunity, db)
        return {"status": "predicted", "prediction": prediction}
    except Exception as e:
        logger.error("sales_prediction_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

