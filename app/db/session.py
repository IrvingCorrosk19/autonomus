"""
Sesiones de base de datos
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from typing import AsyncGenerator
from app.core.config import settings

# Motor asíncrono
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Motor síncrono (para Alembic)
sync_engine = create_engine(
    settings.DATABASE_SYNC_URL,
    echo=settings.DEBUG,
)

# Session makers
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

SessionLocal = sessionmaker(
    bind=sync_engine,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency para obtener sesión de DB asíncrona"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_db():
    """Dependency para obtener sesión de DB síncrona (para Alembic)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

