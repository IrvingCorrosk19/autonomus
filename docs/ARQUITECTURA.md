# Arquitectura del Sistema Autonomous CRM

## Visión General

El sistema está dividido en **dos capas principales**:

1. **n8n Workflows** - Orquestación visual y flujo de trabajo
2. **FastAPI Services** - Lógica de negocio e IA

## ¿Qué hace cada parte?

### n8n (Orquestación)
- ✅ Recibe webhooks de Meta (WhatsApp, Instagram, Messenger)
- ✅ Orquesta llamadas a servicios FastAPI
- ✅ Maneja flujos condicionales (IF/ELSE)
- ✅ Retries automáticos
- ✅ Notificaciones (Slack, Email, etc.)
- ✅ Scheduling de tareas
- ✅ Integración visual sin código

### FastAPI Services (Lógica)
- ✅ Procesa mensajes con IA
- ✅ Clasifica leads
- ✅ Analiza sentimiento
- ✅ Genera respuestas del chatbot
- ✅ Predicciones ML
- ✅ Acceso a base de datos
- ✅ Lógica de negocio compleja

## Flujo de Datos Típico

```
1. Usuario envía mensaje por WhatsApp
   ↓
2. Meta envía webhook a n8n
   ↓
3. n8n workflow recibe webhook
   ↓
4. n8n llama a FastAPI: POST /api/v1/webhooks/inbound
   ↓
5. FastAPI guarda mensaje en DB
   ↓
6. n8n llama a FastAPI: POST /api/v1/leads/classify
   ↓
7. FastAPI usa IA para clasificar lead
   ↓
8. n8n evalúa resultado (IF score > 80)
   ↓
9. n8n llama a FastAPI: POST /api/v1/intents/detect
   ↓
10. FastAPI detecta intención con IA
   ↓
11. n8n llama a FastAPI: POST /api/v1/router/route
   ↓
12. FastAPI decide destino (sales_team, chatbot, etc.)
   ↓
13. n8n envía mensaje según decisión
   ↓
14. n8n retorna respuesta al webhook
```

## Ventajas de esta Arquitectura

### Separación de Responsabilidades
- **n8n**: Orquestación y flujo visual
- **FastAPI**: Lógica compleja e IA

### Flexibilidad
- Cambios en flujo → Solo modificar n8n (sin código)
- Cambios en lógica → Modificar Python

### Escalabilidad
- n8n puede manejar múltiples workflows en paralelo
- FastAPI puede escalar horizontalmente

### Mantenibilidad
- Workflows visuales fáciles de entender
- Código Python bien estructurado y testeable

## Ejemplo Práctico

### Escenario: Lead caliente necesita atención inmediata

**En n8n:**
```
Webhook → Clasificar Lead → IF score > 80 → 
  → Notificar Slack → Asignar a Sales Team → 
  → Enviar WhatsApp al cliente
```

**En FastAPI:**
```python
# app/services/lead_classifier.py
async def classify(request):
    # Lógica compleja con IA
    result = await ai.classify_lead(...)
    return result
```

## Próximos Pasos

1. **Importar workflows** en n8n desde `n8n/workflows/`
2. **Configurar webhooks** de Meta para apuntar a n8n
3. **Ajustar URLs** en workflows si es necesario
4. **Crear workflows adicionales** para flujos 4-22 según necesidad

