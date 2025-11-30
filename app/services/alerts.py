"""
FLUJO 22: Alertas Inteligentes
"""
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.alert import Alert
from app.models.customer import Customer
from app.models.lead import Lead
from app.models.conversation import Conversation
from app.core.logging import get_logger
import enum

logger = get_logger(__name__)


class AlertType(enum.Enum):
    SALES_DROP = "sales_drop"
    ANGRY_CUSTOMER = "angry_customer"
    CHURN_RISK = "churn_risk"
    HOT_LEAD = "hot_lead"
    INVENTORY_LOW = "inventory_low"
    COMPETITOR_MENTION = "competitor_mention"
    PAYMENT_OVERDUE = "payment_overdue"


class IntelligentAlerts:
    """
    Sistema de alertas que detecta:
    - Ventas inusualmente bajas
    - Clientes molestos/riesgo de churn
    - Leads extremadamente calientes
    - Stock bajo
    - Menciones de competencia
    - Pagos vencidos
    """
    
    async def check_all_alerts(self, db: AsyncSession):
        """
        Job que corre cada hora para verificar condiciones de alerta.
        """
        # Alertas de ventas
        await self._check_sales_anomalies(db)
        
        # Alertas de clientes
        await self._check_customer_risks(db)
        
        # Alertas de leads
        await self._check_hot_leads(db)
        
        # Alertas operacionales
        await self._check_overdue_payments(db)
    
    async def _check_sales_anomalies(self, db: AsyncSession):
        """Detecta drops anormales en ventas"""
        # TODO: Implementar cálculo real de ventas
        # Por ahora, solo log
        logger.info("sales_anomaly_check_completed")
    
    async def _check_customer_risks(self, db: AsyncSession):
        """Identifica clientes en riesgo de churn"""
        # Clientes con sentimiento muy negativo reciente
        cutoff_date = datetime.utcnow() - timedelta(days=7)
        
        stmt = select(Customer).join(Conversation).where(
            Conversation.avg_sentiment_score < -0.7,
            Conversation.last_message_at > cutoff_date
        )
        
        result = await db.execute(stmt)
        at_risk = result.scalars().all()
        
        for customer in at_risk:
            await self._send_alert(
                alert_type=AlertType.CHURN_RISK,
                severity="critical",
                message=f"🚨 Cliente {customer.name} en alto riesgo de churn",
                data={
                    "customer_id": customer.id,
                    "sentiment_score": None,  # TODO: Obtener de conversación
                },
                recipients=["customer_success@company.com"],
                db=db
            )
    
    async def _check_hot_leads(self, db: AsyncSession):
        """Notifica sobre leads muy calientes"""
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        
        stmt = select(Lead).where(
            Lead.score > 90,
            Lead.created_at > cutoff_time
        )
        
        result = await db.execute(stmt)
        hot_leads = result.scalars().all()
        
        if hot_leads:
            await self._send_alert(
                alert_type=AlertType.HOT_LEAD,
                severity="high",
                message=f"🔥 {len(hot_leads)} leads calientes sin asignar",
                data={
                    "leads": [{"id": l.id, "score": l.score, "name": l.name} for l in hot_leads]
                },
                recipients=["sales_team@company.com"],
                db=db
            )
    
    async def _check_overdue_payments(self, db: AsyncSession):
        """Verifica pagos vencidos"""
        # TODO: Implementar verificación de facturas vencidas
        logger.info("overdue_payments_check_completed")
    
    async def _send_alert(
        self,
        alert_type: AlertType,
        severity: str,
        message: str,
        data: Dict,
        recipients: List[str],
        db: AsyncSession
    ):
        """
        Envía alerta por múltiples canales.
        """
        alert = Alert(
            type=alert_type.value,
            severity=severity,
            message=message,
            data=data,
            created_at=datetime.utcnow()
        )
        
        db.add(alert)
        await db.commit()
        
        # TODO: Enviar email
        # TODO: Enviar Slack/Teams
        # TODO: SMS para alertas críticas
        
        logger.warning(
            "alert_triggered",
            type=alert_type.value,
            severity=severity,
            recipients=recipients
        )

