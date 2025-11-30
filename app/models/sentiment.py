"""
Modelo de Análisis de Sentimiento
"""
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum
from datetime import datetime
import uuid


class SentimentType(enum.Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analyses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    message_id = Column(String, ForeignKey("messages.id"), nullable=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=True)
    
    sentiment = Column(String, nullable=False)  # positive, neutral, negative
    score = Column(Float, nullable=False)  # -1.0 a +1.0
    confidence = Column(Float, nullable=True)
    emotions = Column(JSON, nullable=True)  # {"anger": 0.65, "frustration": 0.82}
    urgency_level = Column(String, nullable=True)  # low, medium, high, critical
    churn_risk = Column(Float, nullable=True)  # 0-100
    
    ai_model = Column(String, nullable=True)
    analyzed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

