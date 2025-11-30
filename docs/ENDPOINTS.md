# 📋 Endpoints API - Mapeo con Flujos

## Resumen

**Total de Endpoints:** 8 principales + 2 auxiliares = **10 endpoints**

**Flujos con Endpoint:** 7 de 22 flujos (32%)

## Endpoints Actuales

### ✅ Endpoints Implementados

| # | Endpoint | Método | Flujo | Estado |
|---|----------|--------|-------|--------|
| 1 | `/api/v1/webhooks/inbound` | POST | **FLUJO 1** | ✅ |
| 2 | `/api/v1/webhooks/inbound/verify` | GET | **FLUJO 1** | ✅ |
| 3 | `/api/v1/leads/classify` | POST | **FLUJO 2** | ✅ |
| 4 | `/api/v1/intents/detect` | POST | **FLUJO 3** | ✅ |
| 5 | `/api/v1/sentiment/analyze` | POST | **FLUJO 4** | ✅ |
| 6 | `/api/v1/router/route` | POST | **FLUJO 5** | ✅ |
| 7 | `/api/v1/chatbot/respond` | POST | **FLUJO 6** | ✅ |
| 8 | `/api/v1/cases/evaluate-closure` | POST | **FLUJO 9** | ✅ |
| 9 | `/` | GET | - | ✅ (Root) |
| 10 | `/health` | GET | - | ✅ (Health) |

### ❌ Endpoints Faltantes

| Flujo | Servicio | Endpoint Sugerido | Tipo |
|-------|----------|-------------------|------|
| **FLUJO 7** | Escalamiento | `/api/v1/escalation/escalate` | POST |
| **FLUJO 8** | Follow-up | `/api/v1/followups/check` | GET |
| **FLUJO 10** | Nurturing | `/api/v1/nurturing/process` | POST |
| **FLUJO 11** | AI Closer | `/api/v1/sales/close` | POST |
| **FLUJO 12** | Cart Recovery | `/api/v1/carts/recover` | POST |
| **FLUJO 13** | Payment Reminder | `/api/v1/payments/remind` | POST |
| **FLUJO 14** | Content Generation | `/api/v1/content/generate` | POST |
| **FLUJO 15** | Publishing | `/api/v1/content/publish` | POST |
| **FLUJO 16** | Scheduling | `/api/v1/content/schedule` | POST |
| **FLUJO 17** | Comment Response | `/api/v1/comments/respond` | POST |
| **FLUJO 18** | Deduplication | `/api/v1/data/deduplicate` | POST |
| **FLUJO 19** | Data Cleaning | `/api/v1/data/clean` | POST |
| **FLUJO 20** | Enrichment | `/api/v1/data/enrich` | POST |
| **FLUJO 21** | Sales Prediction | `/api/v1/predictions/close-probability` | POST |
| **FLUJO 22** | Alerts | `/api/v1/alerts/check` | GET |

## Detalles por Flujo

### FLUJO 1: Webhook de Entrada ✅
- **Endpoint:** `POST /api/v1/webhooks/inbound`
- **Endpoint:** `GET /api/v1/webhooks/inbound/verify`
- **Servicio:** `MessageProcessor`
- **Función:** Recibe webhooks de Meta y los procesa

### FLUJO 2: Clasificación de Lead ✅
- **Endpoint:** `POST /api/v1/leads/classify`
- **Servicio:** `LeadClassifier`
- **Función:** Clasifica leads con IA (score 0-100)

### FLUJO 3: Detección de Intención ✅
- **Endpoint:** `POST /api/v1/intents/detect`
- **Servicio:** `IntentDetector`
- **Función:** Detecta intención del mensaje

### FLUJO 4: Análisis de Sentimiento ✅
- **Endpoint:** `POST /api/v1/sentiment/analyze`
- **Servicio:** `SentimentAnalyzer`
- **Función:** Analiza sentimiento emocional

### FLUJO 5: Enrutamiento Inteligente ✅
- **Endpoint:** `POST /api/v1/router/route`
- **Servicio:** `IntelligentRouter`
- **Función:** Decide destino del mensaje

### FLUJO 6: Chatbot Autónomo ✅
- **Endpoint:** `POST /api/v1/chatbot/respond`
- **Servicio:** `AutonomousChatbot`
- **Función:** Genera respuesta conversacional

### FLUJO 7: Escalamiento ❌
- **Servicio:** `EscalationService`
- **Endpoint faltante:** `/api/v1/escalation/escalate`

### FLUJO 8: Seguimiento ❌
- **Servicio:** `FollowUpService`
- **Endpoint faltante:** `/api/v1/followups/check`

### FLUJO 9: Cierre de Caso ✅
- **Endpoint:** `POST /api/v1/cases/evaluate-closure`
- **Servicio:** `CaseClosureService`
- **Función:** Evalúa cierre automático

### FLUJOS 10-22 ❌
- Todos tienen servicios implementados
- Faltan endpoints API para exponerlos

## Nota Importante

**Los servicios están implementados**, pero muchos flujos se ejecutan mediante:
1. **Jobs programados** (scheduler.py) - Para tareas periódicas
2. **Llamadas internas** desde otros servicios
3. **n8n workflows** - Para orquestación

No todos los flujos necesitan endpoints HTTP públicos, pero es útil tenerlos para:
- Testing
- Integración manual
- Monitoreo
- Debugging

