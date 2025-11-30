# Guía de Testing - Autonomous CRM

## Pruebas Rápidas

### 1. Setup Inicial

```bash
# 1. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales

# 2. Iniciar servicios
docker-compose up -d

# 3. Setup completo
python scripts/setup_complete.py
```

### 2. Pruebas Automatizadas

```bash
# Ejecutar todas las pruebas
python scripts/test_complete.py

# O en Windows
scripts\run_tests.bat
```

### 3. Pruebas Manuales

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Clasificar Lead
```bash
curl -X POST http://localhost:8000/api/v1/leads/classify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Necesito 500 unidades urgente",
    "sender_metadata": {
      "name": "Juan Pérez",
      "phone": "+507123456789"
    }
  }'
```

#### Detectar Intención
```bash
curl -X POST http://localhost:8000/api/v1/intents/detect \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quiero comprar 10 laptops"
  }'
```

#### Analizar Sentimiento
```bash
curl -X POST http://localhost:8000/api/v1/sentiment/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "message": "El producto llegó defectuoso"
  }'
```

#### Chatbot
```bash
curl -X POST http://localhost:8000/api/v1/chatbot/respond \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hola, busco una laptop",
    "context": {
      "conversation_history": []
    }
  }'
```

## Pruebas con Postman

1. Importa la colección desde `docs/postman_collection.json` (crear)
2. Configura la variable `base_url` = `http://localhost:8000`
3. Ejecuta las requests

## Pruebas de Base de Datos

```bash
# Poblar con datos de prueba
python scripts/seed_db.py

# Verificar datos
python -c "
from app.db.session import SessionLocal
from app.models.lead import Lead
db = SessionLocal()
leads = db.query(Lead).all()
print(f'Leads: {len(leads)}')
"
```

## Pruebas de n8n

1. Accede a n8n: `http://localhost:5678`
2. Importa workflows desde `n8n/workflows/`
3. Activa los workflows
4. Prueba enviando webhooks de prueba

## Troubleshooting

### Error: "No hay adaptador de IA disponible"
- Verifica que tengas al menos una API Key configurada en `.env`
- OpenAI: `OPENAI_API_KEY=sk-...`
- Anthropic: `ANTHROPIC_API_KEY=sk-ant-...`

### Error: "Connection refused" en base de datos
- Verifica que PostgreSQL esté corriendo: `docker-compose ps`
- Inicia PostgreSQL: `docker-compose up -d postgres`

### Error: "Module not found"
- Instala dependencias: `pip install -r requirements.txt`
- Verifica que estés en el entorno virtual correcto

### Tests fallan con timeout
- Aumenta el timeout en `scripts/test_complete.py`
- Verifica que las APIs de IA estén respondiendo

