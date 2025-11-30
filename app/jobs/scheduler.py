"""
Scheduler para jobs periódicos
"""
import asyncio
from datetime import datetime
from app.db.session import AsyncSessionLocal
from app.services.follow_up import FollowUpService
from app.services.cart_recovery import CartRecoveryService
from app.services.payment_reminder import PaymentReminderService
from app.services.deduplicator import Deduplicator
from app.services.alerts import IntelligentAlerts
from app.core.logging import get_logger

logger = get_logger(__name__)


class JobScheduler:
    """Ejecuta jobs periódicos"""
    
    def __init__(self):
        self.running = False
    
    async def start(self):
        """Inicia el scheduler"""
        self.running = True
        logger.info("job_scheduler_started")
        
        # Ejecutar jobs en paralelo
        await asyncio.gather(
            self._run_hourly_jobs(),
            self._run_daily_jobs()
        )
    
    async def _run_hourly_jobs(self):
        """Jobs que corren cada hora"""
        while self.running:
            try:
                async with AsyncSessionLocal() as db:
                    # Follow-ups
                    followup_service = FollowUpService()
                    await followup_service.check_and_send_followups(db)
                    
                    # Cart recovery
                    cart_service = CartRecoveryService()
                    await cart_service.detect_abandoned_carts(db)
                    
                    # Alertas
                    alerts_service = IntelligentAlerts()
                    await alerts_service.check_all_alerts(db)
                
                logger.info("hourly_jobs_completed")
            except Exception as e:
                logger.error("hourly_jobs_error", error=str(e))
            
            # Esperar 1 hora
            await asyncio.sleep(3600)
    
    async def _run_daily_jobs(self):
        """Jobs que corren diariamente"""
        while self.running:
            try:
                async with AsyncSessionLocal() as db:
                    # Payment reminders
                    payment_service = PaymentReminderService()
                    await payment_service.send_reminders(db)
                    
                    # Deduplicación
                    deduplicator = Deduplicator()
                    await deduplicator.find_duplicates(db)
                
                logger.info("daily_jobs_completed")
            except Exception as e:
                logger.error("daily_jobs_error", error=str(e))
            
            # Esperar 24 horas
            await asyncio.sleep(86400)
    
    def stop(self):
        """Detiene el scheduler"""
        self.running = False
        logger.info("job_scheduler_stopped")

