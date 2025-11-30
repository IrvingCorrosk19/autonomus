# 🎯 COMANDOS CURSOR - COPY & PASTE READY

**Versión:** 1.0  
**Proyecto:** Autonomous CRM  
**Uso:** Copia y pega estos comandos directamente en Cursor AI

---

## 📋 ÍNDICE DE COMANDOS

1. [Inicialización del Proyecto](#1-inicialización-del-proyecto)
2. [Core Setup](#2-core-setup)
3. [Base de Datos](#3-base-de-datos)
4. [Servicios IA](#4-servicios-ia)
5. [API Endpoints](#5-api-endpoints)
6. [Testing](#6-testing)
7. [Docker & Deploy](#7-docker--deploy)
8. [Workflows n8n](#8-workflows-n8n)
9. [Scripts Utilities](#9-scripts-utilities)

---

## 1️⃣ INICIALIZACIÓN DEL PROYECTO

### Comando 1.1: Crear estructura completa
```
@workspace Crea la estructura completa del proyecto Autonomous CRM siguiendo esta especificación:

ESTRUCTURA:
autonomous-crm/
├── app/
│   ├── api/v1/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── ai/
│   ├── integrations/
│   ├── jobs/
│   ├── core/
│   └── db/
├── alembic/versions/
├── tests/
│   ├── test_api/
│   └── test_services/
├── scripts/
├── n8n/workflows/
└── docs/

ARCHIVOS ROOT:
- requirements.txt
- .env.example
- docker-compose.yml
- Dockerfile
- alembic.ini
- pytest.ini
- .gitignore
- README.md

Crea TODOS los directorios y archivos __init__.py necesarios.
Usa las convenciones de .cursorrules
```

### Comando 1.2: Generar requirements.txt
```
@workspace Crea requirements.txt con estas dependencias exactas:

# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# Database
sqlalchemy[asyncio]==2.0.23
asyncpg==0.29.0
alembic==1.13.0
psycopg2-binary==2.9.9

# AI/ML
openai==1.6.1
anthropic==0.8.0
tiktoken==0.5.2
tenacity==8.2.3

# HTTP Client
httpx==0.25.2

# Caching
redis==5.0.1
hiredis==2.2.3

# Background Jobs
apscheduler==3.10.4

# Validation
phonenumbers==8.13.26
email-validator==2.1.0
python-dotenv==1.0.0

# Logging
structlog==23.2.0

# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
pytest-mock==3.12.0
faker==20.1.0

# Code Quality
black==23.12.0
isort==5.13.2
flake8==6.1.0

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

Agrupa por categorías con comentarios.
```

### Comando 1.3: Generar .env.example
```
@workspace Crea .env.example con TODAS estas variables:

# ============= DATABASE =============
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/crm
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# ============= REDIS =============
REDIS_URL=redis://localhost:6379/0
REDIS_CACHE_TTL=3600

# ============= OPENAI =============
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4-turbo-preview
OPENAI_MAX_TOKENS=4000
OPENAI_TEMPERATURE=0.7
OPENAI_TIMEOUT=30

# ============= ANTHROPIC =============
ANTHROPIC_API_KEY=sk-ant-your-key-here
ANTHROPIC_MODEL=claude-sonnet-4-20250514
ANTHROPIC_MAX_TOKENS=4000

# ============= META APIS =============
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
META_ACCESS_TOKEN=your_access_token
META_VERIFY_TOKEN=your_verify_token
META_PHONE_NUMBER_ID=your_phone_number_id
META_INSTAGRAM_BUSINESS_ACCOUNT_ID=your_ig_id
META_PAGE_ID=your_page_id

# ============= WEBHOOKS =============
WEBHOOK_VERIFY_TOKEN=your_webhook_token
N8N_WEBHOOK_URL=http://n8n:5678/webhook/crm

# ============= SECURITY =============
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# ============= APPLICATION =============
APP_NAME=Autonomous CRM
APP_VERSION=1.0.0
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=INFO

# ============= CORS =============
ALLOWED_ORIGINS=http://localhost:3000
ALLOWED_HOSTS=*

# ============= JOBS =============
FOLLOW_UP_CHECK_INTERVAL_HOURS=1
CART_RECOVERY_CHECK_INTERVAL_HOURS=1
PAYMENT_REMINDER_CHECK_INTERVAL_HOURS=24

# ============= LIMITS =============
MAX_MESSAGE_LENGTH=4096
LEAD_SCORE_THRESHOLD_HOT=80
LEAD_SCORE_THRESHOLD_WARM=50

Incluye comentarios explicativos para cada sección.
```

---

## 2️⃣ CORE SETUP

### Comando 2.1: Implementar Config
```
@workspace Implementa app/core/config.py completo:

Requisitos:
1. Clase Settings usando pydantic-settings BaseSettings
2. Cargar TODAS las variables de .env.example
3. Validación de variables requeridas
4. Type hints completos
5. Valores por defecto apropiados
6. Docstrings
7. Instancia singleton settings al final

Estructura:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # Database
    database_url: str
    database_pool_size: int = 20
    
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4-turbo-preview"
    
    # ... todas las demás variables
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
```

Usa convenciones de .cursorrules
```

### Comando 2.2: Implementar Logging
```
@workspace Implementa app/core/logging.py con structlog:

Requisitos:
1. Configuración de structlog
2. Procesadores: TimeStamper, JSONRenderer, LogLevelAdder
3. Niveles configurables desde settings
4. Context processors para request_id
5. Función setup_logging()
6. Ejemplo de uso en docstring

Incluir:
- Formato JSON para producción
- Formato colorizado para desarrollo
- Logging de excepciones con traceback
- Configuración de loggers de librerías (uvicorn, sqlalchemy)

Template:
```python
import structlog
import logging
from app.core.config import settings

def setup_logging():
    """Configura logging estructurado para la aplicación."""
    
    processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True
    )
```

Usa convenciones de .cursorrules
```

### Comando 2.3: Implementar Security
```
@workspace Implementa app/core/security.py:

Funciones requeridas:
1. hash_password(password: str) -> str
2. verify_password(plain: str, hashed: str) -> bool
3. create_access_token(data: dict) -> str
4. verify_token(token: str) -> dict
5. get_password_hash (alias de hash_password)

Usar:
- passlib con bcrypt para passwords
- python-jose para JWT
- Settings para SECRET_KEY y ALGORITHM

Incluir:
- Type hints completos
- Docstrings con ejemplos
- Error handling
- Tests de ejemplo en docstring

Template:
```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash de password con bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verifica password contra hash."""
    return pwd_context.verify(plain, hashed)

# ... más funciones
```
```

---

## 3️⃣ BASE DE DATOS

### Comando 3.1: Setup Database Base
```
@workspace Implementa la capa de base de datos:

app/db/base.py:
```python
from sqlalchemy.orm import DeclarativeBase
from typing import Any

class Base(DeclarativeBase):
    """Base class para todos los modelos."""
    
    def __repr__(self) -> str:
        columns = ", ".join(
            f"{k}={repr(v)}"
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        )
        return f"{self.__class__.__name__}({columns})"
```

app/db/session.py:
```python
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from typing import AsyncGenerator
from app.core.config import settings

# Engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=settings.database_pool_size,
    max_overflow=settings.database_max_overflow
)

# Session maker
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
```

Usar SQLAlchemy 2.0+ SOLAMENTE.
```

### Comando 3.2: Crear Modelo Lead
```
@workspace Implementa app/models/lead.py:

Modelo Lead con estos campos:
- id: str (UUID, primary key)
- name: str (required, max 255)
- email: str (optional, max 255)
- phone: str (optional, max 50)
- company: str (optional, max 255)
- score: int (default 0, 0-100)
- category: str (optional: hot/warm/cold)
- status: str (default "new")
- source: str (optional: whatsapp/instagram/messenger)
- created_at: datetime (auto)
- updated_at: datetime (auto)

Usar SQLAlchemy 2.0 sintaxis:
- Mapped[tipo]
- mapped_column()
- UUID default con uuid.uuid4()
- Relationships con back_populates

Incluir:
- Indexes en email, phone, status
- __repr__ method
- Docstring

Template según .cursorrules
```

### Comando 3.3: Crear TODOS los modelos
```
@workspace Implementa TODOS los modelos en app/models/:

Archivos a crear:
1. lead.py - Lead model
2. customer.py - Customer model  
3. conversation.py - Conversation model
4. message.py - Message model
5. classification.py - LeadClassification model
6. intent.py - LeadIntent model
7. sentiment.py - SentimentResult model
8. case.py - Case model
9. cart.py - Cart model
10. purchase.py - Purchase model
11. invoice.py - Invoice model
12. content.py - GeneratedContent model
13. alert.py - Alert model

Para cada modelo:
- Usar Mapped[] y mapped_column()
- UUIDs como primary keys
- Timestamps (created_at, updated_at)
- Relationships apropiadas con back_populates
- Indexes en campos de búsqueda
- Enums para campos categóricos
- Type hints completos
- Docstrings

Referencia: DOCUMENTACION_COMPLETA.md sección "Modelos de Base de Datos"

Usa convenciones de .cursorrules
```

### Comando 3.4: Setup Alembic
```
@workspace Configura Alembic para migraciones:

1. Edita alembic.ini:
   - Configurar sqlalchemy.url = usar settings
   
2. Edita alembic/env.py:
   - Importar Base de app.db.base
   - Importar todos los modelos
   - Configurar target_metadata = Base.metadata
   - Async support

3. Crea migración inicial:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

Template env.py:
```python
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.db.base import Base
from app.core.config import settings

# Importar TODOS los modelos
from app.models.lead import Lead
from app.models.customer import Customer
# ... etc

target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", settings.database_url)
```
```

---

## 4️⃣ SERVICIOS IA

### Comando 4.1: Base AI Adapter
```
@workspace Implementa app/ai/base.py - Abstract AI Adapter:

```python
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class AIAdapter(ABC):
    """
    Interface abstracta para adaptadores de IA.
    
    Todos los adaptadores (OpenAI, Anthropic, etc) deben implementar esta interface.
    """
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """Nombre del modelo (e.g., 'gpt-4', 'claude-3')"""
        pass
    
    @abstractmethod
    async def classify_lead(
        self, 
        prompt: str,
        response_format: type[BaseModel]
    ) -> BaseModel:
        """Clasifica un lead y retorna structured output."""
        pass
    
    @abstractmethod
    async def detect_intent(
        self,
        message: str
    ) -> Dict[str, Any]:
        """Detecta intención del mensaje."""
        pass
    
    @abstractmethod
    async def analyze_sentiment(
        self,
        message: str
    ) -> Dict[str, Any]:
        """Analiza sentimiento del mensaje."""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> str:
        """Genera respuesta conversacional."""
        pass
```

Incluir docstrings detallados y type hints completos.
```

### Comando 4.2: OpenAI Adapter
```
@workspace Implementa app/ai/openai_adapter.py:

Clase OpenAIAdapter que:
1. Hereda de AIAdapter
2. Usa openai>=1.6.1 (AsyncOpenAI)
3. Implementa TODOS los métodos abstractos
4. Structured outputs con Pydantic
5. Retry logic con tenacity (3 intentos)
6. Timeout de 30 segundos
7. Rate limiting awareness
8. Logging estructurado de tokens usados
9. Error handling completo
10. Type hints y docstrings

Template:
```python
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog
from app.ai.base import AIAdapter
from app.core.config import settings

logger = structlog.get_logger()

class OpenAIAdapter(AIAdapter):
    """Adapter para OpenAI GPT models."""
    
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout
        )
        self._model = settings.openai_model
    
    @property
    def model_name(self) -> str:
        return self._model
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def classify_lead(self, prompt: str, response_format):
        logger.info("calling_openai", model=self._model)
        
        response = await self.client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": "Eres un experto clasificador."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result_text = response.choices[0].message.content
        logger.info("openai_response", tokens=response.usage.total_tokens)
        
        import json
        return response_format(**json.loads(result_text))
    
    # ... implementar otros métodos
```

Usa convenciones de .cursorrules
```

### Comando 4.3: Anthropic Adapter
```
@workspace Implementa app/ai/anthropic_adapter.py siguiendo el mismo patrón:

Similar a OpenAI pero usando:
- from anthropic import AsyncAnthropic
- Claude models
- Anthropic API structure

Implementar TODOS los métodos abstractos de AIAdapter.
Mantener misma estructura y logging que OpenAIAdapter.
```

---

## 5️⃣ API ENDPOINTS

### Comando 5.1: Schemas para Leads
```
@workspace Implementa app/schemas/lead.py con estos schemas:

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class LeadBase(BaseModel):
    """Base para Lead."""
    name: str = Field(..., min_length=1, max_length=255)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    company: Optional[str] = Field(None, max_length=255)

class LeadCreate(LeadBase):
    """Schema para crear Lead."""
    source: Optional[str] = None
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "email": "juan@example.com",
                "phone": "+507123456789",
                "company": "Tech Corp"
            }
        }
    )

class LeadResponse(LeadBase):
    """Schema para response de Lead."""
    id: str
    score: int
    category: Optional[str]
    status: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class LeadClassificationRequest(BaseModel):
    """Request para clasificar lead."""
    lead_id: Optional[str] = None
    message: str
    sender_metadata: dict = Field(default_factory=dict)

class LeadScore(BaseModel):
    """Resultado de clasificación."""
    score: int = Field(..., ge=0, le=100)
    category: str = Field(..., pattern="^(hot|warm|cold)$")
    reasoning: str
    recommended_action: str
```

Incluir todos los schemas necesarios para leads.
```

### Comando 5.2: Servicio LeadClassifier
```
@workspace Implementa app/services/lead_classifier.py COMPLETO:

Requisitos:
1. Clase LeadClassifier
2. Constructor con dependency injection de AI adapter
3. Método async classify(request: LeadClassificationRequest) -> LeadScore
4. Construcción de prompt optimizado
5. Llamada a IA con structured output
6. Validación de respuesta
7. Guardado en DB (LeadClassification model)
8. Logging estructurado completo
9. Error handling con custom exceptions
10. Type hints y docstrings
11. Ejemplo de uso en __main__

Usar como referencia el código COMPLETO de GAPS_PARA_CURSOR.md sección 6.

Template:
```python
from typing import Optional
import structlog
import json
from app.ai.base import AIAdapter
from app.schemas.lead import LeadClassificationRequest, LeadScore
from app.models.classification import LeadClassification
from app.db.session import AsyncSessionLocal
from datetime import datetime
import uuid

logger = structlog.get_logger()

class LeadClassifier:
    """Servicio para clasificar leads con IA."""
    
    def __init__(self, ai_adapter: AIAdapter):
        self.ai = ai_adapter
    
    async def classify(
        self,
        request: LeadClassificationRequest
    ) -> LeadScore:
        """
        Clasifica un lead usando IA.
        
        Args:
            request: Datos del lead a clasificar
            
        Returns:
            LeadScore con score 0-100 y categoría
        """
        logger.info("classifying_lead", message_length=len(request.message))
        
        # Construir prompt
        prompt = self._build_prompt(request)
        
        # Llamar IA
        result = await self.ai.classify_lead(prompt, LeadScore)
        
        # Guardar en DB
        async with AsyncSessionLocal() as session:
            classification = LeadClassification(
                id=str(uuid.uuid4()),
                lead_id=request.lead_id,
                score=result.score,
                category=result.category,
                reasoning=result.reasoning,
                recommended_action=result.recommended_action,
                ai_model=self.ai.model_name,
                classified_at=datetime.utcnow()
            )
            session.add(classification)
            await session.commit()
        
        logger.info("lead_classified", score=result.score)
        return result
    
    def _build_prompt(self, request) -> str:
        # Prompt optimizado...
        pass
```
```

### Comando 5.3: Endpoint de Clasificación
```
@workspace Implementa app/api/v1/leads.py:

Router FastAPI con estos endpoints:
1. POST /classify - Clasificar lead
2. GET /{lead_id} - Obtener lead
3. POST / - Crear lead
4. PUT /{lead_id} - Actualizar lead

Para cada endpoint:
- Type hints completos
- response_model definido
- status_code apropiado
- Dependency injection (get_db, services)
- Error handling con HTTPException
- Logging estructurado
- Docstring con ejemplo curl
- Tags para organización

Template:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.lead import (
    LeadClassificationRequest,
    LeadScore,
    LeadCreate,
    LeadResponse
)
from app.services.lead_classifier import LeadClassifier
from app.ai.openai_adapter import OpenAIAdapter
from app.db.session import get_db
import structlog

router = APIRouter(prefix="/leads", tags=["Leads"])
logger = structlog.get_logger()

def get_classifier() -> LeadClassifier:
    """Dependency para LeadClassifier."""
    return LeadClassifier(OpenAIAdapter())

@router.post("/classify", response_model=LeadScore, status_code=200)
async def classify_lead(
    request: LeadClassificationRequest,
    classifier: LeadClassifier = Depends(get_classifier),
    db: AsyncSession = Depends(get_db)
) -> LeadScore:
    """
    Clasifica un lead usando IA.
    
    Example:
        curl -X POST http://localhost:8000/api/v1/leads/classify \
          -H "Content-Type: application/json" \
          -d '{"message": "Necesito 500 laptops", "sender_metadata": {"name": "Juan"}}'
    """
    try:
        logger.info("classify_endpoint_called", lead_id=request.lead_id)
        result = await classifier.classify(request)
        return result
    except Exception as e:
        logger.error("classify_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error clasificando lead"
        )

# ... más endpoints
```
```

---

## 6️⃣ TESTING

### Comando 6.1: Setup de Testing
```
@workspace Implementa tests/conftest.py con fixtures:

```python
import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/crm_test"

# Test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
TestSessionLocal = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture para sesión de DB de prueba."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestSessionLocal() as session:
        yield session
    
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Fixture para cliente HTTP de prueba."""
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture
def mock_openai(mocker):
    """Mock de OpenAI API."""
    mock = mocker.patch("app.ai.openai_adapter.AsyncOpenAI")
    return mock
```

Incluir más fixtures según necesidad.
```

### Comando 6.2: Tests de LeadClassifier
```
@workspace Implementa tests/test_services/test_lead_classifier.py:

Tests para LeadClassifier:
1. test_classify_hot_lead - Lead con alta intención
2. test_classify_cold_lead - Lead con baja intención
3. test_classify_saves_to_db - Verifica guardado en DB
4. test_classify_with_ai_error - Manejo de errores IA
5. test_classify_retry_logic - Retry logic funciona

Cada test debe:
- Usar @pytest.mark.asyncio
- Usar fixtures de conftest
- Mock de OpenAI
- Assertions claras
- Documentación

Template:
```python
import pytest
from app.services.lead_classifier import LeadClassifier
from app.schemas.lead import LeadClassificationRequest, LeadScore
from app.ai.openai_adapter import OpenAIAdapter

@pytest.mark.asyncio
async def test_classify_hot_lead(db_session, mock_openai):
    """Test clasificación de lead caliente."""
    
    # Arrange
    mock_openai.return_value.chat.completions.create.return_value.choices[0].message.content = '''
    {
        "score": 95,
        "category": "hot",
        "reasoning": "Necesidad urgente y presupuesto claro",
        "recommended_action": "assign_to_sales_immediately"
    }
    '''
    
    classifier = LeadClassifier(OpenAIAdapter())
    request = LeadClassificationRequest(
        message="Necesito 500 laptops para mañana, presupuesto $500K",
        sender_metadata={"name": "CEO Tech Corp"}
    )
    
    # Act
    result = await classifier.classify(request)
    
    # Assert
    assert isinstance(result, LeadScore)
    assert result.score > 80
    assert result.category == "hot"
    assert "urgente" in result.reasoning.lower() or "urgency" in result.reasoning.lower()

@pytest.mark.asyncio
async def test_classify_cold_lead(db_session, mock_openai):
    """Test clasificación de lead frío."""
    # Similar structure...
    pass

# ... más tests
```
```

### Comando 6.3: Tests de API
```
@workspace Implementa tests/test_api/test_leads.py:

Tests para endpoints de Leads:
1. test_classify_endpoint_success
2. test_classify_endpoint_invalid_input
3. test_classify_endpoint_server_error
4. test_create_lead_success
5. test_get_lead_success
6. test_get_lead_not_found

Template:
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_classify_endpoint_success(client: AsyncClient, mock_openai):
    """Test endpoint de clasificación exitoso."""
    
    # Arrange
    mock_openai.return_value.chat.completions.create.return_value.choices[0].message.content = '''
    {
        "score": 85,
        "category": "hot",
        "reasoning": "Alta intención",
        "recommended_action": "contact_immediately"
    }
    '''
    
    # Act
    response = await client.post(
        "/api/v1/leads/classify",
        json={
            "message": "Necesito información sobre laptops",
            "sender_metadata": {"name": "Juan"}
        }
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["score"] <= 100
    assert data["category"] in ["hot", "warm", "cold"]

# ... más tests
```
```

---

## 7️⃣ DOCKER & DEPLOY

### Comando 7.1: Dockerfile
```
@workspace Crea Dockerfile optimizado para FastAPI:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Multi-stage build opcional para producción.
```

### Comando 7.2: Docker Compose
```
@workspace Crea docker-compose.yml completo:

Servicios:
1. fastapi - Aplicación FastAPI
2. postgres - PostgreSQL 15
3. redis - Redis 7
4. n8n - n8n workflow automation

```yaml
version: '3.8'

services:
  fastapi:
    build: .
    container_name: crm_fastapi
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:postgres@postgres:5432/crm
      - REDIS_URL=redis://redis:6379/0
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on:
      - postgres
      - redis
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  postgres:
    image: postgres:15-alpine
    container_name: crm_postgres
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=crm
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: crm_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

  n8n:
    image: n8nio/n8n:latest
    container_name: crm_n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=admin123
      - N8N_HOST=n8n
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://n8n:5678/
    volumes:
      - n8n_data:/home/node/.n8n
      - ./n8n/workflows:/workflows

volumes:
  postgres_data:
  redis_data:
  n8n_data:

networks:
  default:
    name: crm_network
```
```

---

## 8️⃣ WORKFLOWS N8N

### Comando 8.1: Workflow Webhook Inbound
```
@workspace Crea n8n/workflows/01_webhook_inbound.json:

Workflow que:
1. Recibe webhook de Meta
2. Llama a FastAPI /webhooks/inbound
3. Dispara clasificación de lead
4. Maneja errores

Estructura JSON básica de n8n workflow con nodos.
```

---

## 9️⃣ SCRIPTS UTILITIES

### Comando 9.1: Script de Setup
```
@workspace Crea scripts/setup_complete.py:

Script que:
1. Verifica .env existe
2. Instala requirements
3. Crea base de datos
4. Ejecuta migraciones Alembic
5. Verifica conexiones (DB, Redis)
6. Seed data opcional
7. Imprime resumen

Ejecutable con: python scripts/setup_complete.py
```

### Comando 9.2: Script de Testing
```
@workspace Crea scripts/test_complete.py:

Script end-to-end que:
1. Inicia servicios si no están corriendo
2. Espera a que DB esté lista
3. Ejecuta suite de pruebas
4. Prueba cada endpoint principal
5. Verifica integraciones
6. Genera reporte

Ejecutable con: python scripts/test_complete.py
```

---

## ✅ CHECKLIST DE VERIFICACIÓN

Después de ejecutar comandos, verificar:

```
@workspace Ayúdame a verificar que el proyecto esté completo:

Revisa que existan:
- [ ] Estructura de carpetas completa
- [ ] requirements.txt con versiones exactas
- [ ] .env.example con todas las variables
- [ ] .cursorrules en la raíz
- [ ] docker-compose.yml funcional
- [ ] Dockerfile optimizado
- [ ] Modelos de DB (13 archivos en app/models/)
- [ ] Schemas Pydantic (en app/schemas/)
- [ ] Servicios (22 servicios en app/services/)
- [ ] Endpoints API (en app/api/v1/)
- [ ] AI Adapters (base, openai, anthropic)
- [ ] Tests (conftest.py + tests de servicios + tests de API)
- [ ] Scripts (setup, test)
- [ ] Configuración Alembic
- [ ] Workflows n8n

Dame un resumen de lo que existe y lo que falta.
```

---

## 🚨 COMANDOS DE EMERGENCIA

### Si algo no funciona:

```
@workspace Ayúdame a debuggear:

El error es: [PEGAR ERROR AQUÍ]

Archivo involucrado: [NOMBRE DEL ARCHIVO]

Revisa:
1. Imports correctos
2. Type hints válidos
3. Async/await usado correctamente
4. Dependencias instaladas
5. Variables de entorno configuradas

Dame una solución paso a paso.
```

---

**FIN DE COMANDOS**

Estos comandos están diseñados para ser ejecutados en orden. Copia y pega directamente en Cursor AI.
