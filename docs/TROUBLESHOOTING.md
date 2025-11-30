# 🔧 TROUBLESHOOTING - Autonomous CRM

Guía de solución de problemas comunes.

---

## 🚨 Problemas con Cursor AI

### Problema: "Cursor no genera código"

**Solución:**
1. Verifica que `.cursorrules` existe en la raíz del proyecto
2. Usa comandos específicos con `@workspace`
3. Menciona archivos específicos a crear
4. Da contexto de otros archivos relacionados

**Ejemplo de comando correcto:**
```
@workspace Siguiendo .cursorrules, crea app/core/config.py completo con todas las variables de .env.example
```

---

### Problema: "Código generado tiene errores"

**Solución:**
1. Especifica versiones exactas en requirements.txt
2. Da ejemplos completos en el prompt
3. Pide tests junto con el código
4. Verifica type hints

**Ejemplo:**
```
@workspace El código en app/services/lead_classifier.py tiene este error: [error].
Corrigelo siguiendo .cursorrules y docs/CURSOR_PROMPTS.md
```

---

### Problema: "Cursor mezcla versiones de SQLAlchemy"

**Solución:**
En `.cursorrules` ya está especificado:
- Usar SOLO SQLAlchemy 2.0+ con:
  - `from sqlalchemy.orm import Mapped, mapped_column`
  - NO usar `Column`, `String`, `Integer` antiguos
  - Usar declarative_base nueva sintaxis

**Si persiste:**
```
@workspace Revisa todos los modelos en app/models/ y asegúrate que usen SOLO SQLAlchemy 2.0 sintaxis:
- Mapped[str] en lugar de Column(String)
- mapped_column() en lugar de Column()
```

---

## 🐛 Problemas con Tests

### Problema: "Tests no corren"

**Solución:**
1. Verifica pytest-asyncio instalado: `pip install pytest-asyncio`
2. Marca tests con `@pytest.mark.asyncio`
3. Usa `AsyncClient` de httpx para test de API
4. Mock de servicios externos

**Ejemplo de test correcto:**
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_classify_lead(client: AsyncClient, mock_openai):
    response = await client.post(
        "/api/v1/leads/classify",
        json={"message": "Test", "sender_metadata": {}}
    )
    assert response.status_code == 200
```

---

## 🐳 Problemas con Docker

### Problema: "Docker no inicia"

**Solución:**
1. Verifica puertos no ocupados (5432, 6379, 8000, 5678)
2. Limpia volumes: `docker-compose down -v`
3. Reconstruye: `docker-compose up --build`
4. Verifica logs: `docker-compose logs`

**Comandos útiles:**
```bash
# Ver qué está usando los puertos
netstat -ano | findstr :5432  # Windows
lsof -i :5432                 # Linux/Mac

# Limpiar todo y empezar de nuevo
docker-compose down -v
docker-compose up --build
```

---

### Problema: "PostgreSQL no conecta"

**Solución:**
1. Verifica que el contenedor esté corriendo: `docker ps`
2. Verifica DATABASE_URL en `.env`
3. Prueba conexión: `docker exec -it autonomous_crm_postgres psql -U user -d autonomous_crm`
4. Verifica que la DB existe: `\l` dentro de psql

---

## 🔌 Problemas con Base de Datos

### Problema: "Alembic no encuentra modelos"

**Solución:**
1. Verifica que `app/models/__init__.py` importa todos los modelos
2. Verifica `alembic/env.py` tiene la importación correcta
3. Asegúrate que Base está importado correctamente

**Verificar:**
```python
# app/models/__init__.py debe tener:
from app.models.lead import Lead
from app.models.customer import Customer
# ... todos los modelos
```

---

### Problema: "Error de migración"

**Solución:**
```bash
# Ver estado de migraciones
alembic current

# Ver historial
alembic history

# Si hay conflicto, revisa la migración
alembic upgrade head --sql  # Ver SQL sin ejecutar

# Si necesitas resetear (CUIDADO: borra datos)
alembic downgrade base
alembic upgrade head
```

---

## 🤖 Problemas con IA

### Problema: "OpenAI API no responde"

**Solución:**
1. Verifica API key: `echo $OPENAI_API_KEY`
2. Verifica que la key sea válida
3. Revisa rate limits
4. Verifica timeout configurado

**Debug:**
```python
# En app/ai/openai_adapter.py, agrega logging:
logger.debug("openai_request", model=model, prompt_length=len(prompt))
```

---

### Problema: "Anthropic falla pero OpenAI funciona"

**Solución:**
1. Verifica que ANTHROPIC_API_KEY esté configurado
2. Verifica formato de la key (debe empezar con `sk-ant-`)
3. Revisa que el modelo sea correcto: `claude-sonnet-4-20250514`

---

## 🔐 Problemas con Variables de Entorno

### Problema: "Settings no carga variables"

**Solución:**
1. Verifica que `.env` existe (no solo `.env.example`)
2. Verifica que `python-dotenv` está instalado
3. Verifica que `pydantic-settings` está en requirements.txt
4. Reinicia el servidor después de cambiar `.env`

**Verificar:**
```python
# En Python:
from app.core.config import settings
print(settings.DATABASE_URL)  # Debe mostrar la URL
```

---

## 📡 Problemas con API

### Problema: "Endpoint retorna 500"

**Solución:**
1. Revisa logs del servidor
2. Verifica que la DB esté conectada
3. Verifica que las dependencias estén instaladas
4. Revisa el stack trace completo

**Debug:**
```bash
# Ver logs detallados
uvicorn app.main:app --reload --log-level debug

# O en Docker
docker-compose logs -f fastapi
```

---

### Problema: "CORS error"

**Solución:**
1. Verifica `ALLOWED_ORIGINS` en `.env`
2. Agrega tu dominio a la lista
3. Reinicia el servidor

**Ejemplo:**
```bash
ALLOWED_ORIGINS=http://localhost:3000,https://mi-dominio.com
```

---

## 🧪 Problemas con Testing

### Problema: "Tests async fallan"

**Solución:**
1. Asegúrate de usar `@pytest.mark.asyncio`
2. Usa `AsyncClient` de httpx
3. Usa `AsyncSession` para DB tests

**Ejemplo correcto:**
```python
@pytest.mark.asyncio
async def test_something():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/endpoint")
```

---

## 🔄 Problemas con n8n

### Problema: "n8n no conecta con FastAPI"

**Solución:**
1. Verifica que FastAPI esté corriendo
2. Verifica la URL en n8n: debe ser `http://fastapi:8000` (desde Docker) o `http://localhost:8000` (desde host)
3. Verifica que el webhook esté configurado correctamente

---

## 📝 Problemas Comunes de Código

### Problema: "Type hints incorrectos"

**Solución:**
Siempre usar type hints completos:
```python
# ✅ Correcto
async def classify(self, request: LeadClassificationRequest) -> LeadScore:

# ❌ Incorrecto
async def classify(self, request):
```

---

### Problema: "SQLAlchemy 1.x sintaxis"

**Solución:**
Usar SOLO SQLAlchemy 2.0:
```python
# ✅ Correcto (2.0)
id: Mapped[str] = mapped_column(String, primary_key=True)

# ❌ Incorrecto (1.x)
id = Column(String, primary_key=True)
```

---

## 🆘 Si Nada Funciona

### Reset Completo

```bash
# 1. Detener todo
docker-compose down -v

# 2. Limpiar Python
rm -rf venv/
rm -rf __pycache__/
rm -rf .pytest_cache/

# 3. Reinstalar
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Reconfigurar
cp .env.example .env
# Editar .env con tus valores

# 5. Reiniciar
docker-compose up --build
python scripts/setup_complete.py
```

---

## 📞 Obtener Ayuda

1. Revisa los logs: `docker-compose logs`
2. Verifica la documentación: `docs/`
3. Revisa `.cursorrules` para convenciones
4. Consulta `docs/CURSOR_PROMPTS.md` para comandos

---

**Última actualización:** Enero 2024

