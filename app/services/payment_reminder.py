"""
FLUJO 13: Recordatorios de Pago
"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.invoice import Invoice
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger

logger = get_logger(__name__)


class PaymentReminderService:
    """
    Secuencia de recordatorios de pago:
    
    - 7 días antes: Recordatorio amistoso
    - 3 días antes: Recordatorio con detalles
    - Día de vencimiento: Urgencia educada
    - 1 día después: Cortés pero firme
    - 7 días después: Escalamiento
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
    
    async def send_reminders(self, db: AsyncSession):
        """Job diario para enviar recordatorios"""
        
        # Facturas próximas a vencer (7 días)
        upcoming_date = datetime.utcnow() + timedelta(days=7)
        stmt = select(Invoice).where(
            Invoice.status == "pending",
            Invoice.due_date <= upcoming_date,
            Invoice.due_date > datetime.utcnow()
        )
        result = await db.execute(stmt)
        upcoming = result.scalars().all()
        
        for invoice in upcoming:
            if invoice.reminder_count == 0:
                await self._send_friendly_reminder(invoice, db)
        
        # Facturas vencidas (1 día)
        overdue_1d = datetime.utcnow() - timedelta(days=1)
        stmt = select(Invoice).where(
            Invoice.status == "pending",
            Invoice.due_date < datetime.utcnow(),
            Invoice.due_date >= overdue_1d
        )
        result = await db.execute(stmt)
        overdue_recent = result.scalars().all()
        
        for invoice in overdue_recent:
            await self._send_polite_overdue_reminder(invoice, db)
        
        # Facturas muy vencidas (7+ días)
        overdue_7d = datetime.utcnow() - timedelta(days=7)
        stmt = select(Invoice).where(
            Invoice.status == "pending",
            Invoice.due_date < overdue_7d
        )
        result = await db.execute(stmt)
        overdue_old = result.scalars().all()
        
        for invoice in overdue_old:
            await self._escalate_overdue_invoice(invoice, db)
    
    async def _send_friendly_reminder(self, invoice: Invoice, db: AsyncSession):
        """Recordatorio 7 días antes de vencimiento"""
        if not self.ai:
            return
        
        message = await self.ai.generate_response(
            f"""
            Genera recordatorio de pago amigable.
            
            Factura #{invoice.number}
            Monto: ${invoice.amount}
            Vence: {invoice.due_date.strftime('%Y-%m-%d')}
            
            TONO: Servicial, no cobranza
            OBJETIVO: Recordar para evitar retrasos
            
            DEBE INCLUIR:
            - Resumen de factura
            - Métodos de pago disponibles
            - Link de pago directo
            - Agradecimiento por ser cliente
            """
        )
        
        # TODO: Enviar mensaje real
        invoice.reminder_count += 1
        await db.commit()
        
        logger.info("payment_reminder_friendly_sent", invoice_id=invoice.id)
    
    async def _send_polite_overdue_reminder(self, invoice: Invoice, db: AsyncSession):
        """Recordatorio cortés para facturas vencidas recientemente"""
        if not self.ai:
            return
        
        message = await self.ai.generate_response(
            f"""
            Genera recordatorio para factura vencida hace 1 día.
            
            Factura #{invoice.number}
            Monto: ${invoice.amount}
            
            TONO: Cortés pero firme
            ASUNCIÓN: Puede ser olvido genuino
            
            DEBE INCLUIR:
            - Mención de que venció ayer
            - Monto + recargo por mora (si aplica)
            - Urgencia de regularizar
            - Facilidades de pago si existen
            """
        )
        
        # TODO: Enviar mensaje y notificar equipo de finanzas
        invoice.reminder_count += 1
        await db.commit()
        
        logger.info("payment_reminder_overdue_sent", invoice_id=invoice.id)
    
    async def _escalate_overdue_invoice(self, invoice: Invoice, db: AsyncSession):
        """Escala facturas muy vencidas"""
        # TODO: Implementar escalamiento a equipo de cobranza
        logger.warning("invoice_escalated", invoice_id=invoice.id, days_overdue=7)

