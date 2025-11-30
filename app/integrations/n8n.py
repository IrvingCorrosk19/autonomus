"""
Integración con n8n
"""
import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class N8NClient:
    """Cliente para interactuar con n8n"""
    
    def __init__(self):
        self.base_url = settings.N8N_WEBHOOK_URL
    
    async def trigger_webhook(
        self,
        workflow_name: str,
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Dispara un webhook de n8n.
        
        Args:
            workflow_name: Nombre del workflow
            data: Datos a enviar
        
        Returns:
            Respuesta del webhook o None si falla
        """
        try:
            url = f"{self.base_url}/{workflow_name}"
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=data)
                response.raise_for_status()
                
                logger.info(
                    "n8n_webhook_triggered",
                    workflow=workflow_name,
                    status_code=response.status_code
                )
                
                return response.json()
        except Exception as e:
            logger.error(
                "n8n_webhook_error",
                workflow=workflow_name,
                error=str(e)
            )
            return None
    
    async def notify_message_received(self, message_id: str):
        """Notifica a n8n que se recibió un mensaje"""
        return await self.trigger_webhook(
            "crm/message-received",
            {"message_id": message_id}
        )

