"""
Clasificador de Leads - FLUJO 2
"""
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.schemas.lead import LeadClassificationRequest, LeadScore
from app.models.lead import Lead
from app.models.classification import LeadClassification
from app.core.logging import get_logger
from datetime import datetime

logger = get_logger(__name__)


class LeadClassifier:
    """Clasifica leads usando IA"""
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
        if not self.ai:
            raise ValueError("No hay adaptador de IA disponible")
    
    async def classify(
        self,
        request: LeadClassificationRequest,
        db: AsyncSession
    ) -> LeadScore:
        """
        Clasifica un lead en base a su mensaje inicial y metadata.
        
        Scoring:
        - 80-100: Hot (requiere atención inmediata)
        - 50-79: Warm (interesado, seguimiento en 24h)
        - 0-49: Cold (bajo interés, nurturing automático)
        """
        prompt = self._build_prompt(request)
        
        try:
            # Llamada a IA
            response = await self.ai.classify_lead(prompt=prompt)
            
            # Validar respuesta
            if not (0 <= response.score <= 100):
                raise ValueError("Score fuera de rango")
            
            # Guardar en DB
            await self._save_classification(request, response, db)
            
            # Log para analytics
            logger.info(
                "lead_classified",
                lead_id=request.lead_id,
                score=response.score,
                category=response.category,
                model=self.ai.model_name
            )
            
            return response
            
        except Exception as e:
            logger.error(
                "classification_failed",
                lead_id=request.lead_id,
                error=str(e)
            )
            # Fallback a score neutro
            return LeadScore(
                score=50,
                category="warm",
                reasoning="Error en clasificación, asignado score neutro",
                recommended_action="reclassify",
                error=str(e)
            )
    
    def _build_prompt(self, request: LeadClassificationRequest) -> str:
        """Construye el prompt optimizado para clasificación."""
        return f"""
        Eres un experto en clasificación de leads para ventas B2B/B2C.
        
        Analiza el siguiente mensaje y metadata del lead:
        
        MENSAJE: "{request.message}"
        
        METADATA:
        - Nombre: {request.sender_metadata.get('name', 'Desconocido')}
        - Interacciones previas: {request.sender_metadata.get('previous_interactions', 0)}
        - Fuente: {request.sender_metadata.get('source', 'Orgánico')}
        
        CRITERIOS DE SCORING:
        1. Urgencia (0-30 puntos)
        2. Poder de decisión (0-25 puntos)
        3. Budget aparente (0-25 puntos)
        4. Fit con producto (0-20 puntos)
        
        Retorna un JSON con:
        - score (0-100)
        - category (hot/warm/cold)
        - reasoning (explicación breve)
        - recommended_action (siguiente acción)
        """
    
    async def _save_classification(
        self,
        request: LeadClassificationRequest,
        result: LeadScore,
        db: AsyncSession
    ):
        """Guarda la clasificación en la base de datos"""
        # Obtener o crear lead
        lead = None
        if request.lead_id:
            lead = await db.get(Lead, request.lead_id)
        
        if not lead:
            # Crear nuevo lead
            lead = Lead(
                name=request.sender_metadata.get('name', 'Unknown'),
                email=request.sender_metadata.get('email'),
                phone=request.sender_metadata.get('phone'),
                company=request.sender_metadata.get('company'),
                source=request.sender_metadata.get('source', 'unknown'),
                score=result.score,
                category=result.category
            )
            db.add(lead)
            await db.flush()
        else:
            # Actualizar score y categoría
            lead.score = result.score
            lead.category = result.category
            await db.flush()
        
        # Crear registro de clasificación
        classification = LeadClassification(
            lead_id=lead.id,
            score=result.score,
            category=result.category,
            reasoning=result.reasoning,
            recommended_action=result.recommended_action,
            ai_model=result.ai_model_used or self.ai.model_name
        )
        db.add(classification)
        await db.commit()

