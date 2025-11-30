# 🚀 Quick Start - Autonomous CRM

Guía rápida para poner en marcha el sistema completo.

## Paso 1: Configuración Inicial

```bash
# 1. Clonar/copiar el proyecto (ya lo tienes)

# 2. Crear archivo .env
cp .env.example .env

# 3. Editar .env con tus credenciales
# Mínimo necesario:
# - OPENAI_API_KEY o ANTHROPIC_API_KEY (al menos una)
# - DATABASE_URL (si no usas Docker)
```

## Paso 2: Iniciar Servicios

### Opción A: Docker Compose (Recomendado)

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f fastapi
```

### Opción B: Manual

```bash
# 1. Iniciar PostgreSQL y Redis
docker-compose up -d postgres redis

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Setup completo
python scripts/setup_complete.py

# 4. Iniciar FastAPI
uvicorn app.main:app --reload
```

## Paso 3: Verificar que Funciona

```bash
# Health check
curl http://localhost:8000/health

# O ejecutar pruebas completas
python scripts/test_complete.py
```

## Paso 4: Probar Endpoints

### Clasificar un Lead

```bash
curl -X POST http://localhost:8000/api/v1/leads/classify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Necesito 500 unidades urgente para mañana",
    "sender_metadata": {
      "name": "Juan Pérez",
      "phone": "+507123456789",
      "source": "whatsapp"
    }
  }'
```

### Usar el Chatbot

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

## Paso 5: Configurar n8n (Opcional)

1. Accede a n8n: `http://localhost:5678`
2. Usuario: `admin` / Contraseña: `admin123`
3. Importa workflows desde `n8n/workflows/`
4. Configura webhooks de Meta para apuntar a n8n

## Documentación API

Una vez iniciado, accede a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Troubleshooting

### "No hay adaptador de IA disponible"
→ Configura al menos una API Key en `.env`

### "Connection refused" en base de datos
→ Verifica que PostgreSQL esté corriendo: `docker-compose ps`

### Tests fallan
→ Asegúrate de que el servidor esté corriendo: `uvicorn app.main:app --reload`

## Próximos Pasos

1. ✅ Sistema funcionando
2. 📝 Configurar credenciales de Meta (WhatsApp, Instagram)
3. 🔗 Conectar n8n con FastAPI
4. 🧪 Probar flujos completos
5. 🚀 Desplegar a producción

