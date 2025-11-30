"""
FLUJO 2: Clasificación Automática de Lead
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.lead import LeadClassificationRequest, LeadScore
from app.services.lead_classifier import LeadClassifier
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/classify", response_model=LeadScore)
async def classify_lead(
    request: LeadClassificationRequest,
    db: AsyncSession = Depends(get_database)
):
    """
    Clasifica un lead usando IA.
    
    Evalúa la calidad/prioridad de un lead basándose en:
    - Mensaje inicial
    - Metadata del remitente
    - Historial previo (si existe)
    
    Retorna un score de 0-100 y categoría (hot/warm/cold).
    """
    try:
        classifier = LeadClassifier()
        result = await classifier.classify(request, db)
        return result
    except Exception as e:
        logger.error("lead_classification_endpoint_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

