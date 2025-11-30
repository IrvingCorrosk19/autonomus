"""
FLUJO 6: Agente Conversacional Autónomo
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.conversation import ChatMessage, ChatContext
from app.services.chatbot import AutonomousChatbot
from app.api.deps import get_database
from app.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/respond", response_model=ChatMessage)
async def chat_respond(
    message: str,
    context: ChatContext,
    db: AsyncSession = Depends(get_database)
):
    """
    Genera respuesta del chatbot autónomo.
    """
    try:
        chatbot = AutonomousChatbot()
        response = await chatbot.respond(message, context, db)
        return response
    except Exception as e:
        logger.error("chatbot_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

