"""
Script para probar la API
"""
import asyncio
import httpx
import json


async def test_classify_lead():
    """Prueba el endpoint de clasificación de leads"""
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        payload = {
            "message": "Hola, soy dueño de una empresa y necesito 500 unidades urgente",
            "sender_metadata": {
                "name": "Juan Pérez",
                "phone": "+507123456789",
                "previous_interactions": 0,
                "source": "whatsapp"
            }
        }
        
        response = await client.post("/api/v1/leads/classify", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")


async def test_detect_intent():
    """Prueba el endpoint de detección de intención"""
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        payload = {
            "message": "Necesito 10 laptops para mañana, tienen stock?",
            "context": {}
        }
        
        response = await client.post("/api/v1/intents/detect", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")


async def test_analyze_sentiment():
    """Prueba el endpoint de análisis de sentimiento"""
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        payload = {
            "message": "Compré hace 2 semanas y el producto llegó defectuoso, quiero reembolso"
        }
        
        response = await client.post("/api/v1/sentiment/analyze", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")


async def main():
    """Ejecuta todos los tests"""
    print("=" * 50)
    print("Test: Clasificación de Lead")
    print("=" * 50)
    await test_classify_lead()
    
    print("\n" + "=" * 50)
    print("Test: Detección de Intención")
    print("=" * 50)
    await test_detect_intent()
    
    print("\n" + "=" * 50)
    print("Test: Análisis de Sentimiento")
    print("=" * 50)
    await test_analyze_sentiment()


if __name__ == "__main__":
    asyncio.run(main())

