"""
Schemas para Detección de Intención
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class IntentDetectionRequest(BaseModel):
    """Request para detectar intención"""
    message: str = Field(..., description="Mensaje a analizar")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexto adicional")
    lead_id: Optional[str] = None


class IntentDetectionResult(BaseModel):
    """Resultado de detección de intención"""
    primary_intent: str = Field(..., description="Intención principal")
    secondary_intents: Optional[List[str]] = Field(None, description="Intenciones secundarias")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confianza 0-1")
    entities: Optional[Dict[str, Any]] = Field(None, description="Entidades extraídas")
    reasoning: Optional[str] = Field(None, description="Razonamiento")
    ai_model_used: Optional[str] = None
    error: Optional[str] = None

