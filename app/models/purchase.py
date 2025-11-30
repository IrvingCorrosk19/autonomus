"""
Modelo de Purchase (Compra)
"""
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import uuid


class Purchase(Base):
    __tablename__ = "purchases"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    
    items = Column(JSON, nullable=False)
    total_amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, paid, shipped, delivered, cancelled
    
    purchased_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    customer = relationship("Customer", back_populates="purchases")

