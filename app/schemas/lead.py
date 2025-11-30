"""
Schemas para Leads
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class LeadClassificationRequest(BaseModel):
    """Request para clasificar un lead"""
    message: str = Field(..., description="Mensaje del lead")
    sender_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata del remitente"
    )
    lead_id: Optional[str] = Field(None, description="ID del lead si ya existe")


class LeadScore(BaseModel):
    """Resultado de clasificación de lead"""
    lead_id: Optional[str] = None
    score: int = Field(..., ge=0, le=100, description="Score del lead 0-100")
    category: str = Field(..., description="Categoría: hot, warm, cold")
    reasoning: str = Field(..., description="Razonamiento de la clasificación")
    recommended_action: str = Field(..., description="Acción recomendada")
    ai_model_used: Optional[str] = None
    processing_time_ms: Optional[int] = None
    error: Optional[str] = None


class LeadBase(BaseModel):
    """Base schema para Lead"""
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None


class LeadCreate(LeadBase):
    """Schema para crear un lead"""
    pass


class LeadResponse(LeadBase):
    """Schema de respuesta de Lead"""
    id: str
    score: int
    category: Optional[str] = None
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

