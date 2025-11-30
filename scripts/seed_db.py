"""
Script para poblar la base de datos con datos de prueba
"""
import asyncio
from datetime import datetime, timedelta
from app.db.session import AsyncSessionLocal
from app.models.lead import Lead, LeadStatus
from app.models.customer import Customer
from app.models.conversation import Conversation, ConversationStatus
from app.models.message import Message, MessageChannel
from app.models.cart import Cart
from app.core.logging import configure_logging

configure_logging()


async def seed_database():
    """Pobla la base de datos con datos de ejemplo"""
    async with AsyncSessionLocal() as db:
        try:
            # Crear leads de ejemplo
            leads = [
                Lead(
                    name="Juan Pérez",
                    email="juan.perez@example.com",
                    phone="+50761234567",
                    company="Tech Corp",
                    score=85,
                    category="hot",
                    status=LeadStatus.QUALIFIED,
                    source="whatsapp",
                    created_at=datetime.utcnow() - timedelta(days=1)
                ),
                Lead(
                    name="María González",
                    email="maria.gonzalez@example.com",
                    phone="+50761234568",
                    company="Retail Store",
                    score=65,
                    category="warm",
                    status=LeadStatus.NEW,
                    source="instagram",
                    created_at=datetime.utcnow() - timedelta(hours=5)
                ),
                Lead(
                    name="Carlos Rodríguez",
                    email="carlos.rodriguez@example.com",
                    phone="+50761234569",
                    score=45,
                    category="cold",
                    status=LeadStatus.NURTURING,
                    source="website",
                    created_at=datetime.utcnow() - timedelta(days=3)
                ),
            ]
            
            for lead in leads:
                db.add(lead)
            
            await db.flush()
            
            # Crear customer de ejemplo
            customer = Customer(
                lead_id=leads[0].id,
                name="Juan Pérez",
                email="juan.perez@example.com",
                phone="+50761234567",
                company="Tech Corp",
                total_purchases=3,
                total_spent=1500.0,
                avg_order_value=500.0,
                predicted_clv=5000.0,
                purchasing_power="high",
                segment="vip",
                status="active"
            )
            db.add(customer)
            await db.flush()
            
            # Crear conversación de ejemplo
            conversation = Conversation(
                lead_id=leads[0].id,
                customer_id=customer.id,
                channel="whatsapp",
                status=ConversationStatus.ACTIVE,
                message_count=5,
                avg_sentiment_score=0.7,
                bot_handled=True,
                started_at=datetime.utcnow() - timedelta(hours=2),
                last_message_at=datetime.utcnow() - timedelta(minutes=30)
            )
            db.add(conversation)
            await db.flush()
            
            # Crear mensajes de ejemplo
            messages = [
                Message(
                    conversation_id=conversation.id,
                    content="Hola, estoy interesado en sus productos",
                    sender="customer",
                    direction="inbound",
                    intent="purchase_inquiry",
                    sentiment="positive",
                    sentiment_score=0.6,
                    sent_at=datetime.utcnow() - timedelta(hours=2)
                ),
                Message(
                    conversation_id=conversation.id,
                    content="¡Hola! Con gusto te ayudo. ¿Qué tipo de producto buscas?",
                    sender="bot",
                    direction="outbound",
                    sent_at=datetime.utcnow() - timedelta(hours=2, minutes=-1)
                ),
            ]
            
            for message in messages:
                db.add(message)
            
            # Crear carrito de ejemplo
            cart = Cart(
                customer_id=customer.id,
                items=[
                    {"product_id": "prod_123", "name": "Laptop Dell XPS", "quantity": 1, "price": 1200.0}
                ],
                total_amount=1200.0,
                status="pending",
                created_at=datetime.utcnow() - timedelta(hours=1),
                last_activity=datetime.utcnow() - timedelta(hours=1)
            )
            db.add(cart)
            
            await db.commit()
            
            print("✅ Base de datos poblada exitosamente!")
            print(f"   - {len(leads)} leads creados")
            print(f"   - 1 customer creado")
            print(f"   - 1 conversación creada")
            print(f"   - {len(messages)} mensajes creados")
            print(f"   - 1 carrito creado")
            
        except Exception as e:
            await db.rollback()
            print(f"❌ Error al poblar base de datos: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed_database())

