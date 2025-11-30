"""
Modelo de Case (Ticket/Caso)
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime
import uuid


class CaseStatus(enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_CUSTOMER = "waiting_customer"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Case(Base):
    __tablename__ = "cases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True)
    
    description = Column(String, nullable=False)
    status = Column(Enum(CaseStatus), default=CaseStatus.OPEN)
    priority = Column(Integer, default=3)  # 1-5
    
    opened_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    closed_at = Column(DateTime, nullable=True)
    resolution_time_hours = Column(Float, nullable=True)
    
    closure_reason = Column(String, nullable=True)
    customer_satisfaction = Column(Integer, nullable=True)  # 1-5
    predicted_csat = Column(Float, nullable=True)  # ML prediction

