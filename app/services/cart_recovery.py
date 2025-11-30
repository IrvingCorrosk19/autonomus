"""
FLUJO 12: Recuperación de Carrito Abandonado
"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.cart import Cart
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger

logger = get_logger(__name__)


class CartRecoveryService:
    """
    Sistema de recuperación de carritos con secuencia inteligente:
    
    1 hora: Recordatorio suave
    24 horas: Incentivo (descuento 5-10%)
    48 horas: Urgencia (stock limitado)
    72 horas: Última oportunidad (descuento mayor)
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
    
    async def detect_abandoned_carts(self, db: AsyncSession):
        """
        Job que corre cada hora para detectar carritos abandonados.
        """
        # Carritos con productos pero sin compra en X tiempo
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        
        stmt = select(Cart).where(
            Cart.status == "pending",
            Cart.last_activity < cutoff_time,
            Cart.recovery_attempt_count < 3
        )
        
        result = await db.execute(stmt)
        abandoned = result.scalars().all()
        
        for cart in abandoned:
            await self._trigger_recovery_sequence(cart, db)
    
    async def _trigger_recovery_sequence(self, cart: Cart, db: AsyncSession):
        """Inicia secuencia de recuperación personalizada"""
        hours_abandoned = (datetime.utcnow() - cart.last_activity).total_seconds() / 3600
        
        if hours_abandoned >= 72:
            await self._send_final_offer(cart, db)
        elif hours_abandoned >= 48:
            await self._send_urgency_message(cart, db)
        elif hours_abandoned >= 24:
            await self._send_incentive_message(cart, db)
        elif hours_abandoned >= 1:
            await self._send_gentle_reminder(cart, db)
    
    async def _send_gentle_reminder(self, cart: Cart, db: AsyncSession):
        """Recordatorio 1 hora después"""
        if not self.ai:
            return
        
        products_text = self._format_cart_items(cart)
        
        message = await self.ai.generate_response(
            f"""
            Genera recordatorio suave de carrito abandonado.
            
            Cliente: {cart.customer_id}
            Productos: {products_text}
            Valor total: ${cart.total_amount}
            
            TONO: Amigable, útil (no vendedor)
            OBJETIVO: Recordar sin presionar
            """
        )
        
        # TODO: Enviar mensaje real
        cart.recovery_attempt_count += 1
        await db.commit()
        
        logger.info("cart_recovery_gentle_sent", cart_id=cart.id)
    
    async def _send_incentive_message(self, cart: Cart, db: AsyncSession):
        """Incentivo después de 24h"""
        discount_code = await self._generate_discount_code(cart, percentage=10)
        
        if self.ai:
            message = await self.ai.generate_response(
                f"""
                Genera mensaje con incentivo para recuperar carrito.
                
                INCLUIR:
                - Recordatorio amigable
                - Código de descuento 10%: {discount_code}
                - Urgencia suave (válido 24h)
                
                TONO: Generoso, creando valor
                """
            )
        
        cart.recovery_attempt_count += 1
        await db.commit()
        
        logger.info("cart_recovery_incentive_sent", cart_id=cart.id)
    
    async def _send_urgency_message(self, cart: Cart, db: AsyncSession):
        """Urgencia después de 48h"""
        if self.ai:
            message = await self.ai.generate_response(
                f"""
                Genera mensaje con urgencia sobre stock limitado.
                Valor del carrito: ${cart.total_amount}
                
                TONO: Urgente pero respetuoso
                """
            )
        
        cart.recovery_attempt_count += 1
        await db.commit()
        
        logger.info("cart_recovery_urgency_sent", cart_id=cart.id)
    
    async def _send_final_offer(self, cart: Cart, db: AsyncSession):
        """Última oportunidad con mejor oferta"""
        discount_code = await self._generate_discount_code(cart, percentage=15)
        
        if self.ai:
            message = await self.ai.generate_response(
                f"""
                Mensaje de última oportunidad.
                
                INCLUIR:
                - Reconocimiento de que no completó compra
                - Mejor oferta (15% descuento): {discount_code}
                - Urgencia real (expira en 24h)
                
                TONO: Último intento pero respetuoso
                """
            )
        
        cart.recovery_attempt_count += 1
        cart.final_attempt = True
        await db.commit()
        
        logger.info("cart_recovery_final_sent", cart_id=cart.id)
    
    def _format_cart_items(self, cart: Cart) -> str:
        """Formatea items del carrito"""
        if not cart.items:
            return "productos"
        return ", ".join([item.get("name", "producto") for item in cart.items])
    
    async def _generate_discount_code(self, cart: Cart, percentage: int) -> str:
        """Genera código de descuento"""
        # TODO: Implementar generación real de códigos
        return f"RECOVER{percentage}"

