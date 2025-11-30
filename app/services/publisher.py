"""
FLUJO 15: Publicación Automática en Redes
"""
from typing import List, Dict, Optional
from datetime import datetime
from app.core.config import settings
from app.core.logging import get_logger
import httpx

logger = get_logger(__name__)


class SocialMediaPublisher:
    """
    Publica contenido en múltiples plataformas automáticamente.
    """
    
    def __init__(self):
        self.meta_token = settings.META_ACCESS_TOKEN
    
    async def publish_post(
        self,
        content: Dict,
        platforms: List[str],
        schedule_time: Optional[datetime] = None
    ) -> Dict:
        """
        Publica o programa contenido en plataformas especificadas.
        """
        results = {}
        
        for platform in platforms:
            try:
                if schedule_time and schedule_time > datetime.utcnow():
                    # Programar para después
                    result = await self._schedule_post(
                        platform=platform,
                        content=content,
                        schedule_time=schedule_time
                    )
                else:
                    # Publicar inmediatamente
                    result = await self._publish_now(platform, content)
                
                results[platform] = result
                
            except Exception as e:
                logger.error(
                    "publication_failed",
                    platform=platform,
                    error=str(e)
                )
                results[platform] = {"status": "error", "error": str(e)}
        
        return results
    
    async def _publish_now(self, platform: str, content: Dict) -> Dict:
        """Publicación inmediata"""
        if platform == "instagram":
            return await self._publish_instagram_post(content)
        elif platform == "facebook":
            return await self._publish_facebook_post(content)
        else:
            raise ValueError(f"Platform {platform} not supported")
    
    async def _publish_instagram_post(self, content: Dict) -> Dict:
        """Publica en Instagram usando Meta Graph API"""
        if not self.meta_token or not settings.INSTAGRAM_BUSINESS_ACCOUNT_ID:
            raise ValueError("Meta credentials not configured")
        
        # Paso 1: Crear container
        container_url = f"https://graph.facebook.com/v18.0/{settings.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
        
        async with httpx.AsyncClient() as client:
            container_response = await client.post(
                container_url,
                data={
                    "image_url": content.get("asset_url"),
                    "caption": f"{content.get('copy', '')}\n\n{' '.join(content.get('hashtags', []))}",
                    "access_token": self.meta_token
                }
            )
            container_response.raise_for_status()
            container_id = container_response.json()["id"]
            
            # Paso 2: Publicar
            publish_url = f"https://graph.facebook.com/v18.0/{settings.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
            publish_response = await client.post(
                publish_url,
                data={
                    "creation_id": container_id,
                    "access_token": self.meta_token
                }
            )
            publish_response.raise_for_status()
            
            return publish_response.json()
    
    async def _publish_facebook_post(self, content: Dict) -> Dict:
        """Publica en Facebook"""
        if not self.meta_token or not settings.FACEBOOK_PAGE_ID:
            raise ValueError("Meta credentials not configured")
        
        url = f"https://graph.facebook.com/v18.0/{settings.FACEBOOK_PAGE_ID}/photos"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                data={
                    "url": content.get("asset_url"),
                    "message": f"{content.get('copy', '')}\n\n{' '.join(content.get('hashtags', []))}",
                    "access_token": self.meta_token
                }
            )
            response.raise_for_status()
            return response.json()
    
    async def _schedule_post(
        self,
        platform: str,
        content: Dict,
        schedule_time: datetime
    ) -> Dict:
        """Programa post para publicación futura"""
        # TODO: Implementar scheduling usando Meta API
        logger.info("post_scheduled", platform=platform, schedule_time=schedule_time)
        return {"status": "scheduled", "scheduled_for": schedule_time.isoformat()}

