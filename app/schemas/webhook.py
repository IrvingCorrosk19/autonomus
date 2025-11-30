"""
Schemas para webhooks
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class InboundWebhook(BaseModel):
    """Payload genérico de webhook entrante"""
    object: Optional[str] = None
    entry: Optional[List[Dict[str, Any]]] = None
    
    def get_channel(self) -> str:
        """Extrae el canal del payload"""
        if self.object == "whatsapp_business_account":
            return "whatsapp"
        elif self.object == "instagram":
            return "instagram"
        elif self.object == "page":
            return "messenger"
        return "unknown"
    
    def extract_message(self) -> Dict[str, Any]:
        """Extrae datos normalizados del mensaje"""
        # Implementación básica - se puede mejorar según estructura real
        if not self.entry:
            return {}
        
        # Simplificado - en producción necesitarías parsear según cada plataforma
        return {
            "sender": "unknown",
            "content": "",
            "metadata": self.dict()
        }


class WebhookResponse(BaseModel):
    """Respuesta del webhook"""
    status: str = Field(..., description="Estado del procesamiento")
    message_id: Optional[str] = Field(None, description="ID del mensaje creado")
    processing_id: Optional[str] = Field(None, description="ID de procesamiento")

