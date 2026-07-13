"""
التقييمات - قايمة "التقييمات الأخيرة" في الداشبورد.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from app.db.session import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("provider_profiles.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String, nullable=False)

    rating = Column(Float, nullable=False)     # من 1 لـ 5
    title = Column(String, nullable=True)       # "إقامة رائعة وإطلالة خيالية"
    comment = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("ProviderProfile", back_populates="reviews")
