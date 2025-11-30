"""
Adaptador para OpenAI (GPT-4)
"""
from typing import Optional, Dict, Any, List
import json
import time
from openai import AsyncOpenAI
from app.ai.base import AIAdapter
from app.core.config import settings
from app.schemas.lead import LeadScore
from app.schemas.intent import IntentDetectionResult
from app.schemas.sentiment import SentimentResult
from app.core.logging import get_logger

logger = get_logger(__name__)


class OpenAIAdapter(AIAdapter):
    """Adaptador para OpenAI GPT"""
    
    def __init__(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY no configurada")
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self._model_name = settings.OPENAI_MODEL
    
    @property
    def model_name(self) -> str:
        return self._model_name
    
    async def classify_lead(
        self,
        prompt: str,
        response_format: Optional[type] = None
    ) -> LeadScore:
        """Clasifica un lead usando GPT"""
        start_time = time.time()
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Eres un experto en clasificación de leads. Responde siempre en formato JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            processing_time = int((time.time() - start_time) * 1000)
            
            return LeadScore(
                score=result.get("score", 50),
                category=result.get("category", "warm"),
                reasoning=result.get("reasoning", ""),
                recommended_action=result.get("recommended_action", ""),
                ai_model_used=self.model_name,
                processing_time_ms=processing_time
            )
        except Exception as e:
            logger.error("openai_classification_error", error=str(e))
            raise
    
    async def detect_intent(
        self,
        prompt: str,
        valid_intents: Optional[List[str]] = None
    ) -> IntentDetectionResult:
        """Detecta intención usando GPT"""
        try:
            system_prompt = "Eres un experto en detección de intenciones. Responde siempre en formato JSON válido."
            if valid_intents:
                system_prompt += f"\nIntenciones válidas: {', '.join(valid_intents)}"
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return IntentDetectionResult(
                primary_intent=result.get("primary_intent", "general_inquiry"),
                secondary_intents=result.get("secondary_intents", []),
                confidence=result.get("confidence", 0.5),
                entities=result.get("entities", {}),
                reasoning=result.get("reasoning"),
                ai_model_used=self.model_name
            )
        except Exception as e:
            logger.error("openai_intent_detection_error", error=str(e))
            raise
    
    async def analyze_sentiment(
        self,
        prompt: str
    ) -> SentimentResult:
        """Analiza sentimiento usando GPT"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Eres un experto en análisis de sentimiento. Responde siempre en formato JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            content = response.choices[0].message.content
            result = json.loads(content)
            
            return SentimentResult(
                sentiment=result.get("sentiment", "neutral"),
                score=result.get("score", 0.0),
                confidence=result.get("confidence", 0.5),
                emotions=result.get("emotions", {}),
                urgency_level=result.get("urgency_level"),
                recommended_priority=result.get("recommended_priority"),
                churn_risk=result.get("churn_risk"),
                ai_model_used=self.model_name
            )
        except Exception as e:
            logger.error("openai_sentiment_analysis_error", error=str(e))
            raise
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Genera respuesta conversacional"""
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("openai_chat_error", error=str(e))
            raise
    
    async def generate_response(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        """Genera respuesta genérica"""
        temperature = kwargs.get("temperature", 0.7)
        max_tokens = kwargs.get("max_tokens", 500)
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error("openai_generate_error", error=str(e))
            raise

