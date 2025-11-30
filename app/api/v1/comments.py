"""
FLUJO 17: Respuesta Automática a Comentarios
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.comment_responder import CommentResponder
from app.api.deps import get_database
from app.core.logging import get_logger
from typing import Dict, Any

router = APIRouter()
logger = get_logger(__name__)


@router.post("/respond")
async def respond_to_comment(
    comment: Dict[str, Any],
    post: Dict[str, Any],
    db: AsyncSession = Depends(get_database)
):
    """
    Procesa y responde automáticamente a un comentario en redes sociales.
    """
    try:
        responder = CommentResponder()
        await responder.process_comment(comment, post, db)
        return {"status": "processed", "comment_id": comment.get("id")}
    except Exception as e:
        logger.error("comment_response_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

