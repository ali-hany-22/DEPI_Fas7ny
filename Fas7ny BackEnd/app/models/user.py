"""
جدول المستخدمين الأساسي. كل يوزر في المنصة (سائح أو مزود خدمة أو أدمن)
بيبقى ليه صف هنا. الـ role هو اللي بيحدد نوع الصلاحيات.

استخدمنا role field في جدول واحد بدل جدول Providers منفصل مربوط
بالـ email، عشان:
1) الـ email ممكن يتغير، والربط بيه بيبقى هش.
2) الـ JWT auth بيتعامل مع جدول users واحد بشكل طبيعي (login
   بتاع السائح والمزود والأدمن كلهم بيمرّوا بنفس الـ endpoint).
"""

import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class UserRole(str, enum.Enum):
    tourist = "tourist"
    provider = "provider"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)

    role = Column(SAEnum(UserRole), default=UserRole.tourist, nullable=False)
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    # لو الـ role provider، هيبقى ليه صف واحد بس هنا (one-to-one)
    provider_profile = relationship(
        "ProviderProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # كل الحجوزات اللي العميل (تورست) عملها، بغض النظر عن المزود
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")