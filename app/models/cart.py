"""
Modelo de Cart (Carrito)
"""
from sqlalchemy import Column, String, Float, DateTime, Integer, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import uuid


class Cart(Base):
    __tablename__ = "carts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    
    items = Column(JSON, nullable=False)  # [{"product_id": "...", "quantity": 2}]
    total_amount = Column(Float, nullable=False)
    
    status = Column(String, default="pending")  # pending, recovered, abandoned, completed
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_activity = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    recovery_attempt_count = Column(Integer, default=0)
    discount_codes_used = Column(JSON, nullable=True)
    recovered_at = Column(DateTime, nullable=True)
    recovery_channel = Column(String, nullable=True)
    final_attempt = Column(Boolean, default=False)
    
    customer = relationship("Customer", back_populates="carts")

