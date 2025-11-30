"""
Modelo de Customer
"""
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import uuid


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=True)
    
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    company = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    
    # Enrichment
    predicted_clv = Column(Float, nullable=True)
    purchasing_power = Column(String, nullable=True)  # low, medium, high
    interests = Column(JSON, nullable=True)
    segment = Column(String, nullable=True)  # vip, regular, at_risk
    
    # Engagement
    total_purchases = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    avg_order_value = Column(Float, nullable=True)
    last_purchase_date = Column(DateTime, nullable=True)
    
    # Status
    status = Column(String, default="active")  # active, inactive, churned
    churn_risk_score = Column(Float, nullable=True)  # 0-1
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.utcnow, nullable=True)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="customer")
    carts = relationship("Cart", back_populates="customer")
    purchases = relationship("Purchase", back_populates="customer")

