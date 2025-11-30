"""
FLUJO 9: Cierre Automático de Caso
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.case import Case, CaseStatus
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)


class CaseClosureService:
    """
    Evalúa si un caso puede cerrarse basándose en:
    1. Confirmación explícita del cliente ("todo bien", "resuelto", etc)
    2. Silencio del cliente después de resolución (72h)
    3. Métricas de satisfacción positivas
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
    
    async def evaluate_closure(
        self,
        case: Case,
        latest_message: str,
        db: AsyncSession
    ) -> dict:
        """
        Determina si el caso debe cerrarse.
        
        Returns:
            Dict con should_close, confidence, reason, requires_survey
        """
        # Detección de confirmación explícita
        confirmation_patterns = [
            "todo bien",
            "resuelto",
            "gracias, perfecto",
            "ya está solucionado",
            "no necesito nada más"
        ]
        
        if any(pattern in latest_message.lower() for pattern in confirmation_patterns):
            return {
                "should_close": True,
                "confidence": 0.95,
                "reason": "Confirmación explícita del cliente",
                "requires_survey": True,
                "closure_type": "customer_confirmed"
            }
        
        # Usar IA para detección más sofisticada
        if self.ai:
            ai_decision = await self._ai_evaluate_closure(case, latest_message)
            if ai_decision.get("should_close") and ai_decision.get("confidence", 0) > 0.8:
                # Enviar mensaje de confirmación antes de cerrar
                await self._send_closure_confirmation(case, db)
                return ai_decision
        
        return {
            "should_close": False,
            "reason": "Requiere más interacción"
        }
    
    async def _ai_evaluate_closure(self, case: Case, latest_message: str) -> dict:
        """IA evalúa si el caso puede cerrarse"""
        if not self.ai:
            return {"should_close": False}
        
        prompt = f"""
        Evalúa si este caso de soporte puede cerrarse:
        
        CASO: {case.description}
        ÚLTIMO MENSAJE: "{latest_message}"
        
        ¿El cliente indica que el problema está resuelto?
        Responde en JSON: {{"should_close": true/false, "confidence": 0.0-1.0, "reason": "..."}}
        """
        
        response = await self.ai.generate_response(prompt)
        # TODO: Parsear respuesta JSON
        return {"should_close": False, "confidence": 0.5}
    
    async def _send_closure_confirmation(self, case: Case, db: AsyncSession):
        """Envía mensaje pidiendo confirmación de cierre"""
        if not self.ai:
            return
        
        message = await self.ai.generate_response(
            f"""
            Genera un mensaje breve preguntando si el problema está resuelto.
            Debe ser amigable y dar opción de reabrir si hay algo más.
            
            Caso: {case.description}
            """
        )
        
        # TODO: Enviar mensaje real
        logger.info("closure_confirmation_sent", case_id=case.id)
    
    async def close_case(
        self,
        case: Case,
        reason: str,
        collect_feedback: bool = True,
        db: AsyncSession = None
    ):
        """
        Cierra el caso y opcionalmente recopila feedback.
        """
        case.status = CaseStatus.CLOSED
        case.closed_at = datetime.utcnow()
        case.closure_reason = reason
        
        if case.opened_at:
            delta = case.closed_at - case.opened_at
            case.resolution_time_hours = delta.total_seconds() / 3600
        
        if db:
            await db.commit()
        
        # Enviar encuesta de satisfacción
        if collect_feedback:
            await self._send_satisfaction_survey(case)
        
        logger.info(
            "case_closed",
            case_id=case.id,
            resolution_time_hours=case.resolution_time_hours
        )
    
    async def _send_satisfaction_survey(self, case: Case):
        """Envía encuesta de satisfacción"""
        # TODO: Implementar envío de encuesta
        logger.info("satisfaction_survey_sent", case_id=case.id)

