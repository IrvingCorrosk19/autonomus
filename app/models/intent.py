"""
Modelo de Intención
"""
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime
import uuid


class IntentType(enum.Enum):
    PURCHASE_INQUIRY = "purchase_inquiry"
    PRODUCT_INFO = "product_info"
    PRICING_QUESTION = "pricing_question"
    COMPLAINT = "complaint"
    SUPPORT_REQUEST = "support_request"
    WARRANTY_CLAIM = "warranty_claim"
    DELIVERY_TRACKING = "delivery_tracking"
    REFUND_REQUEST = "refund_request"
    PARTNERSHIP = "partnership"
    GENERAL_INQUIRY = "general_inquiry"
    SPAM = "spam"


class LeadIntent(Base):
    __tablename__ = "lead_intents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    message_id = Column(String, ForeignKey("messages.id"), nullable=True)
    
    primary_intent = Column(String, nullable=False)
    secondary_intents = Column(JSON, nullable=True)
    confidence = Column(Float, nullable=True)
    entities = Column(JSON, nullable=True)
    
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    lead = relationship("Lead", back_populates="intents")

