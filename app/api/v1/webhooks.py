"""
FLUJO 1: Webhook de Entrada General
"""
from fastapi import APIRouter, BackgroundTasks, HTTPException, Query, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from app.schemas.webhook import InboundWebhook, WebhookResponse
from app.models.message import RawMessage, MessageChannel
from app.services.message_processor import MessageProcessor
from app.api.deps import get_database
from app.core.config import settings
from app.core.logging import get_logger
from app.db.session import AsyncSessionLocal
from datetime import datetime
import uuid

router = APIRouter()
logger = get_logger(__name__)


async def process_message_background(message_id: str, channel: str):
    """Wrapper para procesar mensaje en background con nueva sesión"""
    try:
        async with AsyncSessionLocal() as db:
            await MessageProcessor.process(message_id, channel, db)
    except Exception as e:
        logger.error("background_processing_error", message_id=message_id, error=str(e))


@router.post("/inbound", response_model=WebhookResponse)
async def receive_inbound_message(
    payload: Dict[str, Any],
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_database)
):
    """
    Recibe mensajes de WhatsApp, Instagram o Messenger.
    
    - Valida el payload
    - Almacena mensaje raw
    - Dispara procesamiento asíncrono
    - Retorna 200 OK inmediatamente (requisito de Meta)
    """
    try:
        # 1. Validar origen del canal
        webhook = InboundWebhook(**payload)
        channel = webhook.get_channel()
        
        if channel == "unknown":
            logger.warning("unknown_webhook_source", payload=payload)
            # Retornar 200 de todas formas para Meta
            return WebhookResponse(status="received", message_id=None)
        
        # 2. Extraer datos normalizados
        message_data = webhook.extract_message()
        
        # 3. Guardar mensaje raw en DB
        raw_message = RawMessage(
            channel=MessageChannel[channel.upper()],
            sender_id=message_data.get("sender", "unknown"),
            content=message_data.get("content", ""),
            metadata=payload,
            received_at=datetime.utcnow()
        )
        db.add(raw_message)
        await db.commit()
        await db.refresh(raw_message)
        
        # 4. Disparar procesamiento en background
        # Nota: No podemos pasar db directamente, se creará nueva sesión en el procesador
        background_tasks.add_task(
            process_message_background,
            message_id=raw_message.id,
            channel=channel
        )
        
        # 5. Notificar a n8n (webhook interno)
        from app.integrations.n8n import N8NClient
        n8n_client = N8NClient()
        background_tasks.add_task(
            n8n_client.notify_message_received,
            message_id=raw_message.id
        )
        
        logger.info(
            "message_received",
            message_id=raw_message.id,
            channel=channel,
            sender=message_data.get("sender")
        )
        
        return WebhookResponse(
            status="received",
            message_id=raw_message.id,
            processing_id=str(uuid.uuid4())
        )
        
    except Exception as e:
        logger.error("webhook_processing_error", error=str(e))
        # IMPORTANTE: Retornar 200 de todas formas para Meta
        return WebhookResponse(status="error", message_id=None)


@router.get("/inbound/verify")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """
    Verificación de webhook requerida por Meta.
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.WEBHOOK_VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)
    raise HTTPException(status_code=403, detail="Invalid verify token")

