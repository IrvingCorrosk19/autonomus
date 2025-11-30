# 🐳 Contenedores Docker - Autonomous CRM

## Contenedores Actuales (4/4 Básicos)

### ✅ 1. PostgreSQL
- **Imagen:** `postgres:15-alpine`
- **Puerto:** `5432`
- **Volumen:** `postgres_data`
- **Función:** Base de datos principal
- **Estado:** ✅ Configurado

### ✅ 2. Redis
- **Imagen:** `redis:7-alpine`
- **Puerto:** `6379`
- **Volumen:** `redis_data`
- **Función:** Cache y cola de trabajos
- **Estado:** ✅ Configurado

### ✅ 3. FastAPI
- **Imagen:** Construida desde `Dockerfile`
- **Puerto:** `8000`
- **Volúmenes:** `./app`, `./storage`
- **Función:** API principal con todos los servicios
- **Estado:** ✅ Configurado

### ✅ 4. n8n
- **Imagen:** `n8nio/n8n:latest`
- **Puerto:** `5678`
- **Volumen:** `n8n_data`
- **Función:** Orquestación de workflows
- **Estado:** ✅ Configurado

---

## Contenedores Opcionales (Recomendados)

### ⚠️ 5. Celery Worker (Opcional)
Para ejecutar jobs en background de forma más robusta:
- Procesar mensajes
- Enviar follow-ups
- Recuperar carritos
- Enviar alertas

### ⚠️ 6. Celery Beat (Opcional)
Para scheduling de tareas periódicas:
- Jobs cada hora
- Jobs diarios
- Jobs semanales

### ⚠️ 7. Prometheus (Opcional)
Para monitoreo y métricas

### ⚠️ 8. Grafana (Opcional)
Para dashboards de monitoreo

---

## Resumen

**Contenedores Básicos:** ✅ 4/4 (100%)
- PostgreSQL ✅
- Redis ✅
- FastAPI ✅
- n8n ✅

**Contenedores Opcionales:** 0/4 (pueden agregarse después)

**Total:** 4 contenedores esenciales configurados

---

## ¿Necesitamos más contenedores?

Para el funcionamiento básico: **NO**, ya tenemos todo lo necesario.

Para producción avanzada: Podríamos agregar:
- Celery Worker/Beat (para jobs robustos)
- Monitoreo (Prometheus/Grafana)
- Nginx (reverse proxy)
- Certbot (SSL)

Pero para desarrollo y pruebas, **los 4 contenedores actuales son suficientes**.

