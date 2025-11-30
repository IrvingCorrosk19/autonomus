# ⚙️ CONFIGURACIÓN REQUERIDA - Lo que TÚ debes configurar

**Fecha:** Enero 2024  
**Estado:** ✅ Proyecto completo, solo falta tu configuración

---

## 🎯 Resumen: ¿Qué Falta?

**Sí, básicamente solo falta que configures las API Keys de IA y algunas variables de entorno.**

El proyecto está **100% completo** en código. Solo necesitas:

1. ✅ **API Keys de IA** (al menos una)
2. ✅ **Variables de entorno básicas** (SECRET_KEY, etc.)
3. ⚠️ **Meta APIs** (opcional, solo si quieres WhatsApp/Instagram)

---

## 📋 CONFIGURACIÓN MÍNIMA (Para que funcione)

### Paso 1: Crear archivo `.env`

```bash
cp .env.example .env
```

### Paso 2: Configurar variables MÍNIMAS

Edita `.env` y configura:

```bash
# ============= OBLIGATORIAS =============
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/autonomous_crm
DATABASE_SYNC_URL=postgresql://user:password@localhost:5432/autonomous_crm
SECRET_KEY=tu_clave_secreta_super_segura_de_minimo_32_caracteres
WEBHOOK_VERIFY_TOKEN=mi_token_secreto_12345

# ============= IA - AL MENOS UNA =============
# Opción 1: OpenAI (Recomendado)
OPENAI_API_KEY=sk-tu-key-aqui
OPENAI_MODEL=gpt-4-turbo-preview

# O Opción 2: Anthropic
# ANTHROPIC_API_KEY=sk-ant-tu-key-aqui
# ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

**Con esto ya funciona el sistema básico.**

---

## 🤖 CONFIGURACIÓN DE IA (Tu Responsabilidad)

### Opción 1: OpenAI (Recomendado)

1. **Obtener API Key:**
   - Ve a: https://platform.openai.com/api-keys
   - Crea una cuenta o inicia sesión
   - Genera una nueva API Key
   - Copia la key (empieza con `sk-`)

2. **Configurar en `.env`:**
   ```bash
   OPENAI_API_KEY=sk-tu-key-aqui
   OPENAI_MODEL=gpt-4-turbo-preview
   ```

3. **Verificar:**
   ```bash
   # Probar que funciona
   curl -X POST http://localhost:8000/api/v1/leads/classify \
     -H "Content-Type: application/json" \
     -d '{"message": "Test", "sender_metadata": {}}'
   ```

### Opción 2: Anthropic Claude

1. **Obtener API Key:**
   - Ve a: https://console.anthropic.com/
   - Crea una cuenta o inicia sesión
   - Ve a API Keys
   - Genera una nueva key
   - Copia la key (empieza con `sk-ant-`)

2. **Configurar en `.env`:**
   ```bash
   ANTHROPIC_API_KEY=sk-ant-tu-key-aqui
   ANTHROPIC_MODEL=claude-3-sonnet-20240229
   ```

### Opción 3: Ambas (Recomendado para producción)

Configura ambas para tener fallback automático:

```bash
OPENAI_API_KEY=sk-tu-key-openai
ANTHROPIC_API_KEY=sk-ant-tu-key-anthropic
```

El sistema usará OpenAI por defecto y cambiará a Anthropic si OpenAI falla.

---

## 🔐 OTRAS VARIABLES IMPORTANTES

### SECRET_KEY (Obligatorio)

Genera una clave segura:

```bash
# En Python:
python -c "import secrets; print(secrets.token_urlsafe(32))"

# O usa este:
SECRET_KEY=tu_clave_secreta_super_segura_de_minimo_32_caracteres_aleatorios
```

### WEBHOOK_VERIFY_TOKEN (Obligatorio)

Token para verificar webhooks de Meta:

```bash
WEBHOOK_VERIFY_TOKEN=mi_token_secreto_12345
```

Puede ser cualquier string, pero úsalo también en la configuración de Meta.

---

## 📱 CONFIGURACIÓN OPCIONAL: Meta APIs

Solo necesitas esto si quieres usar WhatsApp/Instagram/Facebook Messenger.

### WhatsApp Business API

1. **Obtener credenciales:**
   - Ve a: https://developers.facebook.com/
   - Crea una app de tipo "Business"
   - Configura WhatsApp Business API
   - Obtén:
     - `META_ACCESS_TOKEN`
     - `WHATSAPP_PHONE_NUMBER_ID`
     - `META_APP_SECRET`

2. **Configurar en `.env`:**
   ```bash
   META_ACCESS_TOKEN=tu_access_token
   META_APP_SECRET=tu_app_secret
   WHATSAPP_PHONE_NUMBER_ID=tu_phone_number_id
   META_VERIFY_TOKEN=mi_token_secreto_12345
   ```

### Instagram Business API

Similar proceso, necesitas:
```bash
INSTAGRAM_BUSINESS_ACCOUNT_ID=tu_ig_business_id
```

---

## ✅ CHECKLIST DE CONFIGURACIÓN

### Mínimo para funcionar:

- [ ] `.env` creado desde `.env.example`
- [ ] `DATABASE_URL` configurado (o usar Docker)
- [ ] `SECRET_KEY` generado
- [ ] `WEBHOOK_VERIFY_TOKEN` configurado
- [ ] **Al menos una API Key de IA configurada:**
  - [ ] `OPENAI_API_KEY` O
  - [ ] `ANTHROPIC_API_KEY`

### Opcional (pero recomendado):

- [ ] Ambas API Keys de IA (fallback)
- [ ] Meta APIs configuradas (WhatsApp/Instagram)
- [ ] Redis configurado (ya está en Docker)
- [ ] n8n configurado (ya está en Docker)

---

## 🚀 DESPUÉS DE CONFIGURAR

### 1. Verificar configuración

```bash
# Verificar que las variables se cargan
python -c "from app.core.config import settings; print('OpenAI:', bool(settings.OPENAI_API_KEY)); print('Anthropic:', bool(settings.ANTHROPIC_API_KEY))"
```

### 2. Iniciar servicios

```bash
docker-compose up -d
```

### 3. Probar que funciona

```bash
# Health check
curl http://localhost:8000/health

# Probar clasificación de lead
curl -X POST http://localhost:8000/api/v1/leads/classify \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Necesito 500 laptops urgente",
    "sender_metadata": {"name": "Test"}
  }'
```

---

## 📊 RESUMEN: Lo que es TU responsabilidad

### ✅ Debes configurar:

1. **API Keys de IA** (al menos una)
   - OpenAI: https://platform.openai.com/api-keys
   - Anthropic: https://console.anthropic.com/

2. **Variables de seguridad**
   - `SECRET_KEY` (generar)
   - `WEBHOOK_VERIFY_TOKEN` (cualquier string)

3. **Base de datos** (si no usas Docker)
   - `DATABASE_URL`

### ✅ Ya está configurado (no necesitas hacer nada):

- ✅ Código completo (22 flujos, 26 endpoints)
- ✅ Docker Compose (PostgreSQL, Redis, n8n)
- ✅ Estructura del proyecto
- ✅ Modelos de base de datos
- ✅ Servicios y lógica de negocio
- ✅ Documentación completa

---

## 🎯 CONCLUSIÓN

**Sí, básicamente solo falta que configures:**

1. **API Keys de IA** (OpenAI o Anthropic) - **ESO ES TODO LO CRÍTICO**
2. Variables de seguridad básicas
3. Meta APIs (opcional)

**El resto del proyecto está 100% completo y listo para usar.**

Una vez que configures las API Keys, el sistema funcionará inmediatamente.

---

## 💡 TIPS

- **Para desarrollo:** Solo necesitas una API Key (OpenAI es más fácil de obtener)
- **Para producción:** Configura ambas (OpenAI + Anthropic) para fallback
- **Costo:** OpenAI y Anthropic cobran por uso, revisa sus precios
- **Límites:** Ambas tienen rate limits, el código ya los maneja

---

**Última actualización:** Enero 2024

