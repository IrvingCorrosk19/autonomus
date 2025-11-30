# 🚀 Autonomous CRM - Sistema CRM Autónomo con IA

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistema CRM Autónomo con IA Multi-Agente que gestiona el ciclo completo de vida del cliente desde el primer contacto hasta el cierre de venta.

## ✨ Características

- ✅ **22 Flujos Automatizados** - Procesamiento completo del ciclo de vida
- ✅ **26 Endpoints API** - RESTful API completa
- ✅ **IA Multi-Modelo** - OpenAI GPT-4 y Anthropic Claude
- ✅ **Omnicanal** - WhatsApp, Instagram, Facebook Messenger
- ✅ **Orquestación n8n** - Workflows visuales
- ✅ **Base de Datos Completa** - 12 modelos con relaciones
- ✅ **Docker Ready** - 4 contenedores configurados

## 🚀 Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/IrvingCorrosk19/autonomus.git
cd autonomus

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales (mínimo: OPENAI_API_KEY o ANTHROPIC_API_KEY)

# 3. Setup completo
python scripts/setup_complete.py

# 4. Iniciar servicios
docker-compose up -d

# 5. Probar
python scripts/test_complete.py
```

## 📚 Documentación

- **[DOCUMENTACION_COMPLETA.md](DOCUMENTACION_COMPLETA.md)** - Documentación exhaustiva
- **[QUICKSTART.md](QUICKSTART.md)** - Guía rápida de inicio
- **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** - Resumen visual
- **[INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md)** - Índice de documentos

## 📊 Estadísticas

- **Flujos:** 22/22 (100%)
- **Endpoints:** 26
- **Modelos DB:** 12
- **Servicios:** 22
- **Contenedores:** 4

## 🔗 Enlaces

- **API Docs:** `http://localhost:8000/docs`
- **n8n:** `http://localhost:5678` (admin/admin123)

## 📝 Licencia

MIT License

---

⭐ Si te gusta este proyecto, dale una estrella!

