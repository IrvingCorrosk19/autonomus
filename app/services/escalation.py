"""
FLUJO 7: Escalamiento Automático
"""
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.conversation import Conversation
from app.models.case import Case, CaseStatus
from app.core.logging import get_logger
from datetime import datetime
import enum

logger = get_logger(__name__)


class EscalationReason(enum.Enum):
    HIGH_SENTIMENT_NEGATIVE = "sentiment_score_below_threshold"
    COMPLEX_QUERY = "bot_cannot_handle"
    CUSTOMER_REQUEST = "customer_explicitly_asked"
    MULTIPLE_FAILED_ATTEMPTS = "bot_failed_to_resolve"
    HIGH_VALUE_TRANSACTION = "transaction_above_threshold"
    LEGAL_ISSUE = "legal_or_compliance_matter"
    VIP_CUSTOMER = "vip_customer_tier"


class EscalationService:
    """Servicio de escalamiento automático"""
    
    async def should_escalate(
        self,
        conversation: Conversation,
        latest_message: str,
        db: AsyncSession
    ) -> Tuple[bool, Optional[EscalationReason]]:
        """
        Evalúa si se debe escalar la conversación.
        
        Criterios:
        1. Sentimiento muy negativo (< -0.7)
        2. Cliente pide explícitamente hablar con humano
        3. Bot ha fallado 3+ veces seguidas
        4. Transacción > $5,000
        5. Temas legales/compliance
        6. Cliente VIP
        """
        # Criterio 1: Sentimiento negativo persistente
        if (conversation.avg_sentiment_score and 
            conversation.avg_sentiment_score < -0.7 and 
            conversation.message_count > 3):
            return True, EscalationReason.HIGH_SENTIMENT_NEGATIVE
        
        # Criterio 2: Solicitud explícita
        if self._customer_requests_human(latest_message):
            return True, EscalationReason.CUSTOMER_REQUEST
        
        # Criterio 3: Fallos repetidos del bot
        # TODO: Implementar tracking de fallos del bot
        # if conversation.bot_failure_count >= 3:
        #     return True, EscalationReason.MULTIPLE_FAILED_ATTEMPTS
        
        # Criterio 4: Transacción alta
        # TODO: Verificar valor de transacción
        # if conversation.potential_transaction_value > 5000:
        #     return True, EscalationReason.HIGH_VALUE_TRANSACTION
        
        # Criterio 5: Temas sensibles
        if self._contains_legal_keywords(latest_message):
            return True, EscalationReason.LEGAL_ISSUE
        
        return False, None
    
    async def escalate(
        self,
        conversation: Conversation,
        reason: EscalationReason,
        db: AsyncSession
    ):
        """
        Ejecuta el escalamiento:
        1. Notifica al equipo humano
        2. Asigna agente disponible
        3. Transfiere contexto completo
        4. Informa al cliente
        """
        # Encontrar mejor agente
        agent = await self._find_best_agent(
            department=self._get_department(conversation),
            priority=self._calculate_priority(reason),
            db=db
        )
        
        # Crear caso/ticket
        case = Case(
            conversation_id=conversation.id,
            customer_id=conversation.customer_id,
            description=f"Escalamiento automático: {reason.value}",
            status=CaseStatus.OPEN,
            priority=self._calculate_priority(reason)
        )
        db.add(case)
        
        # Marcar conversación como escalada
        conversation.escalated = True
        conversation.escalation_reason = reason.value
        
        await db.commit()
        
        # Notificar agente (TODO: Implementar)
        # await self._notify_agent(agent, case)
        
        # Informar al cliente (TODO: Implementar)
        # await self._send_escalation_message(conversation.customer, agent.name)
        
        logger.info(
            "conversation_escalated",
            conversation_id=conversation.id,
            reason=reason.value,
            assigned_to=agent.id if agent else None
        )
    
    def _customer_requests_human(self, message: str) -> bool:
        """Detecta si el cliente pide explícitamente hablar con humano"""
        keywords = [
            "hablar con humano", "agente humano", "supervisor",
            "manager", "representante", "persona real"
        ]
        return any(keyword in message.lower() for keyword in keywords)
    
    def _contains_legal_keywords(self, message: str) -> bool:
        """Detecta temas legales o de compliance"""
        keywords = [
            "demanda", "abogado", "legal", "demandar",
            "regulación", "compliance", "violación"
        ]
        return any(keyword in message.lower() for keyword in keywords)
    
    async def _find_best_agent(
        self,
        department: str,
        priority: int,
        db: AsyncSession
    ) -> Optional[Dict]:
        """Encuentra el mejor agente disponible"""
        # TODO: Implementar lógica de asignación de agentes
        return None
    
    def _get_department(self, conversation: Conversation) -> str:
        """Determina el departamento apropiado"""
        # TODO: Implementar lógica basada en intención
        return "support"
    
    def _calculate_priority(self, reason: EscalationReason) -> int:
        """Calcula prioridad basada en razón"""
        priority_map = {
            EscalationReason.HIGH_SENTIMENT_NEGATIVE: 5,
            EscalationReason.CUSTOMER_REQUEST: 4,
            EscalationReason.MULTIPLE_FAILED_ATTEMPTS: 4,
            EscalationReason.HIGH_VALUE_TRANSACTION: 5,
            EscalationReason.LEGAL_ISSUE: 5,
            EscalationReason.VIP_CUSTOMER: 5,
            EscalationReason.COMPLEX_QUERY: 3,
        }
        return priority_map.get(reason, 3)

