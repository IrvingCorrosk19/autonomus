"""
Procesador de mensajes - FLUJO 1
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import RawMessage, MessageChannel
from app.core.logging import get_logger

logger = get_logger(__name__)


class MessageProcessor:
    """Procesa mensajes entrantes"""
    
    @staticmethod
    async def process(
        message_id: str,
        channel: str,
        db: AsyncSession
    ) -> None:
        """
        Procesa un mensaje raw.
        
        Este método se ejecuta en background después de recibir el webhook.
        """
        try:
            # Obtener mensaje raw
            raw_message = await db.get(RawMessage, message_id)
            if not raw_message:
                logger.error("raw_message_not_found", message_id=message_id)
                return
            
            # Marcar como procesado
            raw_message.processed = True
            await db.commit()
            
            logger.info(
                "message_processed",
                message_id=message_id,
                channel=channel
            )
            
            # Aquí se dispararían los siguientes pasos:
            # 1. Clasificación de lead
            # 2. Detección de intención
            # 3. Análisis de sentimiento
            # 4. Enrutamiento
            
        except Exception as e:
            logger.error(
                "message_processing_error",
                message_id=message_id,
                error=str(e)
            )
            # Marcar error en el mensaje
            try:
                raw_message = await db.get(RawMessage, message_id)
                if raw_message:
                    raw_message.processing_error = str(e)
                    await db.commit()
            except:
                pass  # Si falla, al menos logueamos el error

