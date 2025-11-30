# 🧪 CÓMO PROBAR EL SISTEMA - Guía Rápida

**Tiempo estimado:** 10 minutos

---

## ✅ PRE-REQUISITOS

Antes de probar, asegúrate de tener:

1. ✅ **Docker instalado y corriendo**
2. ✅ **Archivo `.env` configurado** (al menos con API Key de IA)
3. ✅ **Python 3.11+** instalado (si pruebas localmente)

---

## 🚀 OPCIÓN 1: Prueba Rápida (5 minutos)

### Paso 1: Configurar `.env`

```bash
# Si no tienes .env, créalo
cp .env.example .env

# Edita .env y agrega MÍNIMO:
# - OPENAI_API_KEY=sk-tu-key-aqui
# - SECRET_KEY=una-clave-segura-de-32-caracteres
# - WEBHOOK_VERIFY_TOKEN=cualquier-token
```

### Paso 2: Iniciar servicios

```bash
# Iniciar Docker Compose
docker-compose up -d

# Verificar que todo está corriendo
docker-compose ps
```

Deberías ver:
- ✅ `autonomous_crm_postgres` - UP
- ✅ `autonomous_crm_redis` - UP
- ✅ `autonomous_crm_api` - UP
- ✅ `autonomous_crm_n8n` - UP

### Paso 3: Verificar que funciona

```bash
# Health check
curl http://localhost:8000/health

# Debe responder: {"status": "healthy"}
```

### Paso 4: Probar clasificación de Lead

```bash
curl -X POST http://localhost:8000/api/v1/leads/classify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Necesito 500 laptops urgente para mañana",
    "sender_metadata": {
      "name": "Juan Pérez",
      "phone": "+507123456789",
      "source": "whatsapp"
    }
  }'
```

**Si funciona, verás:**
```json
{
  "score": 85,
  "category": "hot",
  "reasoning": "...",
  "recommended_action": "..."
}
```

---

## 🧪 OPCIÓN 2: Prueba Completa con Scripts

### Paso 1: Setup automático

```bash
# Ejecutar setup completo
python scripts/setup_complete.py
```

Este script:
- ✅ Verifica conexiones
- ✅ Inicializa base de datos
- ✅ Pobla datos de prueba
- ✅ Verifica configuración

### Paso 2: Pruebas automáticas

```bash
# Ejecutar suite completa de pruebas
python scripts/test_complete.py
```

Este script prueba:
- ✅ Health check
- ✅ Clasificación de leads
- ✅ Detección de intención
- ✅ Análisis de sentimiento
- ✅ Chatbot
- ✅ Y más endpoints

---

## 🌐 OPCIÓN 3: Probar desde el Navegador

### 1. Acceder a Swagger UI

Abre en tu navegador:
```
http://localhost:8000/docs
```

### 2. Probar endpoints interactivamente

1. Busca el endpoint `/api/v1/leads/classify`
2. Click en "Try it out"
3. Edita el JSON de ejemplo:
```json
{
  "message": "Necesito 500 laptops urgente",
  "sender_metadata": {
    "name": "Juan Pérez",
    "phone": "+507123456789"
  }
}
```
4. Click en "Execute"
5. Verás la respuesta con el score del lead

---

## 📋 CHECKLIST ANTES DE PROBAR

### Configuración Mínima:

- [ ] `.env` existe y tiene:
  - [ ] `OPENAI_API_KEY` o `ANTHROPIC_API_KEY` (al menos una)
  - [ ] `SECRET_KEY` configurado
  - [ ] `WEBHOOK_VERIFY_TOKEN` configurado
  - [ ] `DATABASE_URL` configurado (o usar Docker)

### Servicios:

- [ ] Docker corriendo
- [ ] `docker-compose up -d` ejecutado
- [ ] Todos los contenedores UP (verificar con `docker-compose ps`)

### Verificación:

- [ ] `curl http://localhost:8000/health` responde `{"status": "healthy"}`
- [ ] Puedes acceder a `http://localhost:8000/docs`

---

## 🎯 PRUEBAS ESPECÍFICAS

### 1. Probar Clasificación de Lead

```bash
curl -X POST http://localhost:8000/api/v1/leads/classify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola, busco información sobre laptops",
    "sender_metadata": {"name": "Test User"}
  }'
```

**Resultado esperado:** Score entre 0-100 y categoría (hot/warm/cold)

### 2. Probar Chatbot

```bash
curl -X POST http://localhost:8000/api/v1/chatbot/respond \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola, busco una laptop para programación",
    "context": {
      "conversation_history": []
    }
  }'
```

**Resultado esperado:** Respuesta del chatbot

### 3. Probar Detección de Intención

```bash
curl -X POST http://localhost:8000/api/v1/intents/detect \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quiero comprar 10 laptops",
    "context": {}
  }'
```

**Resultado esperado:** Intención detectada (purchase, inquiry, etc.)

### 4. Probar Análisis de Sentimiento

```bash
curl -X POST http://localhost:8000/api/v1/sentiment/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Estoy muy interesado en su producto",
    "context": {}
  }'
```

**Resultado esperado:** Sentimiento (positive/negative/neutral) y score

---

## ⚠️ PROBLEMAS COMUNES

### "No hay adaptador de IA disponible"

**Solución:**
```bash
# Verifica que tienes API Key en .env
cat .env | grep OPENAI_API_KEY

# Si no está, agrega:
OPENAI_API_KEY=sk-tu-key-aqui
```

### "Connection refused" en base de datos

**Solución:**
```bash
# Verifica que PostgreSQL está corriendo
docker-compose ps

# Si no está, inicia:
docker-compose up -d postgres
```

### "500 Internal Server Error"

**Solución:**
```bash
# Ver logs del servidor
docker-compose logs -f fastapi

# O si corres localmente:
uvicorn app.main:app --reload
# Verás el error en la consola
```

---

## ✅ VERIFICACIÓN FINAL

Si todas estas pruebas funcionan, **¡tu sistema está 100% operativo!**

- ✅ Health check responde
- ✅ Clasificación de leads funciona
- ✅ Chatbot responde
- ✅ Detección de intención funciona
- ✅ Análisis de sentimiento funciona

---

## 🎉 ¡LISTO PARA USAR!

Una vez que todas las pruebas pasen, puedes:

1. ✅ Usar el sistema en producción
2. ✅ Configurar Meta APIs para WhatsApp/Instagram
3. ✅ Conectar n8n workflows
4. ✅ Personalizar según tus necesidades

---

**¿Necesitas ayuda?** Revisa `docs/TROUBLESHOOTING.md`

