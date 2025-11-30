"""
Detector de Intención - FLUJO 3
"""
from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.schemas.intent import IntentDetectionRequest, IntentDetectionResult
from app.models.intent import LeadIntent, IntentType
from app.core.logging import get_logger

logger = get_logger(__name__)


class IntentDetector:
    """Detecta la intención de los mensajes"""
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
        if not self.ai:
            raise ValueError("No hay adaptador de IA disponible")
    
    async def detect(
        self,
        request: IntentDetectionRequest,
        db: AsyncSession
    ) -> IntentDetectionResult:
        """
        Detecta la intención primaria y secundaria del mensaje.
        
        Returns:
            IntentDetectionResult con:
            - primary_intent: Intención principal
            - secondary_intents: Lista de intenciones secundarias
            - confidence: 0.0 - 1.0
            - entities: Entidades extraídas (productos, fechas, etc)
        """
        prompt = self._build_intent_prompt(request.message, request.context)
        
        # Obtener lista de intenciones válidas
        valid_intents = [intent.value for intent in IntentType]
        
        try:
            result = await self.ai.detect_intent(
                prompt=prompt,
                valid_intents=valid_intents
            )
            
            # Guardar en DB
            await self._save_intent(request, result, db)
            
            return result
        except Exception as e:
            logger.error("intent_detection_failed", error=str(e))
            # Fallback
            return IntentDetectionResult(
                primary_intent="general_inquiry",
                secondary_intents=[],
                confidence=0.5,
                entities={},
                reasoning="Error en detección de intención",
                error=str(e)
            )
    
    def _build_intent_prompt(
        self,
        message: str,
        context: Optional[Dict] = None
    ) -> str:
        return f"""
        Analiza el siguiente mensaje y detecta la intención del usuario.
        
        MENSAJE: "{message}"
        
        {f"CONTEXTO: {context}" if context else ""}
        
        INTENCIONES POSIBLES:
        {self._format_intents_description()}
        
        INSTRUCCIONES:
        1. Identifica la intención PRIMARIA (la más importante)
        2. Si hay intenciones secundarias, listalas
        3. Asigna nivel de confianza (0-100%)
        4. Extrae entidades mencionadas (productos, cantidades, fechas)
        
        RESPONDE EN JSON:
        {{
          "primary_intent": "purchase_inquiry",
          "secondary_intents": ["pricing_question"],
          "confidence": 0.92,
          "entities": {{
            "products": ["laptop", "mouse"],
            "quantity": 2,
            "urgency": "this week"
          }},
          "reasoning": "Usuario pregunta por productos específicos con intención de compra"
        }}
        """
    
    def _format_intents_description(self) -> str:
        """Formatea descripción de intenciones"""
        descriptions = {
            "purchase_inquiry": "Quiere comprar",
            "product_info": "Pide información de producto",
            "pricing_question": "Pregunta sobre precios",
            "complaint": "Queja o reclamo",
            "support_request": "Solicita soporte técnico",
            "warranty_claim": "Reclamo de garantía",
            "delivery_tracking": "Consulta sobre estado de envío",
            "refund_request": "Solicita devolución",
            "partnership": "Propuesta de asociación B2B",
            "general_inquiry": "Consulta general",
            "spam": "Spam o irrelevante"
        }
        
        return "\n".join([f"- {intent}: {desc}" for intent, desc in descriptions.items()])
    
    async def _save_intent(
        self,
        request: IntentDetectionRequest,
        result: IntentDetectionResult,
        db: AsyncSession
    ):
        """Guarda la intención detectada en la base de datos"""
        if not request.lead_id:
            return
        
        intent = LeadIntent(
            lead_id=request.lead_id,
            message_id=request.message_id if hasattr(request, 'message_id') else None,
            primary_intent=result.primary_intent,
            secondary_intents=result.secondary_intents,
            confidence=result.confidence,
            entities=result.entities
        )
        db.add(intent)
        await db.commit()

