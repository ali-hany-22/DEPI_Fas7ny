"""
الخدمات اللي المزود بيعرضها (زي "غرفة مزدوجة - كلاسيكية" و
"جناح ملكي - إطلالة النيل" في الصورة). كل خدمة ليها زرار
"تعطيل/تفعيل" و"تعديل".
"""

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from app.db.session import Base


class ServiceStatus(str, enum.Enum):
    active = "active"      # "نشط"
    disabled = "disabled"  # "معطل"


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("provider_profiles.id"), nullable=False)

    title = Column(String, nullable=False)          # "غرفة مزدوجة - كلاسيكية"
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)

    status = Column(SAEnum(ServiceStatus), default=ServiceStatus.active)
    requires_confirmation = Column(Boolean, default=False)  # "يتطلب تأكيد"

    bookings_this_month = Column(Integer, default=0)  # "12 حجز هذا الشهر"

    created_at = Column(DateTime, default=datetime.utcnow)

    provider = relationship("ProviderProfile", back_populates="services")
    bookings = relationship("Booking", back_populates="service")
