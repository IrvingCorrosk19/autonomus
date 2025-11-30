"""
FLUJO 6: Agente Conversacional Autónomo
"""
from typing import List, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.schemas.conversation import ChatMessage, ChatContext
from app.core.logging import get_logger

logger = get_logger(__name__)


class AutonomousChatbot:
    """Bot de IA que mantiene conversaciones naturales"""
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
        if not self.ai:
            raise ValueError("No hay adaptador de IA disponible")
    
    async def respond(
        self,
        message: str,
        context: ChatContext,
        db: AsyncSession
    ) -> ChatMessage:
        """
        Genera respuesta contextual usando:
        - Catálogo de productos
        - Políticas de la empresa
        - Historial del cliente
        - Inventario en tiempo real
        """
        # 1. Obtener contexto relevante
        product_context = await self._search_products(message, db)
        customer_history = await self._get_customer_history(context.customer_id, db)
        
        # 2. Construir prompt con RAG
        prompt = self._build_chatbot_prompt(
            message=message,
            products=product_context,
            customer_history=customer_history,
            company_policies=self._get_company_policies()
        )
        
        # 3. Generar respuesta
        system_prompt = self._get_system_prompt()
        messages = [
            {"role": "system", "content": system_prompt},
            *context.conversation_history,
            {"role": "user", "content": message}
        ]
        
        response_text = await self.ai.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        # 4. Validar respuesta
        validated_response = await self._validate_response(response_text, product_context)
        
        # 5. Determinar si necesita escalamiento
        needs_escalation = await self._should_escalate(message, validated_response)
        
        if needs_escalation:
            return ChatMessage(
                content="Tu consulta requiere atención personalizada. Te estoy conectando con un agente humano.",
                action="escalate_to_human"
            )
        
        return ChatMessage(
            content=validated_response,
            suggested_replies=await self._generate_quick_replies(validated_response),
            metadata={"products_mentioned": [p.get("id") for p in product_context]}
        )
    
    def _get_system_prompt(self) -> str:
        return """
        Eres un asistente virtual de ventas profesional y amigable.
        
        PERSONALIDAD:
        - Empático y servicial
        - Conciso pero completo
        - Usa emojis moderadamente
        - Tono conversacional pero profesional
        
        CAPACIDADES:
        - Recomendar productos basado en necesidades
        - Proporcionar información de precios y stock
        - Explicar políticas de envío y devolución
        - Procesar órdenes simples
        
        LIMITACIONES:
        - No puedes procesar reembolsos (escala a humano)
        - No puedes modificar órdenes existentes (escala a humano)
        - Si no estás seguro, admite y ofrece conectar con humano
        
        CONOCIMIENTO:
        Tienes acceso al catálogo completo, precios actualizados e inventario en tiempo real.
        
        INSTRUCCIONES:
        1. Lee el mensaje del cliente cuidadosamente
        2. Usa el contexto proporcionado (historial, productos, etc)
        3. Responde de forma natural y útil
        4. Si detectas frustración, sé especialmente empático
        5. Sugiere productos relevantes sin ser invasivo
        6. Finaliza con pregunta o call-to-action suave
        """
    
    async def _search_products(self, message: str, db: AsyncSession) -> List[Dict]:
        """Busca productos relevantes en el mensaje"""
        # TODO: Implementar búsqueda real de productos
        return []
    
    async def _get_customer_history(self, customer_id: Optional[str], db: AsyncSession) -> List[Dict]:
        """Obtiene historial del cliente"""
        if not customer_id:
            return []
        # TODO: Implementar obtención de historial
        return []
    
    def _get_company_policies(self) -> Dict:
        """Retorna políticas de la empresa"""
        return {
            "shipping": "Envíos gratis en compras mayores a $50",
            "returns": "30 días de garantía de devolución",
            "payment": "Aceptamos tarjeta, transferencia y ACH"
        }
    
    def _build_chatbot_prompt(
        self,
        message: str,
        products: List[Dict],
        customer_history: List[Dict],
        company_policies: Dict
    ) -> str:
        """Construye prompt para el chatbot"""
        return f"""
        Mensaje del cliente: "{message}"
        
        Productos relevantes: {products}
        Historial: {customer_history}
        Políticas: {company_policies}
        """
    
    async def _validate_response(self, response: str, product_context: List[Dict]) -> str:
        """Valida que la respuesta no contenga información incorrecta"""
        # Validación básica
        return response
    
    async def _should_escalate(self, message: str, response: str) -> bool:
        """Determina si se debe escalar a humano"""
        escalation_keywords = [
            "reembolso", "devolución", "cancelar orden",
            "hablar con humano", "supervisor", "manager"
        ]
        return any(keyword in message.lower() for keyword in escalation_keywords)
    
    async def _generate_quick_replies(self, response: str) -> List[str]:
        """Genera respuestas rápidas sugeridas"""
        # TODO: Implementar generación de quick replies
        return []

