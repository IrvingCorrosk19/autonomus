"""
FLUJO 21: Predicción de Cierre de Venta
"""
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)


class SalesPredictor:
    """
    Modelo ML que predice probabilidad de cierre de una oportunidad.
    
    Features usadas:
    - Lead score
    - Engagement (emails abiertos, respuestas, etc)
    - Tiempo en pipeline
    - Valor de oportunidad
    - Sentimiento promedio
    - Cantidad de interacciones
    """
    
    def __init__(self):
        # TODO: Cargar modelo ML entrenado
        self.model = None
    
    async def predict_close_probability(
        self,
        opportunity: Dict,
        db: AsyncSession
    ) -> Dict:
        """
        Predice probabilidad de cierre (0-100%).
        """
        # Extraer features
        features = await self._extract_features(opportunity)
        
        # Por ahora, cálculo simple (TODO: Usar modelo ML real)
        probability = self._simple_prediction(features)
        
        # Interpretar
        if probability > 80:
            likelihood = "very_high"
            recommendation = "Priorizar, listo para cerrar"
        elif probability > 60:
            likelihood = "high"
            recommendation = "Empujar hacia cierre esta semana"
        elif probability > 40:
            likelihood = "medium"
            recommendation = "Continuar nurturing, no forzar cierre"
        else:
            likelihood = "low"
            recommendation = "Re-calificar o mover a nurturing de largo plazo"
        
        return {
            "probability": round(probability, 2),
            "likelihood": likelihood,
            "recommendation": recommendation,
            "key_factors": self._identify_key_factors(features)
        }
    
    async def _extract_features(self, opportunity: Dict) -> Dict:
        """Extrae features numéricas para el modelo"""
        return {
            "lead_score": opportunity.get("lead_score", 50) / 100,
            "engagement": opportunity.get("engagement_score", 0.5),
            "days_in_pipeline": opportunity.get("days_in_pipeline", 0),
            "deal_value": opportunity.get("estimated_value", 0),
            "sentiment": opportunity.get("avg_sentiment", 0),
            "interaction_count": opportunity.get("interaction_count", 0),
        }
    
    def _simple_prediction(self, features: Dict) -> float:
        """Predicción simple basada en reglas (temporal)"""
        score = features.get("lead_score", 0.5) * 40  # 0-40 puntos
        engagement = features.get("engagement", 0.5) * 30  # 0-30 puntos
        sentiment = (features.get("sentiment", 0) + 1) / 2 * 20  # 0-20 puntos
        interactions = min(features.get("interaction_count", 0) / 10, 1) * 10  # 0-10 puntos
        
        return score + engagement + sentiment + interactions
    
    def _identify_key_factors(self, features: Dict) -> List[str]:
        """Identifica los factores más importantes"""
        factors = []
        
        if features.get("lead_score", 0) > 0.8:
            factors.append("high_lead_score")
        if features.get("engagement", 0) > 0.7:
            factors.append("high_engagement")
        if features.get("sentiment", 0) > 0.5:
            factors.append("positive_sentiment")
        
        return factors[:3]  # Top 3

