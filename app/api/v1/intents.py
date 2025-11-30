"""
FLUJO 3: Detección de Intención
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.intent import IntentDetectionRequest, IntentDetectionResult
from app.services.intent_detector import IntentDetector
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/detect", response_model=IntentDetectionResult)
async def detect_intent(
    request: IntentDetectionRequest,
    db: AsyncSession = Depends(get_database)
):
    """
    Detecta la intención específica del mensaje del usuario.
    
    Identifica:
    - Intención primaria (purchase_inquiry, complaint, etc.)
    - Intenciones secundarias
    - Nivel de confianza
    - Entidades extraídas (productos, cantidades, fechas)
    """
    try:
        detector = IntentDetector()
        result = await detector.detect(request, db)
        return result
    except Exception as e:
        logger.error("intent_detection_endpoint_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

