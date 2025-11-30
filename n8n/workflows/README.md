# Workflows n8n para Autonomous CRM

## Arquitectura

Los workflows de n8n **orquestan** los servicios Python implementados en FastAPI.

```
┌─────────────────────────────────────────────────────────┐
│                    n8n Workflows                         │
│  (Orquestación y flujo de trabajo visual)               │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP Requests
┌────────────────────▼────────────────────────────────────┐
│              FastAPI Services (Python)                   │
│  (Lógica de negocio e IA)                                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              PostgreSQL Database                         │
└─────────────────────────────────────────────────────────┘
```

## Workflows Disponibles

### 01_webhook_inbound.json
**Propósito:** Recibe webhooks de Meta (WhatsApp, Instagram, Messenger) y los procesa.

**Flujo:**
1. Recibe webhook de Meta
2. Llama a `/api/v1/webhooks/inbound` (FastAPI)
3. Dispara clasificación de lead

### 02_lead_classification.json
**Propósito:** Procesa un lead completo: clasifica, detecta intención, analiza sentimiento y enruta.

**Flujo:**
1. Recibe request de clasificación
2. Clasifica lead (`/api/v1/leads/classify`)
3. Si es hot lead (>80):
   - Detecta intención (`/api/v1/intents/detect`)
   - Analiza sentimiento (`/api/v1/sentiment/analyze`)
   - Enruta mensaje (`/api/v1/router/route`)
4. Retorna decisión de enrutamiento

### 03_chatbot_conversation.json
**Propósito:** Maneja conversaciones con el chatbot autónomo.

**Flujo:**
1. Recibe mensaje del usuario
2. Genera respuesta con chatbot (`/api/v1/chatbot/respond`)
3. Si necesita escalamiento, transfiere a humano
4. Retorna respuesta

## Cómo Importar Workflows en n8n

1. Accede a n8n: `http://localhost:5678`
2. Ve a **Workflows** → **Import from File**
3. Selecciona el archivo JSON del workflow
4. Configura las URLs si es necesario (deben apuntar a `http://fastapi:8000`)

## Crear Nuevos Workflows

Para crear workflows adicionales para los otros flujos (4-22), sigue este patrón:

1. **Webhook Node** - Recibe trigger
2. **HTTP Request Nodes** - Llama a servicios FastAPI
3. **IF Nodes** - Lógica condicional
4. **Function Nodes** - Transformaciones de datos
5. **Respond to Webhook** - Retorna respuesta

### Ejemplo: Workflow de Follow-up

```json
{
  "name": "Follow-up Sequence",
  "nodes": [
    {
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 1}]
        }
      }
    },
    {
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://fastapi:8000/api/v1/followups/check",
        "method": "GET"
      }
    }
  ]
}
```

## Endpoints FastAPI Disponibles

- `POST /api/v1/webhooks/inbound` - Recibe webhooks
- `POST /api/v1/leads/classify` - Clasifica leads
- `POST /api/v1/intents/detect` - Detecta intención
- `POST /api/v1/sentiment/analyze` - Analiza sentimiento
- `POST /api/v1/router/route` - Enruta mensaje
- `POST /api/v1/chatbot/respond` - Respuesta del chatbot
- `POST /api/v1/cases/evaluate-closure` - Evalúa cierre de caso

## Notas

- Los workflows de n8n son **visuales** y **fáciles de modificar** sin tocar código
- La lógica compleja está en los servicios Python
- n8n maneja la orquestación, retries, y manejo de errores
- Puedes agregar nodos de notificación (Slack, Email) fácilmente en n8n

