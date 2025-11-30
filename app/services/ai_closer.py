"""
FLUJO 11: IA Closer (Cierre de Ventas)
"""
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.core.logging import get_logger

logger = get_logger(__name__)


class AICloser:
    """
    Agente de IA entrenado específicamente para:
    1. Detectar señales de compra
    2. Manejar objeciones comunes
    3. Crear urgencia apropiada
    4. Facilitar el cierre
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
    
    async def respond_to_sales_opportunity(
        self,
        message: str,
        customer_context: Dict,
        product_interest: Dict
    ) -> str:
        """
        Genera respuesta optimizada para cierre de venta.
        """
        # Detectar objeciones en el mensaje
        objections = await self._detect_objections(message)
        
        # Detectar señales de compra
        buying_signals = await self._detect_buying_signals(message)
        
        if objections:
            # Manejar objeciones con IA
            response = await self._handle_objections(
                objections=objections,
                product=product_interest,
                customer=customer_context
            )
        elif buying_signals:
            # Cliente listo para comprar → facilitar
            response = await self._facilitate_purchase(
                product=product_interest,
                customer=customer_context
            )
        else:
            # Empujar suavemente hacia decisión
            response = await self._nudge_towards_decision(
                product=product_interest,
                customer=customer_context
            )
        
        return response
    
    async def _detect_objections(self, message: str) -> List[str]:
        """Detecta objeciones en el mensaje"""
        objections = []
        
        objection_patterns = {
            "price": ["muy caro", "precio", "costoso", "barato"],
            "timing": ["no es el momento", "después", "más tarde", "no ahora"],
            "authority": ["tengo que consultarlo", "mi jefe", "necesito aprobación"],
            "need": ["no estoy seguro", "no lo necesito", "no sé si"],
            "trust": ["no los conozco", "confianza", "garantía"]
        }
        
        message_lower = message.lower()
        for objection_type, patterns in objection_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                objections.append(objection_type)
        
        return objections
    
    async def _handle_objections(
        self,
        objections: List[str],
        product: Dict,
        customer: Dict
    ) -> str:
        """Maneja objeciones comunes con técnicas de ventas"""
        if not self.ai:
            return "Entiendo tu preocupación. ¿Podemos hablar más sobre esto?"
        
        objection_type = objections[0]
        
        prompt = f"""
        Cliente tiene objeción de tipo: {objection_type}
        
        Mensaje exacto del cliente: "{objections}"
        
        Contexto:
        - Producto: {product.get('name', 'N/A')} - ${product.get('price', 'N/A')}
        - Cliente: {customer.get('name', 'N/A')}
        
        INSTRUCCIONES:
        1. Empatiza con la objeción
        2. Usa estrategia apropiada para {objection_type}
        3. Incluye datos/pruebas concretas
        4. Termina con pregunta que facilite avanzar
        5. NUNCA ser insistente o agresivo
        
        TONO: Consultivo, no vendedor
        LONGITUD: 3-4 oraciones máximo
        """
        
        return await self.ai.generate_response(prompt)
    
    async def _detect_buying_signals(self, message: str) -> List[str]:
        """Detecta señales de alta intención de compra"""
        signals = []
        
        buying_signal_patterns = {
            "purchase_process": ["cómo compro", "proceso de compra", "cómo pago"],
            "pricing_details": ["cotización", "factura", "cuánto cuesta exactamente"],
            "delivery": ["cuándo me llega", "tiempo de entrega", "envío"],
            "comparison": ["diferencia entre", "cuál es mejor", "recomiendas"],
            "guarantees": ["garantía", "devolución", "qué pasa si"]
        }
        
        message_lower = message.lower()
        for signal_type, patterns in buying_signal_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                signals.append(signal_type)
        
        return signals
    
    async def _facilitate_purchase(
        self,
        product: Dict,
        customer: Dict
    ) -> str:
        """Cuando el cliente está listo, facilitar el proceso"""
        if not self.ai:
            return f"Excelente! ¿Quieres proceder con {product.get('name', 'el producto')}?"
        
        prompt = f"""
        Cliente muestra señales claras de querer comprar {product.get('name', 'producto')}.
        
        OBJETIVO: Hacer el proceso de compra lo más fácil posible
        
        MENSAJE DEBE INCLUIR:
        1. Resumen rápido de lo que va a recibir
        2. Precio final claro: ${product.get('price', 'N/A')}
        3. Opciones de pago simples
        4. Timeline de entrega
        5. Tranquilidad (garantías, soporte)
        
        FORMATO: Bullet points para claridad
        TONO: Confiado pero servicial
        """
        
        return await self.ai.generate_response(prompt)
    
    async def _nudge_towards_decision(
        self,
        product: Dict,
        customer: Dict
    ) -> str:
        """Empuja suavemente hacia decisión"""
        if not self.ai:
            return "¿Hay algo más en lo que pueda ayudarte?"
        
        prompt = f"""
        Genera mensaje que empuje suavemente hacia decisión sin ser agresivo.
        
        Producto: {product.get('name', 'N/A')}
        Cliente: {customer.get('name', 'N/A')}
        
        TONO: Amigable, servicial
        """
        
        return await self.ai.generate_response(prompt)

