"""
Modelos de Mensajes
"""
from sqlalchemy import Column, String, Text, DateTime, Enum, Boolean, JSON, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime
import uuid


class MessageChannel(enum.Enum):
    WHATSAPP = "whatsapp"
    INSTAGRAM = "instagram"
    MESSENGER = "messenger"


class RawMessage(Base):
    """Mensaje raw recibido del webhook"""
    __tablename__ = "raw_messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    channel = Column(Enum(MessageChannel), nullable=False)
    sender_id = Column(String, nullable=False)  # Phone/IGID/PSID
    content = Column(Text, nullable=False)
    metadata = Column(JSON, nullable=True)  # Payload completo
    received_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Boolean, default=False)
    processing_error = Column(String, nullable=True)


class Message(Base):
    """Mensaje procesado y normalizado"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    
    content = Column(Text, nullable=False)
    sender = Column(String, nullable=False)  # customer, bot, agent
    direction = Column(String, nullable=False)  # inbound, outbound
    
    # AI Analysis
    intent = Column(String, nullable=True)
    sentiment = Column(String, nullable=True)
    sentiment_score = Column(Float, nullable=True)
    
    # Timestamps
    sent_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    delivered_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    
    # Relationship
    conversation = relationship("Conversation", back_populates="messages")

