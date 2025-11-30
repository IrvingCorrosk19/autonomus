"""
Configuración de pytest
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client():
    """Cliente HTTP para testing"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

