"""
FLUJO 5: Enrutamiento Inteligente
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.router import RoutingDecision
from app.schemas.lead import LeadScore
from app.schemas.intent import IntentDetectionResult
from app.schemas.sentiment import SentimentResult
from app.services.router import IntelligentRouter
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/route", response_model=RoutingDecision)
async def route_message(
    intent: IntentDetectionResult,
    sentiment: SentimentResult,
    lead_score: LeadScore,
    db: AsyncSession = Depends(get_database)
):
    """
    Decide el destino óptimo del mensaje según intención, sentimiento y score.
    
    Matriz de decisión:
    - Hot lead + purchase intent → sales_team
    - Negative sentiment + high churn risk → retention_specialist
    - Complaint/warranty → support_team
    - Simple inquiry → chatbot
    - Spam → auto_reject
    """
    try:
        router_service = IntelligentRouter()
        decision = await router_service.route_message(
            intent=intent,
            sentiment=sentiment,
            lead_score=lead_score,
            db=db
        )
        return decision
    except Exception as e:
        logger.error("routing_endpoint_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

