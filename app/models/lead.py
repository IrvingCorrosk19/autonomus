"""
Modelo de Lead
"""
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime
import uuid


class LeadStatus(enum.Enum):
    NEW = "new"
    QUALIFIED = "qualified"
    NURTURING = "nurturing"
    CONVERTED = "converted"
    LOST = "lost"


class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    
    # Classification
    score = Column(Integer, default=0)  # 0-100
    category = Column(String, nullable=True)  # hot, warm, cold
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    
    # Source
    source = Column(String, nullable=True)  # whatsapp, instagram, messenger, website
    campaign_id = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    converted_at = Column(DateTime, nullable=True)
    
    # Relationships
    classifications = relationship("LeadClassification", back_populates="lead", cascade="all, delete-orphan")
    intents = relationship("LeadIntent", back_populates="lead", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="lead", cascade="all, delete-orphan")

