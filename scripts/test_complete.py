"""
Script completo de pruebas del sistema
"""
import asyncio
import httpx
import json
from datetime import datetime


BASE_URL = "http://localhost:8000"


async def test_health():
    """Test de health check"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Health check: OK")
                return True
            else:
                print(f"❌ Health check: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check falló: {e}")
            return False


async def test_classify_lead():
    """Test de clasificación de lead"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            payload = {
                "message": "Hola, soy dueño de una empresa y necesito 500 unidades urgente para mañana",
                "sender_metadata": {
                    "name": "Juan Pérez",
                    "phone": "+507123456789",
                    "previous_interactions": 0,
                    "source": "whatsapp"
                }
            }
            
            response = await client.post(f"{BASE_URL}/api/v1/leads/classify", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Clasificación de lead: OK")
                print(f"   Score: {data.get('score')}")
                print(f"   Categoría: {data.get('category')}")
                return True
            else:
                print(f"❌ Clasificación falló: {response.status_code}")
                print(f"   {response.text}")
                return False
        except Exception as e:
            print(f"❌ Clasificación falló: {e}")
            return False


async def test_detect_intent():
    """Test de detección de intención"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            payload = {
                "message": "Necesito 10 laptops para mañana, tienen stock?",
                "context": {}
            }
            
            response = await client.post(f"{BASE_URL}/api/v1/intents/detect", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Detección de intención: OK")
                print(f"   Intención: {data.get('primary_intent')}")
                print(f"   Confianza: {data.get('confidence')}")
                return True
            else:
                print(f"❌ Detección de intención falló: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Detección de intención falló: {e}")
            return False


async def test_sentiment_analysis():
    """Test de análisis de sentimiento"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            payload = {
                "message": "Compré hace 2 semanas y el producto llegó defectuoso, quiero reembolso"
            }
            
            response = await client.post(f"{BASE_URL}/api/v1/sentiment/analyze", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Análisis de sentimiento: OK")
                print(f"   Sentimiento: {data.get('sentiment')}")
                print(f"   Score: {data.get('score')}")
                return True
            else:
                print(f"❌ Análisis de sentimiento falló: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Análisis de sentimiento falló: {e}")
            return False


async def test_chatbot():
    """Test de chatbot"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            payload = {
                "message": "Hola, busco una laptop para programación",
                "context": {
                    "customer_id": None,
                    "conversation_id": None,
                    "conversation_history": []
                }
            }
            
            response = await client.post(f"{BASE_URL}/api/v1/chatbot/respond", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Chatbot: OK")
                print(f"   Respuesta: {data.get('content', '')[:100]}...")
                return True
            else:
                print(f"❌ Chatbot falló: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Chatbot falló: {e}")
            return False


async def test_webhook():
    """Test de webhook"""
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
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
            
            response = await client.post(f"{BASE_URL}/api/v1/webhooks/inbound", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Webhook: OK")
                print(f"   Status: {data.get('status')}")
                return True
            else:
                print(f"❌ Webhook falló: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Webhook falló: {e}")
            return False


async def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("PRUEBAS COMPLETAS - Autonomous CRM")
    print("=" * 60)
    print()
    
    print("⚠️  Asegúrate de que el servidor esté corriendo:")
    print("   uvicorn app.main:app --reload")
    print()
    
    results = []
    
    # Health check
    print("1. Health Check...")
    results.append(await test_health())
    print()
    
    # Webhook
    print("2. Webhook de Entrada...")
    results.append(await test_webhook())
    print()
    
    # Clasificación
    print("3. Clasificación de Lead...")
    results.append(await test_classify_lead())
    print()
    
    # Intención
    print("4. Detección de Intención...")
    results.append(await test_detect_intent())
    print()
    
    # Sentimiento
    print("5. Análisis de Sentimiento...")
    results.append(await test_sentiment_analysis())
    print()
    
    # Chatbot
    print("6. Chatbot Autónomo...")
    results.append(await test_chatbot())
    print()
    
    # Resumen
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"RESULTADOS: {passed}/{total} pruebas pasaron")
    print("=" * 60)
    
    if passed == total:
        print("✅ Todas las pruebas pasaron!")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")


if __name__ == "__main__":
    asyncio.run(main())

