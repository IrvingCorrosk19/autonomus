"""
FLUJO 7: Escalamiento Automático
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.escalation import EscalationService
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/escalate")
async def escalate_conversation(
    conversation_id: str,
    reason: str,
    db: AsyncSession = Depends(get_database)
):
    """
    Escala una conversación a agente humano.
    """
    try:
        from app.models.conversation import Conversation
        conversation = await db.get(Conversation, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        from app.services.escalation import EscalationReason
        escalation_reason = EscalationReason(reason)
        
        service = EscalationService()
        await service.escalate(conversation, escalation_reason, db)
        
        return {"status": "escalated", "conversation_id": conversation_id}
    except Exception as e:
        logger.error("escalation_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

