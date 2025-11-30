"""
Adaptador base abstracto para servicios de IA
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from app.schemas.lead import LeadScore
from app.schemas.intent import IntentDetectionResult
from app.schemas.sentiment import SentimentResult


class AIAdapter(ABC):
    """Interfaz base para adaptadores de IA"""
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Nombre del modelo usado"""
        pass
    
    @abstractmethod
    async def classify_lead(
        self,
        prompt: str,
        response_format: Optional[type] = None
    ) -> LeadScore:
        """Clasifica un lead"""
        pass
    
    @abstractmethod
    async def detect_intent(
        self,
        prompt: str,
        valid_intents: Optional[List[str]] = None
    ) -> IntentDetectionResult:
        """Detecta la intención de un mensaje"""
        pass
    
    @abstractmethod
    async def analyze_sentiment(
        self,
        prompt: str
    ) -> SentimentResult:
        """Analiza el sentimiento de un mensaje"""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Genera una respuesta conversacional"""
        pass
    
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        **kwargs
    ) -> str:
        """Genera una respuesta genérica"""
        pass

