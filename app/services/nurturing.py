"""
FLUJO 10: Nutrición Inteligente de Leads
"""
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lead import Lead
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger

logger = get_logger(__name__)


class NurturingEngine:
    """
    Motor de nutrición con IA que adapta contenido según:
    - Comportamiento del lead (opens, clicks, respuestas)
    - Score dinámico (sube/baja según engagement)
    - Fase del buyer journey (awareness, consideration, decision)
    - Intereses detectados
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
        self.campaigns = {
            "cold_to_warm": ColdToWarmCampaign(ai_adapter),
            "product_education": ProductEducationCampaign(ai_adapter),
        }
    
    async def process_lead(self, lead: Lead, db: AsyncSession):
        """
        Evalúa al lead y decide qué campaña/contenido enviar.
        """
        # Determinar fase del buyer journey
        journey_stage = await self._identify_journey_stage(lead)
        
        # Seleccionar campaña apropiada
        campaign = self._select_campaign(lead, journey_stage)
        
        # IA genera contenido personalizado
        content = await campaign.generate_next_content(lead)
        
        if content:
            # Enviar en el timing óptimo
            optimal_time = await self._predict_best_send_time(lead)
            await self._schedule_send(lead, content, send_at=optimal_time)
            
            logger.info(
                "nurturing_content_scheduled",
                lead_id=lead.id,
                campaign=campaign.name,
                journey_stage=journey_stage
            )
    
    async def _identify_journey_stage(self, lead: Lead) -> str:
        """Identifica la fase del buyer journey"""
        if lead.score > 70:
            return "decision"
        elif lead.score > 40:
            return "consideration"
        return "awareness"
    
    def _select_campaign(self, lead: Lead, journey_stage: str):
        """Selecciona campaña apropiada"""
        if journey_stage == "awareness":
            return self.campaigns["cold_to_warm"]
        return self.campaigns["product_education"]
    
    async def _predict_best_send_time(self, lead: Lead) -> datetime:
        """Predice mejor momento para enviar"""
        # TODO: Implementar ML para predecir mejor tiempo
        return datetime.utcnow() + timedelta(hours=2)
    
    async def _schedule_send(self, lead: Lead, content: str, send_at: datetime):
        """Programa envío de contenido"""
        # TODO: Implementar sistema de scheduling
        logger.info("content_scheduled", lead_id=lead.id, send_at=send_at)


class ColdToWarmCampaign:
    """Secuencia de 7 días para leads fríos"""
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter
        self.name = "cold_to_warm"
    
    async def generate_next_content(self, lead: Lead) -> Optional[str]:
        """Genera contenido según día de campaña"""
        if not self.ai:
            return None
        
        # TODO: Calcular día basado en fecha de entrada a campaña
        day = 0
        
        if day == 0:
            return await self._generate_educational_content(lead)
        elif day == 2:
            return await self._generate_case_study(lead)
        elif day == 4:
            return await self._generate_comparison(lead)
        elif day == 6:
            return await self._generate_offer(lead)
        
        return None
    
    async def _generate_educational_content(self, lead: Lead) -> str:
        """IA genera artículo/video educativo personalizado"""
        if not self.ai:
            return ""
        
        prompt = f"""
        Genera un mensaje de nurturing educativo para:
        
        Lead: {lead.name}
        Industria: {lead.company or "particular"}
        
        OBJETIVO: Educar sin vender
        FORMATO: Mensaje corto + link a recurso
        TONO: Experto pero accesible
        """
        
        return await self.ai.generate_response(prompt)
    
    async def _generate_case_study(self, lead: Lead) -> str:
        """Genera caso de éxito"""
        if not self.ai:
            return ""
        return await self.ai.generate_response(f"Genera caso de éxito relevante para {lead.name}")
    
    async def _generate_comparison(self, lead: Lead) -> str:
        """Genera comparativa"""
        if not self.ai:
            return ""
        return await self.ai.generate_response(f"Genera comparativa de soluciones para {lead.name}")
    
    async def _generate_offer(self, lead: Lead) -> str:
        """Genera oferta especial"""
        if not self.ai:
            return ""
        return await self.ai.generate_response(f"Genera oferta especial para {lead.name}")


class ProductEducationCampaign:
    """Campaña de educación de producto"""
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter
        self.name = "product_education"
    
    async def generate_next_content(self, lead: Lead) -> Optional[str]:
        """Genera contenido educativo"""
        if not self.ai:
            return None
        return await self.ai.generate_response(f"Genera contenido educativo sobre productos para {lead.name}")

