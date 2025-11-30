"""
Script completo de setup del proyecto
"""
import asyncio
import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


async def check_database():
    """Verifica conexión a base de datos"""
    try:
        from app.db.session import AsyncSessionLocal
        from sqlalchemy import text
        async with AsyncSessionLocal() as db:
            await db.execute(text("SELECT 1"))
        print("✅ Conexión a base de datos: OK")
        return True
    except Exception as e:
        print(f"❌ Error de conexión a base de datos: {e}")
        return False


def check_env_file():
    """Verifica que exista archivo .env"""
    if os.path.exists(".env"):
        print("✅ Archivo .env encontrado")
        return True
    else:
        print("⚠️  Archivo .env no encontrado. Copiando desde .env.example...")
        try:
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Archivo .env creado. Por favor, edítalo con tus credenciales.")
            return True
        except Exception as e:
            print(f"❌ Error al crear .env: {e}")
            return False


def check_ai_credentials():
    """Verifica que existan credenciales de IA"""
    from app.core.config import settings
    
    has_credentials = False
    if settings.OPENAI_API_KEY:
        print("✅ OpenAI API Key configurada")
        has_credentials = True
    else:
        print("⚠️  OpenAI API Key no configurada")
    
    if settings.ANTHROPIC_API_KEY:
        print("✅ Anthropic API Key configurada")
        has_credentials = True
    else:
        print("⚠️  Anthropic API Key no configurada")
    
    if not has_credentials:
        print("⚠️  ADVERTENCIA: Necesitas al menos una API Key de IA para que funcione")
    
    return has_credentials


async def init_database():
    """Inicializa la base de datos"""
    try:
        from app.db.base import Base
        from app.models import *
        from app.db.session import async_engine
        
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("✅ Base de datos inicializada")
        return True
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        return False


async def main():
    """Ejecuta setup completo"""
    print("=" * 60)
    print("SETUP COMPLETO - Autonomous CRM")
    print("=" * 60)
    print()
    
    # 1. Verificar .env
    if not check_env_file():
        print("\n❌ Setup incompleto. Por favor, crea el archivo .env")
        return
    
    # 2. Verificar credenciales de IA
    check_ai_credentials()
    print()
    
    # 3. Verificar base de datos
    if not await check_database():
        print("\n⚠️  No se pudo conectar a la base de datos.")
        print("   Asegúrate de que PostgreSQL esté corriendo:")
        print("   docker-compose up -d postgres")
        return
    
    # 4. Inicializar base de datos
    print("\n📦 Inicializando base de datos...")
    if not await init_database():
        print("\n❌ Error al inicializar base de datos")
        return
    
    # 5. Poblar con datos de prueba
    print("\n📊 Poblando base de datos con datos de prueba...")
    try:
        from scripts.seed_db import seed_database
        await seed_database()
    except Exception as e:
        print(f"⚠️  Error al poblar datos: {e}")
    
    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETADO")
    print("=" * 60)
    print("\nPróximos pasos:")
    print("1. Edita .env con tus credenciales de APIs")
    print("2. Inicia los servicios: docker-compose up -d")
    print("3. Prueba la API: python scripts/test_api.py")
    print("4. Accede a la documentación: http://localhost:8000/docs")


if __name__ == "__main__":
    asyncio.run(main())

