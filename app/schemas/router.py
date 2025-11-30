"""
Schemas para Enrutamiento
"""
from pydantic import BaseModel, Field
from typing import Optional


class RoutingDecision(BaseModel):
    """Decisión de enrutamiento"""
    destination: str = Field(..., description="Destino: sales_team, support_bot, human_agent, etc")
    priority: int = Field(..., ge=1, le=5, description="Prioridad 1-5")
    reasoning: str = Field(..., description="Razonamiento de la decisión")
    assigned_to: Optional[str] = Field(None, description="ID del agente asignado si aplica")

