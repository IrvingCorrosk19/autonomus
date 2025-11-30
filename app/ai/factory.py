"""
Factory para crear adaptadores de IA
"""
from typing import Optional
from app.ai.base import AIAdapter
from app.ai.openai_adapter import OpenAIAdapter
from app.ai.anthropic_adapter import AnthropicAdapter
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class AIAdapterFactory:
    """Factory para crear adaptadores de IA"""
    
    @staticmethod
    def create_adapter(provider: str = "openai") -> AIAdapter:
        """
        Crea un adaptador de IA según el proveedor especificado.
        
        Args:
            provider: "openai", "anthropic", o "gemini"
        
        Returns:
            Instancia del adaptador
        """
        try:
            if provider.lower() == "openai":
                return OpenAIAdapter()
            elif provider.lower() == "anthropic" or provider.lower() == "claude":
                return AnthropicAdapter()
            elif provider.lower() == "gemini" or provider.lower() == "google":
                # TODO: Implementar cuando esté disponible
                raise NotImplementedError("Gemini adapter no implementado aún")
            else:
                raise ValueError(f"Proveedor de IA desconocido: {provider}")
        except Exception as e:
            logger.error("ai_adapter_creation_error", provider=provider, error=str(e))
            # Fallback a OpenAI si está disponible
            if provider.lower() != "openai" and settings.OPENAI_API_KEY:
                logger.warning("falling_back_to_openai")
                return OpenAIAdapter()
            raise
    
    @staticmethod
    def get_default_adapter() -> Optional[AIAdapter]:
        """Obtiene el adaptador por defecto según configuración"""
        # Prioridad: OpenAI > Anthropic > Gemini
        if settings.OPENAI_API_KEY:
            try:
                return OpenAIAdapter()
            except:
                pass
        
        if settings.ANTHROPIC_API_KEY:
            try:
                return AnthropicAdapter()
            except:
                pass
        
        logger.error("no_ai_adapter_available")
        return None

