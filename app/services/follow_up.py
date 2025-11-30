"""
FLUJO 8: Seguimiento Inteligente
"""
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.lead import Lead
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger

logger = get_logger(__name__)


class FollowUpService:
    """
    Secuencias de seguimiento automatizadas:
    
    Día 1: Mensaje inicial
    Día 2: Si no responde → Follow-up 1 (valor agregado)
    Día 4: Si no responde → Follow-up 2 (urgencia suave)
    Día 7: Si no responde → Follow-up 3 (última oportunidad)
    Día 14: Si no responde → Mover a nurturing pasivo
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
    
    async def check_and_send_followups(self, db: AsyncSession):
        """
        Job programado que corre cada hora.
        Busca leads sin actividad y envía follow-up correspondiente.
        """
        # Leads sin respuesta en 24h (Follow-up 1)
        leads_24h = await self._get_silent_leads(hours=24, followup_count=0, db=db)
        for lead in leads_24h:
            await self._send_followup_1(lead, db)
        
        # Leads sin respuesta en 4 días (Follow-up 2)
        leads_4d = await self._get_silent_leads(hours=96, followup_count=1, db=db)
        for lead in leads_4d:
            await self._send_followup_2(lead, db)
        
        # Leads sin respuesta en 7 días (Follow-up 3)
        leads_7d = await self._get_silent_leads(hours=168, followup_count=2, db=db)
        for lead in leads_7d:
            await self._send_followup_3(lead, db)
    
    async def _get_silent_leads(
        self,
        hours: int,
        followup_count: int,
        db: AsyncSession
    ) -> List[Lead]:
        """Obtiene leads sin actividad en X horas"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        # TODO: Implementar query real con tracking de follow-ups
        return []
    
    async def _send_followup_1(self, lead: Lead, db: AsyncSession):
        """Follow-up 1: Valor agregado"""
        if not self.ai:
            return
        
        message = await self.ai.generate_response(
            f"""
            Genera un mensaje de follow-up amigable que:
            1. Haga referencia a la consulta original del lead: {lead.name}
            2. Aporte información adicional útil (ej: guía, comparativa, caso de éxito)
            3. No sea insistente
            4. Termine con pregunta abierta
            
            Tono: Servicial, no vendedor
            """
        )
        
        # TODO: Enviar mensaje real
        logger.info("followup_1_sent", lead_id=lead.id)
    
    async def _send_followup_2(self, lead: Lead, db: AsyncSession):
        """Follow-up 2: Urgencia suave"""
        if not self.ai:
            return
        
        message = await self.ai.generate_response(
            f"""
            Genera mensaje con:
            1. Recordatorio amable de su interés
            2. Incentivo temporal (descuento, stock limitado, etc)
            3. Facilita tomar acción (link directo, respuesta simple)
            
            Tono: Urgente pero respetuoso
            """
        )
        
        # TODO: Enviar mensaje real
        logger.info("followup_2_sent", lead_id=lead.id)
    
    async def _send_followup_3(self, lead: Lead, db: AsyncSession):
        """Follow-up 3: Última oportunidad"""
        if not self.ai:
            return
        
        message = await self.ai.generate_response(
            f"""
            Genera mensaje final:
            1. Reconoce que no ha habido respuesta
            2. Ofrece última oportunidad (oferta especial si aplica)
            3. Da opción de darse de baja educadamente
            4. Deja puerta abierta para futuro
            
            Tono: Profesional, no desesperado
            """
        )
        
        # TODO: Enviar mensaje y mover a nurturing pasivo
        logger.info("followup_3_sent", lead_id=lead.id)

