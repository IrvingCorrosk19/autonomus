# Autonomous CRM - Sistema CRM Autónomo con IA Multi-Agente

Sistema CRM completo con capacidades de IA que gestiona el ciclo completo de vida del cliente desde el primer contacto hasta el cierre de venta, utilizando agentes inteligentes que operan 24/7.

## 🚀 Características

- ✅ **Omnicanal:** WhatsApp, Instagram, Facebook Messenger
- ✅ **IA Multi-Modelo:** GPT-4, Claude Sonnet (Gemini próximamente)
- ✅ **Orquestación n8n:** 22 flujos automatizados interconectados
- ✅ **Auto-Escalable:** Manejo de picos de tráfico automático
- ✅ **Predictivo:** ML para scoring, intención, cierre de ventas
- ✅ **Auditabilidad Completa:** Logs estructurados de cada acción

## 📋 Flujos Implementados (22/22)

### Flujos Core (1-5)
1. ✅ **Webhook de Entrada General** - Gateway único para mensajes multicanal
2. ✅ **Clasificación Automática de Lead** - Scoring 0-100 con IA
3. ✅ **Detección de Intención** - Identifica propósito del mensaje
4. ✅ **Análisis de Sentimiento** - Detecta emociones y urgencia
5. ✅ **Enrutamiento Inteligente** - Asigna destino óptimo

### Flujos Conversacionales (6-9)
6. ✅ **Agente Conversacional Autónomo** - Bot inteligente con contexto
7. ✅ **Escalamiento Automático** - Transfiere a humano cuando es necesario
8. ✅ **Seguimiento Inteligente** - Re-engage automático de leads
9. ✅ **Cierre Automático de Caso** - Detecta resolución y cierra tickets

### Flujos de Ventas (10-13)
10. ✅ **Nutrición Inteligente de Leads** - Secuencias de contenido dinámicas
11. ✅ **IA Closer** - Cierre de ventas y manejo de objeciones
12. ✅ **Recuperación de Carrito** - Secuencia de recuperación automática
13. ✅ **Recordatorios de Pago** - Notificaciones automáticas de facturas

### Flujos de Marketing (14-17)
14. ✅ **Generación Automática de Contenido** - Posts para redes sociales
15. ✅ **Publicación Automática en Redes** - Publica en Instagram/Facebook
16. ✅ **Programador Inteligente de Publicación** - Predice mejor momento
17. ✅ **Respuesta Automática a Comentarios** - Responde comentarios en redes

### Flujos de Datos (18-20)
18. ✅ **Deduplicación Automática** - Detecta y fusiona registros duplicados
19. ✅ **Limpieza y Normalización de Datos** - Estandariza información
20. ✅ **Enriquecimiento de Datos** - Agrega datos externos y predicciones

### Flujos Analíticos (21-22)
21. ✅ **Predicción de Cierre de Venta** - ML para probabilidad de cierre
22. ✅ **Alertas Inteligentes** - Detecta anomalías y notifica proactivamente

## 📋 Requisitos

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker y Docker Compose (opcional)

## 🛠️ Instalación Rápida

**Ver `QUICKSTART.md` para guía detallada paso a paso.**

### Setup Automático (Recomendado)

```bash
# 1. Configurar .env
cp .env.example .env
# Editar .env con tus credenciales (mínimo: OPENAI_API_KEY o ANTHROPIC_API_KEY)

# 2. Setup completo (crea DB, migraciones, datos de prueba)
python scripts/setup_complete.py

# 3. Iniciar servicios
docker-compose up -d

# 4. Probar que funciona
python scripts/test_complete.py
```

### Setup Manual

1. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus credenciales
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Iniciar con Docker Compose**
```bash
docker-compose up -d
```

4. **Ejecutar migraciones de base de datos**
```bash
alembic upgrade head
# O usar el script de setup
python scripts/setup_complete.py
```

## 🏃 Ejecución Local

### Opción 1: Docker Compose (Recomendado)

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f fastapi

# La API estará disponible en http://localhost:8000
```

### Opción 2: Desarrollo Local

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 4. Iniciar PostgreSQL y Redis (o usar Docker)
docker-compose up -d postgres redis

# 5. Inicializar base de datos
python scripts/init_db.py
# O usar Alembic:
alembic upgrade head

# 6. Ejecutar la aplicación
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

## 📚 Documentación API

Una vez iniciada la aplicación, la documentación interactiva está disponible en:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app tests/

# Tests específicos
pytest tests/test_api/
```

## 📝 Migraciones de Base de Datos

```bash
# Crear nueva migración
alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

## 📁 Estructura del Proyecto

```
autonomous-crm/
├── app/
│   ├── api/          # Endpoints FastAPI
│   ├── models/       # Modelos SQLAlchemy
│   ├── schemas/      # Schemas Pydantic
│   ├── services/    # Lógica de negocio
│   ├── ai/          # Adaptadores de IA
│   ├── integrations/# Integraciones externas
│   ├── core/        # Configuración
│   └── db/          # Base de datos
├── alembic/         # Migraciones
├── n8n/            # Workflows n8n
├── tests/          # Tests
└── scripts/        # Scripts utilitarios
```

## 🔧 Configuración

Ver `.env.example` para todas las variables de entorno necesarias.

## 📖 Documentación Completa

### 📚 Documentos Principales

- **`DOCUMENTACION_COMPLETA.md`** ⭐ - Documentación exhaustiva completa
- **`RESUMEN_EJECUTIVO.md`** ⭐ - Resumen visual y conciso
- **`QUICKSTART.md`** - Guía rápida de inicio
- **`INDICE_DOCUMENTACION.md`** - Índice de todos los documentos

### 📊 Resúmenes Específicos

- **`RESUMEN_ENDPOINTS.md`** - Lista completa de 26 endpoints
- **`RESUMEN_CONTENEDORES.md`** - Información de contenedores Docker
- **`PROYECTO_COMPLETO.md`** - Estado completo del proyecto

### 🔧 Documentación Técnica

- **`docs/ARQUITECTURA.md`** - Arquitectura n8n + FastAPI
- **`docs/ENDPOINTS.md`** - Documentación técnica de endpoints
- **`docs/TESTING.md`** - Guía completa de pruebas
- **`docs/CONTENEDORES.md`** - Detalles de contenedores

### 🔄 n8n Workflows

- **`n8n/workflows/README.md`** - Guía de workflows de n8n
- **`n8n/workflows/*.json`** - Workflows listos para importar

### 📝 Instrucciones Originales

- `Instrucciones_Autonomous_CRM_Cursor_MEJORADO.md`
- `Instrucciones_Autonomous_CRM_Cursor_PARTE_2.md`

## 🔄 n8n vs FastAPI

**IMPORTANTE:** Los flujos están implementados en **dos capas**:

1. **FastAPI Services (Python)** - Contiene la **lógica de negocio** e IA
2. **n8n Workflows** - **Orquestan** y conectan los servicios

### ¿Dónde está qué?

- ✅ **Lógica de IA y procesamiento** → `app/services/*.py` (FastAPI)
- ✅ **Orquestación y flujo visual** → `n8n/workflows/*.json` (n8n)
- ✅ **Base de datos** → `app/models/*.py` (SQLAlchemy)
- ✅ **API Endpoints** → `app/api/v1/*.py` (FastAPI)

Ver `docs/ARQUITECTURA.md` para más detalles.

## 📝 Licencia

[Tu licencia aquí]

