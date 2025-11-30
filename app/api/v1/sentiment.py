"""
FLUJO 4: Sentiment Analysis
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sentiment import SentimentAnalysisRequest, SentimentResult
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/analyze", response_model=SentimentResult)
async def analyze_sentiment(
    request: SentimentAnalysisRequest,
    db: AsyncSession = Depends(get_database)
):
    """
    Analiza el sentimiento emocional del mensaje.
    
    Retorna:
    - Sentimiento (positive/neutral/negative)
    - Score numérico (-1.0 a +1.0)
    - Emociones específicas detectadas
    - Nivel de urgencia
    - Riesgo de churn (si aplica)
    """
    try:
        analyzer = SentimentAnalyzer()
        result = await analyzer.analyze(request, db)
        return result
    except Exception as e:
        logger.error("sentiment_analysis_endpoint_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

