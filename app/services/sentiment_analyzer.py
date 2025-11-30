"""
Analizador de Sentimiento - FLUJO 4
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.schemas.sentiment import SentimentAnalysisRequest, SentimentResult
from app.models.sentiment import SentimentAnalysis
from app.core.logging import get_logger

logger = get_logger(__name__)


class SentimentAnalyzer:
    """Analiza el sentimiento de los mensajes"""
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
        if not self.ai:
            raise ValueError("No hay adaptador de IA disponible")
    
    async def analyze(
        self,
        request: SentimentAnalysisRequest,
        db: AsyncSession
    ) -> SentimentResult:
        """
        Analiza el sentimiento con granularidad emocional.
        
        Categorías:
        - positive: Cliente satisfecho, agradecido
        - neutral: Consulta objetiva, sin carga emocional
        - negative: Molesto, frustrado, enojado
        
        Score: -1.0 (muy negativo) a +1.0 (muy positivo)
        """
        prompt = self._build_sentiment_prompt(request.message)
        
        try:
            result = await self.ai.analyze_sentiment(prompt)
            
            # Guardar en DB
            await self._save_sentiment(request, result, db)
            
            # Si es muy negativo, disparar alerta
            if result.score < -0.7:
                await self._trigger_escalation_alert(result, db)
            
            return result
        except Exception as e:
            logger.error("sentiment_analysis_failed", error=str(e))
            # Fallback
            return SentimentResult(
                sentiment="neutral",
                score=0.0,
                confidence=0.5,
                urgency_level="low",
                error=str(e)
            )
    
    def _build_sentiment_prompt(self, message: str) -> str:
        """Construye el prompt para análisis de sentimiento"""
        return f"""
        Analiza el sentimiento del siguiente mensaje de cliente:
        
        "{message}"
        
        DIMENSIONES A EVALUAR:
        1. Sentimiento general (positive/neutral/negative)
        2. Score numérico (-1.0 a +1.0)
        3. Emociones específicas (anger, joy, frustration, satisfaction, etc)
        4. Nivel de urgencia (low/medium/high/critical)
        5. Riesgo de churn (0-100%)
        
        CONTEXTO: Esto es para priorizar respuestas y asignar al agente adecuado.
        
        RESPONDE EN JSON:
        {{
          "sentiment": "negative",
          "score": -0.8,
          "confidence": 0.95,
          "emotions": {{
            "anger": 0.7,
            "frustration": 0.9
          }},
          "urgency_level": "critical",
          "churn_risk": 85,
          "recommended_priority": "escalate_immediately"
        }}
        """
    
    async def _save_sentiment(
        self,
        request: SentimentAnalysisRequest,
        result: SentimentResult,
        db: AsyncSession
    ):
        """Guarda el análisis de sentimiento en la base de datos"""
        sentiment = SentimentAnalysis(
            message_id=request.message_id,
            conversation_id=request.conversation_id,
            sentiment=result.sentiment,
            score=result.score,
            confidence=result.confidence,
            emotions=result.emotions,
            urgency_level=result.urgency_level,
            churn_risk=result.churn_risk,
            ai_model=result.ai_model_used
        )
        db.add(sentiment)
        await db.commit()
    
    async def _trigger_escalation_alert(
        self,
        result: SentimentResult,
        db: AsyncSession
    ):
        """Dispara alerta de escalamiento para sentimientos muy negativos"""
        logger.warning(
            "negative_sentiment_alert",
            sentiment_score=result.score,
            urgency=result.urgency_level,
            churn_risk=result.churn_risk
        )
        # TODO: Implementar sistema de alertas

