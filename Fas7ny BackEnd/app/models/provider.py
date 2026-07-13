"""
بروفايل مزود الخدمة (فندق / شركة سياحية / إلخ). مربوط بـ user_id
(مش email) عشان العلاقة تفضل صحيحة حتى لو اليوزر غيّر إيميله.

الحقول هنا مبنية على أساس شاشة الـ Dashboard اللي شفناها بالظبط:
- verified / trust badge ("تم توثيق حسابك بنجاح")
- checklist بتاع "طلبات التحقق" (تأكيد هاتف / سجل تجاري / صور 360 / حساب بنكي)
- KPIs (revenue, rating, bookings, views) بيتحسبوا من جداول تانية
  (Booking, Review) مش مخزنين هنا كـ snapshot، عشان يفضلوا live.

latitude/longitude: مضافين يدويًا دلوقتي (المزود بيدخلهم بنفسه أو
بيتحطوا يدويًا من الداتا بيز) عشان نقدر نعرض المكان على الخريطة.
مستقبلاً ممكن نستبدلها بـ geocoding تلقائي من العنوان/المدينة.
"""

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship

from app.db.session import Base


class BusinessType(str, enum.Enum):
    hotel = "hotel"
    restaurant = "restaurant"
    transport = "transport"
    tour_guide = "tour_guide"
    activity = "activity"
    other = "other"


class ProviderTier(str, enum.Enum):
    standard = "standard"
    elite = "elite"  # زي "Elite Provider" الظاهر في الصورة


class ProviderProfile(Base):
    __tablename__ = "provider_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)

    business_name = Column(String, nullable=False)       # "فندق النيل أسوان"
    business_name_en = Column(String, nullable=True)      # "Luxor Travels"
    business_type = Column(SAEnum(BusinessType), default=BusinessType.hotel)
    tier = Column(SAEnum(ProviderTier), default=ProviderTier.standard)

    city = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)

    # إحداثيات المكان - عشان نعرضه على الخريطة (Map.vue). لو فاضيين
    # (None) الفرونت بيعتبر إن المكان ده مش هيظهر كنقطة على الخريطة.
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    is_verified = Column(Boolean, default=False)

    # checklist بتاع التحقق - كل واحد بولياني بسيط زي ما هو ظاهر بالظبط
    phone_verified = Column(Boolean, default=False)
    commercial_registry_uploaded = Column(Boolean, default=False)
    photos_360_uploaded = Column(Boolean, default=False)
    bank_account_verified = Column(Boolean, default=False)

    description = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="provider_profile")
    services = relationship("Service", back_populates="provider", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="provider", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="provider", cascade="all, delete-orphan")