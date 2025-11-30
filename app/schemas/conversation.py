"""
Schemas para Conversaciones
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class ChatMessage(BaseModel):
    """Mensaje de chat"""
    content: str = Field(..., description="Contenido del mensaje")
    action: Optional[str] = Field(None, description="Acción a realizar (escalate_to_human, etc)")
    suggested_replies: Optional[List[str]] = Field(None, description="Respuestas rápidas")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata adicional")


class ChatContext(BaseModel):
    """Contexto de conversación"""
    customer_id: Optional[str] = None
    conversation_id: Optional[str] = None
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)

