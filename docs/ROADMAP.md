# 🗺️ ROADMAP DE IMPLEMENTACIÓN - Autonomous CRM

**Versión:** 1.0  
**Tiempo Estimado Total:** 12-16 horas  
**Nivel:** Intermedio-Avanzado

---

## 📊 VISIÓN GENERAL

### Fases del Proyecto

```
FASE 1: Setup Base (2h)         ████████░░░░░░░░░░░░  20%
FASE 2: Core & DB (3h)          ████████████░░░░░░░░  40%
FASE 3: IA & Servicios (4h)     ████████████████░░░░  60%
FASE 4: API Endpoints (2h)      ████████████████████  80%
FASE 5: Testing & Deploy (2h)   ████████████████████ 100%
```

---

## 🎯 FASE 1: SETUP BASE (2 horas)

**Objetivo:** Proyecto inicializado con estructura completa

### ✅ Paso 1.1: Crear Estructura (15 min)

**Comando Cursor:**
```
@workspace Crea la estructura completa del proyecto según CURSOR_PROMPTS.md comando 1.1
```

**Verificación:**
```bash
# Verificar carpetas creadas
ls -la autonomous-crm/app/
ls -la autonomous-crm/tests/

# Debe mostrar:
# app/api/, app/models/, app/services/, app/ai/, etc.
```

**✓ Completado cuando:**
- [ ] Todas las carpetas existen
- [ ] Archivos `__init__.py` en cada módulo
- [ ] `.gitignore` creado

---

### ✅ Paso 1.2: Requirements & Dependencias (20 min)

**Comando Cursor:**
```
@workspace Crea requirements.txt según CURSOR_PROMPTS.md comando 1.2
```

**Instalación:**
```bash
cd autonomous-crm
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Verificación:**
```bash
pip list | grep fastapi
pip list | grep sqlalchemy
pip list | grep openai
```

**✓ Completado cuando:**
- [ ] requirements.txt existe con versiones exactas
- [ ] Todas las dependencias instaladas sin errores
- [ ] Virtual environment activado

---

### ✅ Paso 1.3: Configuración Inicial (30 min)

**Comando Cursor:**
```
@workspace Crea .env.example según CURSOR_PROMPTS.md comando 1.3
```

**Setup manual:**
```bash
# Copiar .env.example a .env
cp .env.example .env

# Editar .env con tus valores reales:
nano .env  # o tu editor preferido
```

**Variables CRÍTICAS a configurar:**
```bash
# Mínimo necesario para empezar:
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/crm
OPENAI_API_KEY=sk-tu-key-aqui
SECRET_KEY=genera-una-key-segura-de-32-chars
```

**✓ Completado cuando:**
- [ ] .env.example existe
- [ ] .env creado con valores reales
- [ ] OPENAI_API_KEY configurado
- [ ] DATABASE_URL configurado

---

### ✅ Paso 1.4: Docker Setup (45 min)

**Comando Cursor:**
```
@workspace Crea Dockerfile y docker-compose.yml según CURSOR_PROMPTS.md comandos 7.1 y 7.2
```

**Iniciar contenedores:**
```bash
# Verificar que Docker esté corriendo
docker --version

# Iniciar solo DB y Redis primero
docker-compose up -d postgres redis

# Verificar que estén corriendo
docker ps

# Debe mostrar:
# crm_postgres    Up
# crm_redis       Up
```

**Verificar conexión a DB:**
```bash
# Conectarse a PostgreSQL
docker exec -it crm_postgres psql -U postgres

# Dentro de psql:
\l              # Listar databases
\q              # Salir
```

**✓ Completado cuando:**
- [ ] Dockerfile existe
- [ ] docker-compose.yml existe
- [ ] PostgreSQL corriendo (puerto 5432)
- [ ] Redis corriendo (puerto 6379)
- [ ] Puedes conectarte a la DB

---

### 🎉 CHECKPOINT FASE 1

**Verificación completa:**
```bash
# Estructura
ls -la autonomous-crm/

# Dependencies
pip list | wc -l  # Debe ser ~50+ paquetes

# Docker
docker ps  # 2 contenedores UP

# Config
cat .env | grep DATABASE_URL
```

**Si TODO está ✅, continúa a FASE 2**

---

## 🔧 FASE 2: CORE & DATABASE (3 horas)

**Objetivo:** Core funcional y modelos de DB creados

### ✅ Paso 2.1: Core Config (30 min)

**Comando Cursor:**
```
@workspace Implementa app/core/config.py según CURSOR_PROMPTS.md comando 2.1
```

**Probar configuración:**
```python
# Test rápido
python -c "from app.core.config import settings; print(settings.database_url)"
```

**✓ Completado cuando:**
- [ ] app/core/config.py existe
- [ ] Settings carga desde .env
- [ ] No hay errores de import

---

### ✅ Paso 2.2: Logging Setup (20 min)

**Comando Cursor:**
```
@workspace Implementa app/core/logging.py según CURSOR_PROMPTS.md comando 2.2
```

**Probar logging:**
```python
# Test en terminal
python -c "
from app.core.logging import setup_logging
import structlog
setup_logging()
logger = structlog.get_logger()
logger.info('test', key='value')
"
```

**✓ Completado cuando:**
- [ ] app/core/logging.py existe
- [ ] Logger imprime JSON
- [ ] No hay errores

---

### ✅ Paso 2.3: Security Utils (20 min)

**Comando Cursor:**
```
@workspace Implementa app/core/security.py según CURSOR_PROMPTS.md comando 2.3
```

**Probar hashing:**
```python
python -c "
from app.core.security import hash_password, verify_password
hashed = hash_password('test123')
print('Hash:', hashed)
print('Verify:', verify_password('test123', hashed))
"
```

**✓ Completado cuando:**
- [ ] app/core/security.py existe
- [ ] Hashing funciona
- [ ] JWT funciona (opcional por ahora)

---

### ✅ Paso 2.4: Database Setup (30 min)

**Comando Cursor:**
```
@workspace Implementa app/db/base.py y app/db/session.py según CURSOR_PROMPTS.md comando 3.1
```

**Probar conexión:**
```python
# tests/test_db_connection.py
import asyncio
from app.db.session import AsyncSessionLocal

async def test_connection():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT 1")
        print("DB Connection OK:", result.scalar())

asyncio.run(test_connection())
```

**✓ Completado cuando:**
- [ ] app/db/base.py existe
- [ ] app/db/session.py existe
- [ ] Conexión a DB funciona

---

### ✅ Paso 2.5: Modelos de DB (60 min)

**Comando Cursor (en orden):**
```
# Primero el modelo más importante
@workspace Implementa app/models/lead.py según CURSOR_PROMPTS.md comando 3.2

# Luego el resto
@workspace Implementa TODOS los modelos en app/models/ según CURSOR_PROMPTS.md comando 3.3
```

**Lista de modelos a crear:**
1. ✅ lead.py
2. ✅ customer.py
3. ✅ conversation.py
4. ✅ message.py
5. ✅ classification.py
6. ✅ intent.py
7. ✅ sentiment.py
8. ✅ case.py
9. ✅ cart.py
10. ✅ purchase.py
11. ✅ invoice.py
12. ✅ content.py
13. ✅ alert.py

**Verificar modelos:**
```python
python -c "
from app.models.lead import Lead
from app.models.customer import Customer
print('Modelos importados OK')
"
```

**✓ Completado cuando:**
- [ ] 13 archivos de modelos existen
- [ ] Todos se importan sin errores
- [ ] Relationships definidas

---

### ✅ Paso 2.6: Alembic Migrations (20 min)

**Comando Cursor:**
```
@workspace Configura Alembic según CURSOR_PROMPTS.md comando 3.4
```

**Crear migración inicial:**
```bash
# Inicializar Alembic (si no existe)
alembic init alembic

# Crear migración automática
alembic revision --autogenerate -m "Initial migration"

# Revisar la migración generada
cat alembic/versions/[archivo generado]

# Aplicar migración
alembic upgrade head
```

**Verificar en DB:**
```bash
docker exec -it crm_postgres psql -U postgres -d crm -c "\dt"

# Debe mostrar:
# leads, customers, conversations, messages, etc.
```

**✓ Completado cuando:**
- [ ] Alembic configurado
- [ ] Migración inicial creada
- [ ] Migración aplicada exitosamente
- [ ] Tablas creadas en PostgreSQL

---

### 🎉 CHECKPOINT FASE 2

**Verificación:**
```python
# test_phase_2.py
import asyncio
from app.db.session import AsyncSessionLocal
from app.models.lead import Lead

async def test():
    async with AsyncSessionLocal() as session:
        # Crear lead de prueba
        lead = Lead(name="Test Lead", email="test@example.com")
        session.add(lead)
        await session.commit()
        
        # Verificar que se creó
        result = await session.execute("SELECT COUNT(*) FROM leads")
        count = result.scalar()
        print(f"Leads en DB: {count}")

asyncio.run(test())
```

**Si imprime "Leads en DB: 1", continúa a FASE 3**

---

## 🤖 FASE 3: IA & SERVICIOS (4 horas)

**Objetivo:** Servicios de IA y lógica de negocio funcionando

### ✅ Paso 3.1: AI Base Adapter (20 min)

**Comando Cursor:**
```
@workspace Implementa app/ai/base.py según CURSOR_PROMPTS.md comando 4.1
```

**✓ Completado cuando:**
- [ ] app/ai/base.py existe
- [ ] Clase abstracta AIAdapter definida
- [ ] Métodos abstractos documentados

---

### ✅ Paso 3.2: OpenAI Adapter (45 min)

**Comando Cursor:**
```
@workspace Implementa app/ai/openai_adapter.py según CURSOR_PROMPTS.md comando 4.2
```

**Probar OpenAI:**
```python
# test_openai.py
import asyncio
from app.ai.openai_adapter import OpenAIAdapter

async def test():
    adapter = OpenAIAdapter()
    response = await adapter.chat(
        messages=[{"role": "user", "content": "Di 'hola'"}]
    )
    print("OpenAI responde:", response)

asyncio.run(test())
```

**✓ Completado cuando:**
- [ ] OpenAIAdapter implementado
- [ ] Prueba con API real funciona
- [ ] Retry logic implementado

---

### ✅ Paso 3.3: Anthropic Adapter (30 min)

**Comando Cursor:**
```
@workspace Implementa app/ai/anthropic_adapter.py según CURSOR_PROMPTS.md comando 4.3
```

**Opcional si no tienes API key de Claude - puedes saltarlo**

---

### ✅ Paso 3.4: Schemas Pydantic (30 min)

**Comando Cursor:**
```
@workspace Implementa app/schemas/lead.py según CURSOR_PROMPTS.md comando 5.1
```

**Schemas a crear:**
- LeadBase
- LeadCreate
- LeadResponse
- LeadUpdate
- LeadClassificationRequest
- LeadScore

**Probar schemas:**
```python
from app.schemas.lead import LeadCreate, LeadScore

# Test validación
lead = LeadCreate(name="Juan", email="juan@test.com")
print(lead.model_dump())

# Test LeadScore
score = LeadScore(
    score=85,
    category="hot",
    reasoning="Alta intención",
    recommended_action="contact_now"
)
print(score)
```

**✓ Completado cuando:**
- [ ] Todos los schemas existen
- [ ] Validación funciona
- [ ] Ejemplos en schema_extra

---

### ✅ Paso 3.5: Servicio LeadClassifier (60 min) - CRÍTICO

**Comando Cursor:**
```
@workspace Implementa app/services/lead_classifier.py COMPLETO según CURSOR_PROMPTS.md comando 5.2
```

**Este es el servicio más importante. Debe incluir:**
- Integración con OpenAI
- Structured outputs con Pydantic
- Guardado en DB
- Logging completo
- Error handling

**Probar servicio:**
```python
# test_lead_classifier.py
import asyncio
from app.services.lead_classifier import LeadClassifier
from app.ai.openai_adapter import OpenAIAdapter
from app.schemas.lead import LeadClassificationRequest

async def test():
    classifier = LeadClassifier(OpenAIAdapter())
    
    request = LeadClassificationRequest(
        message="Necesito 500 laptops urgente para mi empresa",
        sender_metadata={"name": "CEO Tech Corp"}
    )
    
    result = await classifier.classify(request)
    
    print(f"Score: {result.score}")
    print(f"Category: {result.category}")
    print(f"Reasoning: {result.reasoning}")

asyncio.run(test())
```

**✓ Completado cuando:**
- [ ] LeadClassifier funciona end-to-end
- [ ] IA responde correctamente
- [ ] Se guarda en DB
- [ ] Logs son claros

---

### ✅ Paso 3.6: Más Servicios (90 min)

**Implementar en este orden:**

1. **IntentDetector** (30 min)
```
@workspace Implementa app/services/intent_detector.py similar a LeadClassifier
```

2. **SentimentAnalyzer** (30 min)
```
@workspace Implementa app/services/sentiment_analyzer.py similar a LeadClassifier
```

3. **IntelligentRouter** (30 min)
```
@workspace Implementa app/services/router.py con lógica de enrutamiento
```

**Puedes paralelizar con Cursor:**
```
@workspace Implementa estos 3 servicios en paralelo:
1. app/services/intent_detector.py
2. app/services/sentiment_analyzer.py  
3. app/services/router.py

Sigue el mismo patrón que LeadClassifier.
```

**✓ Completado cuando:**
- [ ] 3 servicios implementados
- [ ] Cada uno tiene su schema
- [ ] Pruebas básicas pasan

---

### 🎉 CHECKPOINT FASE 3

**Test de integración:**
```python
# test_phase_3_integration.py
import asyncio
from app.services.lead_classifier import LeadClassifier
from app.services.intent_detector import IntentDetector
from app.services.sentiment_analyzer import SentimentAnalyzer
from app.ai.openai_adapter import OpenAIAdapter

async def test():
    ai = OpenAIAdapter()
    
    # Test clasificación
    classifier = LeadClassifier(ai)
    score = await classifier.classify(...)
    print("✅ Clasificación OK")
    
    # Test intención
    intent_detector = IntentDetector(ai)
    intent = await intent_detector.detect(...)
    print("✅ Intención OK")
    
    # Test sentimiento
    sentiment_analyzer = SentimentAnalyzer(ai)
    sentiment = await sentiment_analyzer.analyze(...)
    print("✅ Sentimiento OK")
    
    print("\n🎉 FASE 3 COMPLETA")

asyncio.run(test())
```

---

## 🌐 FASE 4: API ENDPOINTS (2 horas)

**Objetivo:** API REST funcional y documentada

### ✅ Paso 4.1: FastAPI Main App (20 min)

**Comando Cursor:**
```
@workspace Crea app/main.py con:
- FastAPI app instance
- CORS middleware
- Logging middleware
- Include routers de api/v1
- Health check endpoint
- Startup/shutdown events
```

**Template básico:**
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1 import leads

# Setup logging
setup_logging()

# Create app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include routers
app.include_router(leads.router, prefix="/api/v1", tags=["Leads"])

@app.get("/health")
async def health():
    return {"status": "ok"}
```

**Probar:**
```bash
uvicorn app.main:app --reload

# En otro terminal:
curl http://localhost:8000/health
# Debe retornar: {"status":"ok"}

# Documentación automática:
# http://localhost:8000/docs
```

**✓ Completado cuando:**
- [ ] App inicia sin errores
- [ ] /health responde
- [ ] /docs muestra Swagger UI

---

### ✅ Paso 4.2: Endpoint de Clasificación (40 min)

**Comando Cursor:**
```
@workspace Implementa app/api/v1/leads.py según CURSOR_PROMPTS.md comando 5.3
```

**Endpoints a implementar:**
- POST /api/v1/leads/classify
- POST /api/v1/leads
- GET /api/v1/leads/{lead_id}
- PUT /api/v1/leads/{lead_id}

**Probar endpoint:**
```bash
# Clasificar lead
curl -X POST http://localhost:8000/api/v1/leads/classify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Necesito 500 laptops urgente",
    "sender_metadata": {"name": "Juan Pérez"}
  }'

# Debe retornar:
# {
#   "score": 85,
#   "category": "hot",
#   "reasoning": "...",
#   "recommended_action": "..."
# }
```

**✓ Completado cuando:**
- [ ] POST /classify funciona
- [ ] Responde con LeadScore válido
- [ ] Se guarda en DB
- [ ] Documentado en /docs

---

### ✅ Paso 4.3: Más Endpoints (60 min)

**Implementar en orden:**

1. **Intents Endpoint** (20 min)
```
@workspace Implementa app/api/v1/intents.py con:
- POST /api/v1/intents/detect
```

2. **Sentiment Endpoint** (20 min)
```
@workspace Implementa app/api/v1/sentiment.py con:
- POST /api/v1/sentiment/analyze
```

3. **Webhooks Endpoint** (20 min)
```
@workspace Implementa app/api/v1/webhooks.py con:
- POST /api/v1/webhooks/inbound
- GET /api/v1/webhooks/inbound/verify
```

**Incluir todos en main.py:**
```python
# app/main.py
from app.api.v1 import leads, intents, sentiment, webhooks

app.include_router(leads.router, prefix="/api/v1")
app.include_router(intents.router, prefix="/api/v1")
app.include_router(sentiment.router, prefix="/api/v1")
app.include_router(webhooks.router, prefix="/api/v1")
```

**✓ Completado cuando:**
- [ ] 4 routers funcionando
- [ ] Todos documentados en /docs
- [ ] Tests manuales pasan

---

### 🎉 CHECKPOINT FASE 4

**Test completo de API:**
```bash
# Script de prueba
python scripts/test_api.py

# O manual:
# 1. Clasificar lead
curl -X POST localhost:8000/api/v1/leads/classify -d '{"message":"test"}'

# 2. Detectar intención
curl -X POST localhost:8000/api/v1/intents/detect -d '{"message":"test"}'

# 3. Analizar sentimiento
curl -X POST localhost:8000/api/v1/sentiment/analyze -d '{"message":"test"}'

# Si todos responden correctamente → ✅ FASE 4 COMPLETA
```

---

## 🧪 FASE 5: TESTING & DEPLOY (2 horas)

**Objetivo:** Tests automatizados y deployment funcional

### ✅ Paso 5.1: Setup de Testing (30 min)

**Comando Cursor:**
```
@workspace Implementa tests/conftest.py según CURSOR_PROMPTS.md comando 6.1
```

**Configurar pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
asyncio_mode = auto
```

**✓ Completado cuando:**
- [ ] conftest.py existe
- [ ] Fixtures funcionan
- [ ] pytest encuentra tests

---

### ✅ Paso 5.2: Tests de Servicios (40 min)

**Comando Cursor:**
```
@workspace Implementa tests/test_services/test_lead_classifier.py según CURSOR_PROMPTS.md comando 6.2
```

**Ejecutar tests:**
```bash
pytest tests/test_services/test_lead_classifier.py -v

# Debe pasar todos los tests
```

**Implementar más tests:**
```
@workspace Crea tests para:
- tests/test_services/test_intent_detector.py
- tests/test_services/test_sentiment_analyzer.py
```

**✓ Completado cuando:**
- [ ] Tests de servicios pasan
- [ ] Coverage > 70%

---

### ✅ Paso 5.3: Tests de API (30 min)

**Comando Cursor:**
```
@workspace Implementa tests/test_api/test_leads.py según CURSOR_PROMPTS.md comando 6.3
```

**Ejecutar:**
```bash
pytest tests/test_api/ -v
```

**✓ Completado cuando:**
- [ ] Tests de API pasan
- [ ] Mock de IA funciona

---

### ✅ Paso 5.4: Docker Build Completo (20 min)

**Build y deploy:**
```bash
# Build imagen
docker-compose build

# Iniciar TODO
docker-compose up -d

# Verificar
docker ps
# Debe mostrar: fastapi, postgres, redis, n8n

# Logs
docker-compose logs -f fastapi

# Probar API en Docker
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

**✓ Completado cuando:**
- [ ] 4 contenedores corriendo
- [ ] API accesible
- [ ] n8n accesible en :5678

---

### 🎉 CHECKPOINT FINAL

**Test end-to-end completo:**
```bash
# Ejecutar script de prueba completa
python scripts/test_complete.py

# Debe ejecutar:
# 1. ✅ Verificar DB
# 2. ✅ Verificar Redis  
# 3. ✅ Probar clasificación
# 4. ✅ Probar intención
# 5. ✅ Probar sentimiento
# 6. ✅ Crear lead
# 7. ✅ Obtener lead
# 8. ✅ Actualizar lead

# Si TODO pasa → 🎉 PROYECTO COMPLETO
```

---

## 🎓 POST-IMPLEMENTACIÓN

### Optimizaciones Opcionales

1. **Más Servicios** (Flujos 6-22)
```
- Chatbot conversacional
- Follow-ups automáticos
- Cart recovery
- Content generation
- etc.
```

2. **Integración Meta APIs**
```
- WhatsApp Business API
- Instagram Graph API
- Messenger Platform
```

3. **Workflows n8n**
```
- Importar workflows
- Conectar con FastAPI
- Automatizar flujos
```

4. **Monitoring**
```
- Prometheus metrics
- Grafana dashboards
- Sentry error tracking
```

5. **Production Deploy**
```
- AWS/GCP/Azure
- CI/CD pipeline
- Environment configs
```

---

## 📊 MÉTRICAS DE ÉXITO

Al finalizar, deberías tener:

- ✅ **Estructura:** 50+ archivos Python
- ✅ **Modelos:** 13 modelos de DB
- ✅ **Servicios:** 3+ servicios funcionando
- ✅ **Endpoints:** 10+ endpoints API
- ✅ **Tests:** 20+ tests pasando
- ✅ **Docker:** 4 contenedores UP
- ✅ **Coverage:** >70%
- ✅ **Documentación:** Swagger completo

---

## 🆘 TROUBLESHOOTING

### Problema: Imports no funcionan
```bash
# Solución: PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### Problema: DB connection error
```bash
# Verificar DB corriendo
docker ps | grep postgres

# Verificar URL correcta
echo $DATABASE_URL
```

### Problema: OpenAI API error
```bash
# Verificar API key
echo $OPENAI_API_KEY

# Test directo
python -c "
from openai import OpenAI
client = OpenAI()
print('API Key válida')
"
```

### Problema: Tests fallan
```bash
# Correr con verbose
pytest -vvs tests/

# Ver coverage
pytest --cov=app tests/
```

---

## ✅ LISTA DE VERIFICACIÓN FINAL

Marca cuando completes cada fase:

- [ ] FASE 1: Setup Base (estructura, deps, docker)
- [ ] FASE 2: Core & DB (config, modelos, migrations)
- [ ] FASE 3: IA & Servicios (adapters, servicios core)
- [ ] FASE 4: API Endpoints (FastAPI, routers)
- [ ] FASE 5: Testing & Deploy (tests, docker completo)

---

**🎉 ¡FELICITACIONES!**

Si completaste todas las fases, tienes un **CRM Autónomo con IA completamente funcional**.

---

**Tiempo Real Estimado:**
- Desarrollador experimentado: 12-14 horas
- Desarrollador intermedio: 16-20 horas
- Con ayuda de Cursor AI: -30% tiempo

**Próximo paso:** Comenzar con FASE 1, Paso 1.1
