"""
FLUJO 14: Generación Automática de Contenido
"""
from typing import Dict, Optional
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger

logger = get_logger(__name__)


class ContentGenerator:
    """
    Genera contenido multimodal para redes sociales:
    - Imágenes (DALL-E, Midjourney)
    - Videos cortos (Runway, Pika)
    - Copy (GPT-5)
    - Carruseles
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.text_gen = ai_adapter or AIAdapterFactory.get_default_adapter()
        # TODO: Agregar adaptadores para imagen y video
    
    async def generate_product_post(
        self,
        product: Dict,
        platform: str,
        purpose: str
    ) -> Dict:
        """
        Genera post completo (imagen + copy) para producto.
        """
        # 1. Generar copy
        copy = await self._generate_copy(product, platform, purpose)
        
        # 2. Generar hashtags
        hashtags = await self._generate_hashtags(product, platform)
        
        # 3. TODO: Generar imagen (requiere integración con DALL-E/Midjourney)
        image_url = None
        
        return {
            "asset_url": image_url,
            "copy": copy,
            "hashtags": hashtags,
            "platform": platform,
            "recommended_post_time": None  # TODO: Integrar con scheduler
        }
    
    async def _generate_copy(
        self,
        product: Dict,
        platform: str,
        purpose: str
    ) -> str:
        """IA genera copy optimizado para plataforma"""
        if not self.text_gen:
            return ""
        
        platform_guidelines = {
            "instagram": {
                "optimal_length": 150,
                "tone": "visual, storytelling, emojis ok",
            },
            "facebook": {
                "optimal_length": 250,
                "tone": "conversational, detailed",
            },
            "tiktok": {
                "optimal_length": 100,
                "tone": "casual, trendy, hooks matter",
            }
        }
        
        guidelines = platform_guidelines.get(platform, platform_guidelines["instagram"])
        
        prompt = f"""
        Genera copy para post de {platform} sobre:
        
        PRODUCTO: {product.get('name', 'N/A')}
        PROPÓSITO: {purpose}
        
        GUIDELINES:
        - Longitud óptima: {guidelines['optimal_length']} caracteres
        - Tono: {guidelines['tone']}
        
        ESTRUCTURA:
        1. Hook (primera línea debe captar atención)
        2. Beneficio clave
        3. Descripción breve
        4. Call to action
        
        REGLAS:
        - Emojis: Sí (pero no exagerar)
        - Enfocarse en valor, no features
        """
        
        return await self.text_gen.generate_response(prompt)
    
    async def _generate_hashtags(self, product: Dict, platform: str) -> list:
        """Genera hashtags relevantes"""
        if not self.text_gen:
            return []
        
        prompt = f"""
        Genera 5-10 hashtags relevantes para:
        Producto: {product.get('name', 'N/A')}
        Plataforma: {platform}
        
        Retorna solo los hashtags separados por comas.
        """
        
        response = await self.text_gen.generate_response(prompt)
        hashtags = [tag.strip() for tag in response.split(",")]
        return hashtags[:10]

