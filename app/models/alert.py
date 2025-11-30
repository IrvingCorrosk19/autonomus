"""
Modelo de Alert
"""
from sqlalchemy import Column, String, Text, DateTime, JSON
from app.db.base import Base
from datetime import datetime
import uuid


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    type = Column(String, nullable=False)  # sales_drop, churn_risk, hot_lead, etc
    severity = Column(String, nullable=False)  # low, medium, high, critical
    message = Column(Text, nullable=False)
    data = Column(JSON, nullable=True)
    
    status = Column(String, default="active")  # active, acknowledged, resolved
    acknowledged_by = Column(String, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

