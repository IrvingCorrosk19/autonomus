"""
Schemas para Análisis de Sentimiento
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class SentimentAnalysisRequest(BaseModel):
    """Request para analizar sentimiento"""
    message: str = Field(..., description="Mensaje a analizar")
    conversation_id: Optional[str] = None
    message_id: Optional[str] = None


class SentimentResult(BaseModel):
    """Resultado de análisis de sentimiento"""
    sentiment: str = Field(..., description="positive, neutral, negative")
    score: float = Field(..., ge=-1.0, le=1.0, description="Score -1 a +1")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confianza 0-1")
    emotions: Optional[Dict[str, float]] = Field(None, description="Emociones detectadas")
    urgency_level: Optional[str] = Field(None, description="Nivel de urgencia")
    recommended_priority: Optional[str] = Field(None, description="Prioridad recomendada")
    churn_risk: Optional[float] = Field(None, ge=0.0, le=100.0, description="Riesgo de churn 0-100")
    ai_model_used: Optional[str] = None
    error: Optional[str] = None

