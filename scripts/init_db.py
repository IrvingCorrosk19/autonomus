"""
Script para inicializar la base de datos
"""
import asyncio
from sqlalchemy import text
from app.db.session import async_engine
from app.core.logging import configure_logging

configure_logging()


async def init_db():
    """Crea las tablas en la base de datos"""
    from app.db.base import Base
    from app.models import *  # Importar todos los modelos
    
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Base de datos inicializada correctamente")


if __name__ == "__main__":
    asyncio.run(init_db())

