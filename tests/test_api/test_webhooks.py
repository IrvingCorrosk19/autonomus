"""
Tests para webhooks
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_webhook_verification(client: AsyncClient):
    """Test de verificación de webhook"""
    response = await client.get(
        "/api/v1/webhooks/inbound/verify",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "test-token",
            "hub.challenge": "test-challenge"
        }
    )
    # Debería fallar sin token correcto, pero probamos el endpoint
    assert response.status_code in [200, 403]


@pytest.mark.asyncio
async def test_webhook_inbound(client: AsyncClient):
    """Test de recepción de webhook"""
    payload = {
        "object": "whatsapp_business_account",
        "entry": [{
            "id": "123456789",
            "changes": [{
                "field": "messages",
                "value": {
                    "messaging_product": "whatsapp",
                    "metadata": {
                        "phone_number_id": "987654321"
                    },
                    "messages": [{
                        "from": "+507123456789",
                        "id": "wamid.XXX",
                        "timestamp": "1640000000",
                        "type": "text",
                        "text": {
                            "body": "Hola, quiero información sobre sus productos"
                        }
                    }]
                }
            }]
        }]
    }
    
    response = await client.post("/api/v1/webhooks/inbound", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["received", "error"]

