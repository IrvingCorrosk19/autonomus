"""
FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import configure_logging
from app.api.v1 import (
    webhooks, leads, intents, sentiment, router, chatbot, cases,
    escalation, followups, nurturing, sales, carts, payments,
    content, comments, data, predictions, alerts
)

# Configurar logging
configure_logging()

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Sistema CRM Autónomo con IA Multi-Agente",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(
    webhooks.router,
    prefix=f"{settings.API_V1_PREFIX}/webhooks",
    tags=["webhooks"]
)

app.include_router(
    leads.router,
    prefix=f"{settings.API_V1_PREFIX}/leads",
    tags=["leads"]
)

app.include_router(
    intents.router,
    prefix=f"{settings.API_V1_PREFIX}/intents",
    tags=["intents"]
)

app.include_router(
    sentiment.router,
    prefix=f"{settings.API_V1_PREFIX}/sentiment",
    tags=["sentiment"]
)

app.include_router(
    router.router,
    prefix=f"{settings.API_V1_PREFIX}/router",
    tags=["router"]
)

app.include_router(
    chatbot.router,
    prefix=f"{settings.API_V1_PREFIX}/chatbot",
    tags=["chatbot"]
)

app.include_router(
    cases.router,
    prefix=f"{settings.API_V1_PREFIX}/cases",
    tags=["cases"]
)

app.include_router(
    escalation.router,
    prefix=f"{settings.API_V1_PREFIX}/escalation",
    tags=["escalation"]
)

app.include_router(
    followups.router,
    prefix=f"{settings.API_V1_PREFIX}/followups",
    tags=["followups"]
)

app.include_router(
    nurturing.router,
    prefix=f"{settings.API_V1_PREFIX}/nurturing",
    tags=["nurturing"]
)

app.include_router(
    sales.router,
    prefix=f"{settings.API_V1_PREFIX}/sales",
    tags=["sales"]
)

app.include_router(
    carts.router,
    prefix=f"{settings.API_V1_PREFIX}/carts",
    tags=["carts"]
)

app.include_router(
    payments.router,
    prefix=f"{settings.API_V1_PREFIX}/payments",
    tags=["payments"]
)

app.include_router(
    content.router,
    prefix=f"{settings.API_V1_PREFIX}/content",
    tags=["content"]
)

app.include_router(
    comments.router,
    prefix=f"{settings.API_V1_PREFIX}/comments",
    tags=["comments"]
)

app.include_router(
    data.router,
    prefix=f"{settings.API_V1_PREFIX}/data",
    tags=["data"]
)

app.include_router(
    predictions.router,
    prefix=f"{settings.API_V1_PREFIX}/predictions",
    tags=["predictions"]
)

app.include_router(
    alerts.router,
    prefix=f"{settings.API_V1_PREFIX}/alerts",
    tags=["alerts"]
)


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": "Autonomous CRM API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

