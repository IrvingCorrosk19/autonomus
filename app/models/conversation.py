"""
Modelo de Conversación
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime
import uuid


class ConversationStatus(enum.Enum):
    ACTIVE = "active"
    WAITING_CUSTOMER = "waiting_customer"
    WAITING_AGENT = "waiting_agent"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    
    channel = Column(String, nullable=False)  # whatsapp, instagram, messenger
    status = Column(Enum(ConversationStatus), default=ConversationStatus.ACTIVE)
    
    # Analytics
    message_count = Column(Integer, default=0)
    avg_sentiment_score = Column(Float, nullable=True)
    bot_handled = Column(Boolean, default=True)
    escalated = Column(Boolean, default=False)
    escalation_reason = Column(String, nullable=True)
    
    # Timestamps
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_message_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationships
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    lead = relationship("Lead", back_populates="conversations")
    customer = relationship("Customer", back_populates="conversations")

