"""
Dependencies para FastAPI
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.logging import get_logger

logger = get_logger(__name__)


async def get_database() -> AsyncGenerator[AsyncSession, None]:
    """Dependency para obtener sesión de base de datos"""
    async for session in get_db():
        yield session

