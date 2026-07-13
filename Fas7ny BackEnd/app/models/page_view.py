"""
تسجيل بسيط لكل زيارة لصفحة خدمة/فندق. صف واحد لكل زيارة - بسيط
عن قصد، مفيش session tracking أو user identification معقد.
لو المشروع كبر بعدين ومحتاج analytics أدق (unique visitors,
bounce rate...) وقتها نستبدله بحل مخصص.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey

from app.db.session import Base


class PageView(Base):
    __tablename__ = "page_views"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("provider_profiles.id"), nullable=False, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)

    viewed_at = Column(DateTime, default=datetime.utcnow, index=True)
