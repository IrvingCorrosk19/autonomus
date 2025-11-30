"""
Modelo de Invoice (Factura)
"""
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import uuid


class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    customer_id = Column(String, ForeignKey("customers.id"), nullable=False)
    purchase_id = Column(String, ForeignKey("purchases.id"), nullable=True)
    
    number = Column(String, unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, paid, overdue, cancelled
    
    issued_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=False)
    paid_at = Column(DateTime, nullable=True)
    
    late_fee = Column(Float, default=0.0)
    reminder_count = Column(Integer, default=0)
    
    customer = relationship("Customer")

