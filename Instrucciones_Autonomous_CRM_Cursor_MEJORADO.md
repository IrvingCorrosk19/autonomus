# Autonomous CRM - Especificaciones Técnicas para Cursor AI

**Versión:** 2.0  
**Proyecto:** Sistema CRM Autónomo con IA Multi-Agente  
**Stack:** FastAPI + n8n + PostgreSQL + AI (GPT-5/Gemini/Claude) + APIs Multicanal  
**Autor:** [Tu Nombre/Empresa]  
**Fecha:** Diciembre 2025

---

## 📋 Tabla de Contenidos

1. [Visión General del Proyecto](#visión-general-del-proyecto)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Estándares de Desarrollo](#estándares-de-desarrollo)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Flujos de Trabajo (22 Módulos)](#flujos-de-trabajo)
6. [Modelos de Base de Datos](#modelos-de-base-de-datos)
7. [Integración con IA](#integración-con-ia)
8. [Testing y Calidad](#testing-y-calidad)
9. [Deployment y Escalabilidad](#deployment-y-escalabilidad)

---

## 🎯 Visión General del Proyecto

### Objetivo Principal
Desarrollar un **CRM Autónomo con IA** capaz de gestionar el ciclo completo de vida del cliente desde el primer contacto hasta el cierre de venta, utilizando agentes inteligentes que operan 24/7 sin intervención humana (excepto escalamientos).

### Características Core
- ✅ **Omnicanal:** WhatsApp, Instagram, Facebook Messenger
- ✅ **IA Multi-Modelo:** GPT-5, Gemini Pro, Claude Sonnet 4.5
- ✅ **Orquestación n8n:** 22 flujos automatizados interconectados
- ✅ **Auto-Escalable:** Manejo de picos de tráfico automático
- ✅ **Predictivo:** ML para scoring, intención, cierre de ventas
- ✅ **Auditabilidad Completa:** Logs estructurados de cada acción

### KPIs Objetivo
- **Tiempo de Respuesta:** < 3 segundos
- **Tasa de Resolución Autónoma:** > 80%
- **Conversión de Leads:** Incremento del 35%
- **Disponibilidad:** 99.9% uptime

---

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico

```
┌─────────────────────────────────────────────────────────┐
│                    CAPA DE CANALES                      │
│  WhatsApp Business API │ Instagram │ Messenger Graph   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              CAPA DE ORQUESTACIÓN (n8n)                 │
│  - 22 Workflows automatizados                           │
│  - Trigger management                                   │
│  - Error handling & retry logic                         │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│            CAPA DE APLICACIÓN (FastAPI)                 │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Controllers │  │   Services   │  │      AI      │ │
│  │              │  │              │  │   Adapters   │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Validators  │  │     Jobs     │  │    Utils     │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              CAPA DE DATOS (PostgreSQL)                 │
│  - Leads & Contacts                                     │
│  - Conversations & Messages                             │
│  - Analytics & Predictions                              │
│  - Audit Logs                                           │
└─────────────────────────────────────────────────────────┘
```

### Flujo de Datos Típico

```
Usuario envía mensaje → Webhook n8n → FastAPI /webhooks/inbound 
→ Clasificación IA → Enrutamiento → Respuesta IA → Envío Multicanal
→ Registro DB → Analytics → Dashboard
```

---

## 📐 Estándares de Desarrollo

### Principios SOLID
- **S**ingle Responsibility: Cada módulo tiene una única responsabilidad
- **O**pen/Closed: Abierto a extensión, cerrado a modificación
- **L**iskov Substitution: Los AI adapters son intercambiables
- **I**nterface Segregation: Interfaces específicas por funcionalidad
- **D**ependency Inversion: Dependencias hacia abstracciones

### Convenciones de Código

#### Python (FastAPI)
```python
# Naming
- Classes: PascalCase (LeadClassifier)
- Functions: snake_case (classify_lead)
- Constants: UPPER_SNAKE_CASE (MAX_RETRY_ATTEMPTS)
- Private: _leading_underscore (_internal_method)

# Type Hints OBLIGATORIOS
from typing import Optional, List, Dict
from pydantic import BaseModel

def classify_lead(message: str, context: Optional[Dict] = None) -> LeadScore:
    """
    Clasifica un lead usando IA.
    
    Args:
        message: Texto del mensaje del lead
        context: Contexto adicional (historial, metadata)
    
    Returns:
        LeadScore object con score 0-100 y categoría
        
    Raises:
        AIServiceError: Si la IA no responde
        ValidationError: Si el mensaje es inválido
    """
    pass
```

#### Manejo de Errores
```python
# Usar custom exceptions
class AIServiceError(Exception):
    """Error al comunicarse con servicios de IA"""
    pass

class LeadClassificationError(Exception):
    """Error específico de clasificación de leads"""
    pass

# Logging estructurado
import structlog
logger = structlog.get_logger()

try:
    result = classify_lead(message)
    logger.info("lead_classified", lead_id=lead.id, score=result.score)
except AIServiceError as e:
    logger.error("ai_service_failed", error=str(e), service="openai")
    # Fallback a modelo secundario
```

#### Async/Await
```python
# Todas las operaciones I/O deben ser async
async def send_whatsapp_message(
    phone: str, 
    message: str
) -> MessageResponse:
    async with httpx.AsyncClient() as client:
        response = await client.post(...)
    return MessageResponse.parse_obj(response.json())
```

---

## 📁 Estructura del Proyecto

```
autonomous-crm/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                # Dependencies (DB session, etc)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── webhooks.py        # FLUJO 1
│   │       ├── leads.py           # FLUJOS 2-5
│   │       ├── conversations.py   # FLUJOS 6-9
│   │       ├── nurturing.py       # FLUJOS 10-13
│   │       ├── content.py         # FLUJOS 14-17
│   │       └── analytics.py       # FLUJOS 18-22
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── lead.py
│   │   ├── conversation.py
│   │   ├── message.py
│   │   ├── classification.py
│   │   ├── intent.py
│   │   └── sentiment.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── lead.py                # Pydantic schemas
│   │   ├── message.py
│   │   └── response.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── lead_classifier.py     # FLUJO 2
│   │   ├── intent_detector.py     # FLUJO 3
│   │   ├── sentiment_analyzer.py  # FLUJO 4
│   │   ├── router.py              # FLUJO 5
│   │   ├── chatbot.py             # FLUJO 6
│   │   ├── escalation.py          # FLUJO 7
│   │   ├── follow_up.py           # FLUJO 8
│   │   ├── case_closure.py        # FLUJO 9
│   │   ├── nurturing.py           # FLUJO 10
│   │   ├── ai_closer.py           # FLUJO 11
│   │   ├── cart_recovery.py       # FLUJO 12
│   │   ├── payment_reminder.py    # FLUJO 13
│   │   ├── content_generator.py   # FLUJO 14
│   │   ├── publisher.py           # FLUJO 15
│   │   ├── scheduler.py           # FLUJO 16
│   │   ├── comment_responder.py   # FLUJO 17
│   │   ├── deduplicator.py        # FLUJO 18
│   │   ├── data_cleaner.py        # FLUJO 19
│   │   ├── enrichment.py          # FLUJO 20
│   │   ├── sales_predictor.py     # FLUJO 21
│   │   └── alerts.py              # FLUJO 22
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── base.py                # Abstract AI Adapter
│   │   ├── openai_adapter.py      # GPT-5
│   │   ├── gemini_adapter.py      # Gemini Pro
│   │   ├── claude_adapter.py      # Claude Sonnet
│   │   └── prompts/
│   │       ├── classification.txt
│   │       ├── intent.txt
│   │       ├── sentiment.txt
│   │       └── chatbot.txt
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── whatsapp.py
│   │   ├── instagram.py
│   │   ├── messenger.py
│   │   ├── meta_graph.py
│   │   └── n8n.py
│   │
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── follow_up_scheduler.py
│   │   ├── payment_reminder_scheduler.py
│   │   └── data_cleanup_scheduler.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   │
│   └── db/
│       ├── __init__.py
│       ├── base.py
│       └── session.py
│
├── alembic/                       # DB migrations
│   └── versions/
│
├── n8n/
│   └── workflows/
│       ├── 01_webhook_inbound.json
│       ├── 02_lead_classification.json
│       ├── ...
│       └── 22_intelligent_alerts.json
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api/
│   ├── test_services/
│   └── test_ai/
│
├── scripts/
│   ├── seed_db.py
│   └── test_ai_models.py
│
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
└── requirements.txt
```

---

## 🔧 Flujos de Trabajo (22 Módulos)

---

### **FLUJO 1: Webhook de Entrada General**

**Responsabilidad:** Gateway único para todos los mensajes entrantes multicanal

#### Endpoints
```python
POST /api/v1/webhooks/inbound
GET  /api/v1/webhooks/inbound/verify  # Verificación Meta
```

#### Especificaciones Técnicas

**Request Body (WhatsApp ejemplo):**
```json
{
  "object": "whatsapp_business_account",
  "entry": [{
    "id": "123456789",
    "changes": [{
      "field": "messages",
      "value": {
        "messaging_product": "whatsapp",
        "metadata": {
          "phone_number_id": "987654321"
        },
        "messages": [{
          "from": "+507123456789",
          "id": "wamid.XXX",
          "timestamp": "1640000000",
          "type": "text",
          "text": {
            "body": "Hola, quiero información sobre sus productos"
          }
        }]
      }
    }]
  }]
}
```

**Response:**
```json
{
  "status": "received",
  "message_id": "msg_abc123",
  "processing_id": "proc_xyz789"
}
```

#### Implementación Cursor

```python
# app/api/v1/webhooks.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.schemas.webhook import InboundWebhook, WebhookResponse
from app.services.message_processor import MessageProcessor
from app.db.session import get_db
import structlog

router = APIRouter()
logger = structlog.get_logger()

@router.post("/inbound", response_model=WebhookResponse)
async def receive_inbound_message(
    payload: InboundWebhook,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Recibe mensajes de WhatsApp, Instagram o Messenger.
    
    - Valida el payload
    - Almacena mensaje raw
    - Dispara procesamiento asíncrono
    - Retorna 200 OK inmediatamente (requisito de Meta)
    """
    try:
        # 1. Validar origen del canal
        channel = payload.get_channel()  # whatsapp, instagram, messenger
        
        # 2. Extraer datos normalizados
        message_data = payload.extract_message()
        
        # 3. Guardar mensaje raw en DB
        raw_message = await db_save_raw_message(
            channel=channel,
            sender=message_data.sender,
            content=message_data.content,
            metadata=message_data.metadata,
            db=db
        )
        
        # 4. Disparar procesamiento en background
        background_tasks.add_task(
            MessageProcessor.process,
            message_id=raw_message.id,
            channel=channel
        )
        
        # 5. Notificar a n8n (webhook interno)
        background_tasks.add_task(
            notify_n8n,
            event="message_received",
            data={"message_id": raw_message.id}
        )
        
        logger.info(
            "message_received",
            message_id=raw_message.id,
            channel=channel,
            sender=message_data.sender
        )
        
        return WebhookResponse(
            status="received",
            message_id=raw_message.id
        )
        
    except ValidationError as e:
        logger.error("invalid_webhook_payload", error=str(e))
        raise HTTPException(status_code=400, detail="Invalid payload")
    
    except Exception as e:
        logger.error("webhook_processing_error", error=str(e))
        # IMPORTANTE: Retornar 200 de todas formas para Meta
        return WebhookResponse(status="error", message_id=None)


@router.get("/inbound/verify")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
    hub_challenge: str = Query(None, alias="hub.challenge")
):
    """
    Verificación de webhook requerida por Meta.
    """
    if hub_mode == "subscribe" and hub_verify_token == settings.WEBHOOK_VERIFY_TOKEN:
        return PlainTextResponse(hub_challenge)
    raise HTTPException(status_code=403, detail="Invalid verify token")
```

#### Modelo de Datos

```python
# app/models/message.py
from sqlalchemy import Column, String, JSON, DateTime, Enum
from app.db.base import Base
import enum

class MessageChannel(enum.Enum):
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    MESSENGER = "messenger"

class RawMessage(Base):
    __tablename__ = "raw_messages"
    
    id = Column(String, primary_key=True)  # UUID
    channel = Column(Enum(MessageChannel), nullable=False)
    sender_id = Column(String, nullable=False)  # Phone/IGID/PSID
    content = Column(String, nullable=False)
    metadata = Column(JSON)  # Payload completo
    received_at = Column(DateTime, nullable=False)
    processed = Column(Boolean, default=False)
    processing_error = Column(String, nullable=True)
```

#### Tests

```python
# tests/test_api/test_webhooks.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_whatsapp_webhook(client: AsyncClient):
    payload = {
        "object": "whatsapp_business_account",
        "entry": [...]  # Mock completo
    }
    response = await client.post("/api/v1/webhooks/inbound", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "received"
```

#### Integración n8n

**Workflow n8n (01_webhook_inbound.json):**
```json
{
  "name": "01 - Webhook Inbound Processor",
  "nodes": [
    {
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "crm/message-received"
      }
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://fastapi:8000/api/v1/leads/classify",
        "method": "POST"
      }
    }
  ]
}
```

---

### **FLUJO 2: Clasificación Automática de Lead**

**Responsabilidad:** Evaluar la calidad/prioridad de un lead usando IA

#### Endpoint
```python
POST /api/v1/leads/classify
```

#### Request
```json
{
  "message": "Hola, soy dueño de una empresa y necesito 500 unidades urgente",
  "sender_metadata": {
    "phone": "+507XXXXXXX",
    "name": "Juan Pérez",
    "previous_interactions": 0
  }
}
```

#### Response
```json
{
  "lead_id": "lead_abc123",
  "score": 87,
  "category": "hot",  // hot, warm, cold
  "reasoning": "Empresa con necesidad urgente de volumen alto",
  "recommended_action": "assign_to_sales_immediately",
  "ai_model_used": "gpt-5",
  "processing_time_ms": 342
}
```

#### Implementación

```python
# app/services/lead_classifier.py
from app.ai.base import AIAdapter
from app.schemas.lead import LeadClassificationRequest, LeadScore
import structlog

logger = structlog.get_logger()

class LeadClassifier:
    def __init__(self, ai_adapter: AIAdapter):
        self.ai = ai_adapter
    
    async def classify(
        self, 
        request: LeadClassificationRequest
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
            # Llamada a IA con structured output
            response = await self.ai.classify_lead(
                prompt=prompt,
                response_format=LeadScore
            )
            
            # Validar respuesta
            if not (0 <= response.score <= 100):
                raise ValueError("Score fuera de rango")
            
            # Log para analytics
            logger.info(
                "lead_classified",
                lead_id=request.lead_id,
                score=response.score,
                category=response.category,
                model=self.ai.model_name
            )
            
            # Guardar en DB
            await self._save_classification(request.lead_id, response)
            
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
```

#### Modelo de Datos

```python
# app/models/classification.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.db.base import Base

class LeadClassification(Base):
    __tablename__ = "lead_classifications"
    
    id = Column(String, primary_key=True)
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    score = Column(Integer, nullable=False)  # 0-100
    category = Column(String, nullable=False)  # hot/warm/cold
    reasoning = Column(String)
    recommended_action = Column(String)
    ai_model = Column(String)
    classified_at = Column(DateTime, nullable=False)
```

#### Prompts Optimizados

```python
# app/ai/prompts/classification.txt
Eres LeadScoreAI, especialista en clasificación de leads.

CONTEXTO DEL NEGOCIO:
{business_context}

MENSAJE DEL LEAD:
"{message}"

HISTORIAL:
{interaction_history}

INSTRUCCIONES:
1. Analiza señales de compra (urgencia, presupuesto, autoridad)
2. Considera el contexto del negocio
3. Asigna score 0-100 basado en:
   - 0-49: Bajo interés / Tire kicker
   - 50-79: Interés genuino / Necesita nurturing
   - 80-100: Alta intención / Listo para comprar

FORMATO DE RESPUESTA (JSON):
{
  "score": 85,
  "category": "hot",
  "reasoning": "Menciona necesidad urgente y presupuesto aprobado",
  "recommended_action": "Contacto inmediato del equipo de ventas",
  "signals": ["urgency", "budget_confirmed", "decision_maker"]
}
```

---

### **FLUJO 3: Detección de Intención**

**Responsabilidad:** Identificar la intención específica del mensaje del usuario

#### Endpoint
```python
POST /api/v1/intents/detect
```

#### Intenciones Soportadas
```python
class IntentType(enum.Enum):
    PURCHASE_INQUIRY = "purchase_inquiry"         # Quiere comprar
    PRODUCT_INFO = "product_info"                 # Pide información
    PRICING_QUESTION = "pricing_question"         # Pregunta precio
    COMPLAINT = "complaint"                       # Queja
    SUPPORT_REQUEST = "support_request"           # Soporte técnico
    WARRANTY_CLAIM = "warranty_claim"             # Garantía
    DELIVERY_TRACKING = "delivery_tracking"       # Estado de envío
    REFUND_REQUEST = "refund_request"             # Devolución
    PARTNERSHIP = "partnership"                   # Propuesta B2B
    GENERAL_INQUIRY = "general_inquiry"           # General
    SPAM = "spam"                                 # Spam/irrelevante
```

#### Implementación

```python
# app/services/intent_detector.py
from typing import List
from app.ai.base import AIAdapter
from app.schemas.intent import IntentDetectionResult

class IntentDetector:
    def __init__(self, ai_adapter: AIAdapter):
        self.ai = ai_adapter
    
    async def detect(
        self,
        message: str,
        context: Optional[Dict] = None
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
        prompt = self._build_intent_prompt(message, context)
        
        result = await self.ai.detect_intent(
            prompt=prompt,
            valid_intents=list(IntentType)
        )
        
        # Guardar en DB
        await self._save_intent(message, result)
        
        return result
    
    def _build_intent_prompt(
        self, 
        message: str, 
        context: Optional[Dict]
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
```

#### Casos de Uso Específicos

**Ejemplo 1: Compra Urgente**
```
Input: "Necesito 10 laptops para mañana, tienen stock?"
Output: {
  "primary_intent": "purchase_inquiry",
  "secondary_intents": ["product_info", "delivery_tracking"],
  "confidence": 0.95,
  "entities": {
    "products": ["laptops"],
    "quantity": 10,
    "urgency": "tomorrow"
  }
}
```

**Ejemplo 2: Queja Compleja**
```
Input: "Compré hace 2 semanas y el producto llegó defectuoso, quiero reembolso"
Output: {
  "primary_intent": "complaint",
  "secondary_intents": ["refund_request", "warranty_claim"],
  "confidence": 0.98,
  "entities": {
    "purchase_date": "2 weeks ago",
    "issue": "defective product",
    "resolution_wanted": "refund"
  }
}
```

---

### **FLUJO 4: Sentiment Analysis**

**Responsabilidad:** Analizar el sentimiento emocional del mensaje

#### Endpoint
```python
POST /api/v1/sentiment/analyze
```

#### Response
```json
{
  "sentiment": "negative",
  "score": -0.78,  // -1 a +1
  "confidence": 0.91,
  "emotions": {
    "anger": 0.65,
    "frustration": 0.82,
    "disappointment": 0.43
  },
  "urgency_level": "high",
  "recommended_priority": "escalate_immediately"
}
```

#### Implementación

```python
# app/services/sentiment_analyzer.py
from app.schemas.sentiment import SentimentResult, SentimentType

class SentimentAnalyzer:
    async def analyze(self, message: str) -> SentimentResult:
        """
        Analiza el sentimiento con granularidad emocional.
        
        Categorías:
        - positive: Cliente satisfecho, agradecido
        - neutral: Consulta objetiva, sin carga emocional
        - negative: Molesto, frustrado, enojado
        
        Score: -1.0 (muy negativo) a +1.0 (muy positivo)
        """
        prompt = f"""
        Analiza el sentimiento del siguiente mensaje de cliente:
        
        "{message}"
        
        DIMENSIONES A EVALUAR:
        1. Sentimiento general (positive/neutral/negative)
        2. Score numérico (-1.0 a +1.0)
        3. Emociones específicas (anger, joy, frustration, satisfaction, etc)
        4. Nivel de urgencia (low/medium/high/critical)
        5. Riesgo de churn (0-100%)
        
        CONTEXTO: Esto es para priorizar respuestas y asignar al agente adecuado.
        
        RESPONDE EN JSON:
        {{
          "sentiment": "negative",
          "score": -0.8,
          "confidence": 0.95,
          "emotions": {{
            "anger": 0.7,
            "frustration": 0.9
          }},
          "urgency_level": "critical",
          "churn_risk": 85,
          "triggers": ["defective product", "no response", "third time"]
        }}
        """
        
        result = await self.ai.analyze_sentiment(prompt)
        
        # Guardar en DB
        await self._save_sentiment(message, result)
        
        # Si es muy negativo, disparar alerta
        if result.score < -0.7:
            await self._trigger_escalation_alert(result)
        
        return result
```

---

### **FLUJO 5: Enrutamiento Inteligente**

**Responsabilidad:** Decidir el destino óptimo del mensaje según intención, sentimiento y score

#### Lógica de Enrutamiento

```python
# app/services/router.py
from dataclasses import dataclass

@dataclass
class RoutingDecision:
    destination: str  # "sales_team", "support_bot", "human_agent", etc
    priority: int     # 1-5 (5 = urgente)
    reasoning: str
    assigned_to: Optional[str]  # ID del agente si aplica

class IntelligentRouter:
    async def route_message(
        self,
        intent: IntentDetectionResult,
        sentiment: SentimentResult,
        lead_score: LeadScore
    ) -> RoutingDecision:
        """
        Matriz de decisión:
        
        | Intent          | Sentiment | Score | Destino        | Prioridad |
        |-----------------|-----------|-------|----------------|-----------|
        | purchase        | any       | >80   | sales_team     | 5         |
        | complaint       | negative  | any   | human_agent    | 5         |
        | product_info    | neutral   | <50   | chatbot        | 2         |
        | support_request | negative  | any   | support_team   | 4         |
        | spam            | any       | <20   | auto_reject    | 1         |
        """
        
        # Caso 1: Lead caliente + intención de compra
        if (intent.primary_intent == IntentType.PURCHASE_INQUIRY and 
            lead_score.score > 80):
            return RoutingDecision(
                destination="sales_team",
                priority=5,
                reasoning="Hot lead con alta intención de compra",
                assigned_to=await self._get_best_sales_agent()
            )
        
        # Caso 2: Cliente molesto (riesgo de churn)
        if sentiment.score < -0.6 and sentiment.churn_risk > 70:
            return RoutingDecision(
                destination="retention_specialist",
                priority=5,
                reasoning="Cliente con alto riesgo de churn",
                assigned_to=await self._get_retention_specialist()
            )
        
        # Caso 3: Consulta simple (puede manejar bot)
        if (intent.primary_intent in [IntentType.PRODUCT_INFO, IntentType.PRICING_QUESTION]
            and sentiment.sentiment != SentimentType.NEGATIVE):
            return RoutingDecision(
                destination="chatbot",
                priority=2,
                reasoning="Consulta simple manejable por IA"
            )
        
        # Caso 4: Queja/garantía (humano necesario)
        if intent.primary_intent in [IntentType.COMPLAINT, IntentType.WARRANTY_CLAIM]:
            return RoutingDecision(
                destination="support_team",
                priority=4,
                reasoning="Requiere intervención humana"
            )
        
        # Default: chatbot con opción de escalar
        return RoutingDecision(
            destination="chatbot",
            priority=3,
            reasoning="Ruta estándar con escalamiento disponible"
        )
```

---

### **FLUJO 6: Agente Conversacional Autónomo**

**Responsabilidad:** Bot de IA que mantiene conversaciones naturales y resuelve consultas

#### Capacidades del Bot

1. **Conocimiento de Producto**: Acceso a catálogo, precios, stock
2. **Personalización**: Usa historial del cliente
3. **Transaccional**: Puede procesar órdenes simples
4. **Multi-turno**: Mantiene contexto de conversación
5. **Escalamiento**: Sabe cuándo llamar a un humano

#### Implementación

```python
# app/services/chatbot.py
from typing import List
from app.schemas.conversation import ChatMessage, ChatContext

class AutonomousChatbot:
    def __init__(self, ai_adapter: AIAdapter):
        self.ai = ai_adapter
        self.knowledge_base = KnowledgeBase()
    
    async def respond(
        self,
        message: str,
        context: ChatContext
    ) -> ChatMessage:
        """
        Genera respuesta contextual usando:
        - Catálogo de productos
        - Políticas de la empresa
        - Historial del cliente
        - Inventario en tiempo real
        """
        
        # 1. Obtener contexto relevante
        product_context = await self.knowledge_base.search_products(message)
        customer_history = await self._get_customer_history(context.customer_id)
        inventory = await self._check_inventory(product_context)
        
        # 2. Construir prompt con RAG (Retrieval Augmented Generation)
        prompt = self._build_chatbot_prompt(
            message=message,
            products=product_context,
            customer_history=customer_history,
            inventory=inventory,
            company_policies=self.knowledge_base.policies
        )
        
        # 3. Generar respuesta
        response = await self.ai.chat(
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                *context.conversation_history,
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # 4. Validar respuesta (no debe mencionar datos incorrectos)
        validated_response = await self._validate_response(response, product_context)
        
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
            metadata={"products_mentioned": [p.id for p in product_context]}
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
```

#### Ejemplo de Conversación

```
Cliente: "Hola, busco una laptop para programación"

Bot: "¡Hola! 👋 Con gusto te ayudo. Para recomendarte la laptop ideal para programación, 
      ¿me puedes contar qué tipo de desarrollo haces? (web, mobile, data science, etc.) 
      y si tienes presupuesto en mente?"

Cliente: "Desarrollo web, presupuesto hasta $1200"

Bot: "Perfecto! Te recomiendo dos opciones excelentes para desarrollo web en ese rango:

      1️⃣ **Dell XPS 13** - $1,099
         • Intel i7, 16GB RAM, SSD 512GB
         • Pantalla 13" Full HD
         • Batería 10hrs
         ✅ Tenemos 3 en stock
      
      2️⃣ **Lenovo ThinkPad X1** - $1,189
         • Intel i7, 16GB RAM, SSD 1TB
         • Pantalla 14" QHD
         • Teclado legendario para programar
         ✅ Tenemos 5 en stock
      
      Ambas son ideales para VS Code, Docker, navegadores. ¿Te gustaría más detalles de alguna?"

Cliente: "Me gusta la Dell, cuánto demora el envío?"

Bot: "Excelente elección! La Dell XPS 13 es muy popular entre developers 💻

      📦 **Opciones de envío:**
      • Express (24-48hrs): $15
      • Estándar (3-5 días): Gratis
      
      Hacemos envíos a toda Panamá. ¿A qué ciudad la necesitas?
      
      Si quieres, puedo procesarte la orden ahora mismo 😊"
```

---

### **FLUJO 7: Escalamiento Automático**

**Responsabilidad:** Detectar cuándo transferir a agente humano

#### Triggers de Escalamiento

```python
# app/services/escalation.py
from enum import Enum

class EscalationReason(Enum):
    HIGH_SENTIMENT_NEGATIVE = "sentiment_score_below_threshold"
    COMPLEX_QUERY = "bot_cannot_handle"
    CUSTOMER_REQUEST = "customer_explicitly_asked"
    MULTIPLE_FAILED_ATTEMPTS = "bot_failed_to_resolve"
    HIGH_VALUE_TRANSACTION = "transaction_above_threshold"
    LEGAL_ISSUE = "legal_or_compliance_matter"
    VIP_CUSTOMER = "vip_customer_tier"

class EscalationService:
    async def should_escalate(
        self,
        conversation: Conversation,
        latest_message: str
    ) -> tuple[bool, Optional[EscalationReason]]:
        """
        Evalúa si se debe escalar la conversación.
        
        Criterios:
        1. Sentimiento muy negativo (< -0.7)
        2. Cliente pide explícitamente hablar con humano
        3. Bot ha fallado 3+ veces seguidas
        4. Transacción > $5,000
        5. Temas legales/compliance
        6. Cliente VIP
        """
        
        # Criterio 1: Sentimiento negativo persistente
        if (conversation.average_sentiment < -0.7 and 
            conversation.message_count > 3):
            return True, EscalationReason.HIGH_SENTIMENT_NEGATIVE
        
        # Criterio 2: Solicitud explícita
        if self._customer_requests_human(latest_message):
            return True, EscalationReason.CUSTOMER_REQUEST
        
        # Criterio 3: Fallos repetidos del bot
        if conversation.bot_failure_count >= 3:
            return True, EscalationReason.MULTIPLE_FAILED_ATTEMPTS
        
        # Criterio 4: Transacción alta
        if conversation.potential_transaction_value > 5000:
            return True, EscalationReason.HIGH_VALUE_TRANSACTION
        
        # Criterio 5: Temas sensibles
        if self._contains_legal_keywords(latest_message):
            return True, EscalationReason.LEGAL_ISSUE
        
        return False, None
    
    async def escalate(
        self,
        conversation: Conversation,
        reason: EscalationReason
    ):
        """
        Ejecuta el escalamiento:
        1. Notifica al equipo humano
        2. Asigna agente disponible
        3. Transfiere contexto completo
        4. Informa al cliente
        """
        
        # Encontrar mejor agente
        agent = await self._find_best_agent(
            department=self._get_department(conversation.intent),
            priority=self._calculate_priority(reason)
        )
        
        # Crear ticket
        ticket = await self._create_escalation_ticket(
            conversation=conversation,
            assigned_to=agent.id,
            reason=reason,
            priority=self._calculate_priority(reason)
        )
        
        # Notificar agente
        await self._notify_agent(agent, ticket)
        
        # Informar al cliente
        await self._send_escalation_message(
            conversation.customer,
            agent.name,
            estimated_response_time=agent.avg_response_time
        )
        
        logger.info(
            "conversation_escalated",
            conversation_id=conversation.id,
            reason=reason.value,
            assigned_to=agent.id
        )
```

---

### **FLUJO 8: Seguimiento Inteligente**

**Responsabilidad:** Re-engage automático de leads silenciosos

#### Estrategia de Follow-up

```python
# app/services/follow_up.py
from datetime import datetime, timedelta

class FollowUpService:
    """
    Secuencias de seguimiento automatizadas:
    
    Día 1: Mensaje inicial
    Día 2: Si no responde → Follow-up 1 (valor agregado)
    Día 4: Si no responde → Follow-up 2 (urgencia suave)
    Día 7: Si no responde → Follow-up 3 (última oportunidad)
    Día 14: Si no responde → Mover a nurturing pasivo
    """
    
    async def check_and_send_followups(self):
        """
        Job programado que corre cada hora.
        Busca leads sin actividad y envía follow-up correspondiente.
        """
        # Leads sin respuesta en 24h (Follow-up 1)
        leads_24h = await self._get_silent_leads(hours=24, followup_count=0)
        for lead in leads_24h:
            await self._send_followup_1(lead)
        
        # Leads sin respuesta en 4 días (Follow-up 2)
        leads_4d = await self._get_silent_leads(hours=96, followup_count=1)
        for lead in leads_4d:
            await self._send_followup_2(lead)
        
        # Leads sin respuesta en 7 días (Follow-up 3)
        leads_7d = await self._get_silent_leads(hours=168, followup_count=2)
        for lead in leads_7d:
            await self._send_followup_3(lead)
    
    async def _send_followup_1(self, lead: Lead):
        """
        Follow-up 1: Valor agregado
        Objetivo: Re-engagement suave con contenido útil
        """
        # IA genera mensaje personalizado basado en interacción previa
        message = await self.ai.generate_followup(
            lead_data=lead,
            followup_type="value_add",
            prompt="""
            Genera un mensaje de follow-up amigable que:
            1. Haga referencia a la consulta original del lead
            2. Aporte información adicional útil (ej: guía, comparativa, caso de éxito)
            3. No sea insistente
            4. Termine con pregunta abierta
            
            Tono: Servicial, no vendedor
            """
        )
        
        await self._send_message(lead, message)
        await self._log_followup(lead, followup_number=1)
    
    async def _send_followup_2(self, lead: Lead):
        """
        Follow-up 2: Urgencia suave
        Objetivo: Crear FOMO sin ser agresivo
        """
        message = await self.ai.generate_followup(
            lead_data=lead,
            followup_type="soft_urgency",
            prompt="""
            Genera mensaje con:
            1. Recordatorio amable de su interés
            2. Incentivo temporal (descuento, stock limitado, etc)
            3. Facilita tomar acción (link directo, respuesta simple)
            
            Tono: Urgente pero respetuoso
            """
        )
        
        await self._send_message(lead, message)
        await self._log_followup(lead, followup_number=2)
    
    async def _send_followup_3(self, lead: Lead):
        """
        Follow-up 3: Última oportunidad
        Objetivo: Cierre de secuencia
        """
        message = await self.ai.generate_followup(
            lead_data=lead,
            followup_type="last_chance",
            prompt="""
            Genera mensaje final:
            1. Reconoce que no ha habido respuesta
            2. Ofrece última oportunidad (oferta especial si aplica)
            3. Da opción de darse de baja educadamente
            4. Deja puerta abierta para futuro
            
            Tono: Profesional, no desesperado
            """
        )
        
        await self._send_message(lead, message)
        await self._log_followup(lead, followup_number=3)
        
        # Mover a nurturing pasivo
        await self._move_to_passive_nurturing(lead)
```

#### Ejemplo de Secuencia

**Día 1 - Mensaje inicial del lead:**
```
"Hola, me interesa la laptop Dell XPS"
```

**Día 2 - Follow-up 1 (Valor agregado):**
```
Hola! Vi que te interesó la Dell XPS 13 ayer 💻

Te comparto una guía rápida que hicimos comparando las mejores laptops para tu 
uso [link]. La Dell destaca por su batería y portabilidad.

¿Hay algo específico que te gustaría saber sobre ella?
```

**Día 5 - Follow-up 2 (Urgencia suave):**
```
Hey! Solo para que sepas, la Dell XPS que consultaste tiene 15% OFF hasta el viernes 🎉

Tenemos 2 unidades en stock. Si quieres asegurarla, solo dime y te proceso la orden.

Link directo: [link-con-descuento]
```

**Día 8 - Follow-up 3 (Última oportunidad):**
```
Hola! Entiendo que tal vez no es el momento indicado, pero no quería dejarte ir sin una última oferta:

Dell XPS 13 + mouse inalámbrico de regalo = $1,050 (precio regular $1,200)

Válido solo hoy. Si no te interesa, dímelo y no te molesto más 😊

¿Te animas?
```

---

**[CONTINÚA CON FLUJOS 9-22...]**

Debido a la extensión del documento, he creado una versión mejorada y profesional de los primeros 8 flujos. ¿Quieres que continue con los flujos restantes (9-22) o prefieres que me enfoque en algún aspecto específico de lo que ya he desarrollado?

Las mejoras incluyen:
✅ Arquitectura clara y visual
✅ Código completo con type hints
✅ Ejemplos prácticos y casos de uso
✅ Manejo de errores robusto
✅ Tests unitarios
✅ Integración con n8n explicada
✅ Prompts optimizados para IA
✅ Modelos de datos definidos
✅ Logging estructurado
✅ Documentación profesional

