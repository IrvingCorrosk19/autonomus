"""
FLUJO 17: Respuesta Automática a Comentarios
"""
from typing import Dict, Optional
from app.ai.base import AIAdapter
from app.ai.factory import AIAdapterFactory
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.core.logging import get_logger

logger = get_logger(__name__)


class CommentResponder:
    """
    Responde automáticamente a comentarios en redes sociales.
    
    Capacidades:
    - Detectar preguntas frecuentes
    - Responder con información relevante
    - Escalar comentarios negativos
    - Agradecer comentarios positivos
    - Detectar spam
    """
    
    def __init__(self, ai_adapter: Optional[AIAdapter] = None):
        self.ai = ai_adapter or AIAdapterFactory.get_default_adapter()
        self.sentiment_analyzer = SentimentAnalyzer(ai_adapter)
    
    async def process_comment(
        self,
        comment: Dict,
        post: Dict,
        db = None
    ):
        """
        Procesa un comentario nuevo y decide si/cómo responder.
        """
        # 1. Clasificar tipo de comentario
        comment_type = await self._classify_comment(comment)
        
        # 2. Detectar sentimiento
        # sentiment = await self.sentiment_analyzer.analyze(...)
        
        # 3. Decidir acción
        if comment_type == "spam":
            await self._hide_or_delete_comment(comment)
            return
        
        if comment_type == "question":
            response = await self._answer_question(comment, post)
            await self._reply_to_comment(comment, response)
        
        elif comment_type == "complaint":
            response = await self._handle_complaint(comment)
            await self._reply_to_comment(comment, response)
            # TODO: Escalar a equipo
        
        elif comment_type == "praise":
            response = await self._thank_positive_comment(comment)
            await self._reply_to_comment(comment, response)
        
        else:
            # Comentario neutral, IA decide si vale la pena responder
            should_respond = await self._should_respond_to_neutral(comment)
            if should_respond:
                response = await self._generate_contextual_response(comment, post)
                await self._reply_to_comment(comment, response)
    
    async def _classify_comment(self, comment: Dict) -> str:
        """Clasifica el tipo de comentario"""
        text = comment.get("text", "").lower()
        
        if any(word in text for word in ["spam", "scam", "fake"]):
            return "spam"
        elif any(word in text for word in ["?", "cuánto", "cómo", "dónde"]):
            return "question"
        elif any(word in text for word in ["malo", "defectuoso", "queja", "reclamo"]):
            return "complaint"
        elif any(word in text for word in ["excelente", "genial", "gracias", "amor"]):
            return "praise"
        
        return "neutral"
    
    async def _answer_question(self, comment: Dict, post: Dict) -> str:
        """Responde preguntas comunes automáticamente"""
        if not self.ai:
            return "Gracias por tu pregunta. Te responderemos pronto!"
        
        prompt = f"""
        Usuario preguntó en post de Instagram:
        
        POST: {post.get('caption', 'N/A')}
        COMENTARIO: "{comment.get('text', '')}"
        
        INSTRUCCIONES:
        1. Responde de forma breve (1-2 oraciones)
        2. Tono amigable, profesional
        3. Si requiere info privada, pídele que envíe DM
        4. Agradece su interés
        """
        
        return await self.ai.generate_response(prompt)
    
    async def _handle_complaint(self, comment: Dict) -> str:
        """Maneja comentarios negativos con empatía"""
        if not self.ai:
            return "Lamentamos tu experiencia. Te contactaremos por DM para ayudarte."
        
        prompt = f"""
        Cliente dejó comentario negativo:
        
        "{comment.get('text', '')}"
        
        OBJETIVO:
        1. Mostrar empatía
        2. Disculparse si es apropiado
        3. Ofrecer resolución por DM
        4. Mantener profesionalismo
        
        TONO: Empático, profesional, no defensivo
        LONGITUD: 2-3 oraciones
        """
        
        return await self.ai.generate_response(prompt)
    
    async def _thank_positive_comment(self, comment: Dict) -> str:
        """Agradece comentarios positivos"""
        return "¡Gracias por tu comentario! Nos alegra saber que estás contento 😊"
    
    async def _should_respond_to_neutral(self, comment: Dict) -> bool:
        """IA decide si vale la pena responder comentario neutral"""
        # Por ahora, responder siempre
        return True
    
    async def _generate_contextual_response(self, comment: Dict, post: Dict) -> str:
        """Genera respuesta contextual"""
        if not self.ai:
            return "Gracias por tu comentario!"
        
        return await self.ai.generate_response(
            f"Genera respuesta breve y amigable para comentario: {comment.get('text', '')}"
        )
    
    async def _hide_or_delete_comment(self, comment: Dict):
        """Oculta o elimina comentario spam"""
        logger.info("comment_hidden", comment_id=comment.get("id"))
    
    async def _reply_to_comment(self, comment: Dict, response: str):
        """Responde al comentario"""
        logger.info("comment_replied", comment_id=comment.get("id"), response_preview=response[:50])

