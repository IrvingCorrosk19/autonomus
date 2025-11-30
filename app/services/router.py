"""
Enrutador Inteligente - FLUJO 5
"""
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.lead import LeadScore
from app.schemas.intent import IntentDetectionResult
from app.schemas.sentiment import SentimentResult
from app.schemas.router import RoutingDecision
from app.models.intent import IntentType
from app.core.logging import get_logger

logger = get_logger(__name__)


class IntelligentRouter:
    """Enruta mensajes según intención, sentimiento y score"""
    
    async def route_message(
        self,
        intent: IntentDetectionResult,
        sentiment: SentimentResult,
        lead_score: LeadScore,
        db: AsyncSession
    ) -> RoutingDecision:
        """
        Matriz de decisión:
        
        | Intent          | Sentiment | Score | Destino        | Prioridad |
        |-----------------|-----------|-------|----------------|-----------|
        | purchase        | any       | >80   | sales_team     | 5         |
        | complaint       | negative  | any   | human_agent    | 5         |
        | product_info    | neutral   | <50   | chatbot       | 2         |
        | support_request | negative  | any   | support_team   | 4         |
        | spam            | any       | <20   | auto_reject    | 1         |
        """
        
        # Caso 1: Lead caliente + intención de compra
        if (intent.primary_intent == IntentType.PURCHASE_INQUIRY.value and 
            lead_score.score > 80):
            return RoutingDecision(
                destination="sales_team",
                priority=5,
                reasoning="Hot lead con alta intención de compra",
                assigned_to=await self._get_best_sales_agent(db)
            )
        
        # Caso 2: Cliente molesto (riesgo de churn)
        if sentiment.score < -0.6 and (sentiment.churn_risk or 0) > 70:
            return RoutingDecision(
                destination="retention_specialist",
                priority=5,
                reasoning="Cliente con alto riesgo de churn",
                assigned_to=await self._get_retention_specialist(db)
            )
        
        # Caso 3: Queja/garantía (humano necesario)
        if intent.primary_intent in [IntentType.COMPLAINT.value, IntentType.WARRANTY_CLAIM.value]:
            return RoutingDecision(
                destination="support_team",
                priority=4,
                reasoning="Requiere intervención humana"
            )
        
        # Caso 4: Consulta simple (puede manejar bot)
        if (intent.primary_intent in [IntentType.PRODUCT_INFO.value, IntentType.PRICING_QUESTION.value]
            and sentiment.sentiment != "negative"):
            return RoutingDecision(
                destination="chatbot",
                priority=2,
                reasoning="Consulta simple manejable por IA"
            )
        
        # Caso 5: Spam
        if intent.primary_intent == IntentType.SPAM.value:
            return RoutingDecision(
                destination="auto_reject",
                priority=1,
                reasoning="Mensaje identificado como spam"
            )
        
        # Default: chatbot con opción de escalar
        return RoutingDecision(
            destination="chatbot",
            priority=3,
            reasoning="Ruta estándar con escalamiento disponible"
        )
    
    async def _get_best_sales_agent(self, db: AsyncSession) -> Optional[str]:
        """Obtiene el mejor agente de ventas disponible"""
        # TODO: Implementar lógica de asignación de agentes
        # Por ahora retorna None
        return None
    
    async def _get_retention_specialist(self, db: AsyncSession) -> Optional[str]:
        """Obtiene especialista en retención disponible"""
        # TODO: Implementar lógica de asignación
        return None

