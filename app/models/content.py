"""
Modelo de GeneratedContent
"""
from sqlalchemy import Column, String, Text, DateTime, Integer, Float, JSON
from app.db.base import Base
from datetime import datetime
import uuid


class GeneratedContent(Base):
    __tablename__ = "generated_content"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    content_type = Column(String, nullable=False)  # image, video, text, carousel
    platform = Column(String, nullable=False)  # instagram, facebook, tiktok
    
    asset_url = Column(String, nullable=True)
    copy = Column(Text, nullable=True)
    hashtags = Column(JSON, nullable=True)
    
    status = Column(String, default="draft")  # draft, scheduled, published
    scheduled_for = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    
    # Performance
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    engagement_rate = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

