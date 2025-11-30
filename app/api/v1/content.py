"""
FLUJOS 14-16: Generación, Publicación y Programación de Contenido
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.content_generator import ContentGenerator
from app.services.publisher import SocialMediaPublisher
from app.services.scheduler import IntelligentScheduler
from app.api.deps import get_database
from app.core.logging import get_logger
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter()
logger = get_logger(__name__)


@router.post("/generate")
async def generate_content(
    product: Dict[str, Any],
    platform: str,
    purpose: str,
    db: AsyncSession = Depends(get_database)
):
    """
    FLUJO 14: Genera contenido automático para redes sociales.
    """
    try:
        generator = ContentGenerator()
        content = await generator.generate_product_post(product, platform, purpose)
        return {"status": "generated", "content": content}
    except Exception as e:
        logger.error("content_generation_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/publish")
async def publish_content(
    content: Dict[str, Any],
    platforms: List[str],
    schedule_time: str = None,
    db: AsyncSession = Depends(get_database)
):
    """
    FLUJO 15: Publica contenido en redes sociales.
    """
    try:
        publisher = SocialMediaPublisher()
        schedule_dt = datetime.fromisoformat(schedule_time) if schedule_time else None
        result = await publisher.publish_post(content, platforms, schedule_dt)
        return {"status": "published", "results": result}
    except Exception as e:
        logger.error("content_publish_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/schedule")
async def schedule_content(
    platform: str,
    content_type: str,
    target_audience: str,
    db: AsyncSession = Depends(get_database)
):
    """
    FLUJO 16: Predice mejor momento para publicar.
    """
    try:
        scheduler = IntelligentScheduler()
        best_time = await scheduler.predict_best_time(platform, content_type, target_audience)
        return {"status": "scheduled", "best_time": best_time.isoformat()}
    except Exception as e:
        logger.error("content_schedule_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

