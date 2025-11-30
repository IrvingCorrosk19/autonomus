"""
Modelo de Clasificación de Lead
"""
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
import uuid


class LeadClassification(Base):
    __tablename__ = "lead_classifications"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = Column(String, ForeignKey("leads.id"), nullable=False)
    
    score = Column(Integer, nullable=False)  # 0-100
    category = Column(String, nullable=True)  # hot, warm, cold
    reasoning = Column(Text, nullable=True)
    recommended_action = Column(String, nullable=True)
    
    ai_model = Column(String, nullable=True)
    classified_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    lead = relationship("Lead", back_populates="classifications")

