"""
app/models/booking.py

حجز وهمي (مفيش بوابة دفع حقيقية دلوقتي) - الهدف إن أي حجز يتعمل من
صفحة الـ checkout يظهر فورًا في:
  1) "الحجوزات الأخيرة" و KPIs في داشبورد المزوّد (Provider Dashboard)
  2) صفحة "رحلاتي" بتاعة العميل (لو موجودة)

booking_reference: كود قصير يتعرض للعميل كـ "رقم الحجز" (زي
"FSH-8X2K9Q") بدل ما نعرضله الـ id الرقمي الداخلي مباشرة.
"""

import enum
import secrets
import string
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum as SAEnum, ForeignKey, Float, Date
from sqlalchemy.orm import relationship

from app.db.session import Base


class BookingStatus(str, enum.Enum):
    pending = "pending"        # "قيد الانتظار" - لسه محتاج تأكيد من المزود
    confirmed = "confirmed"    # "مؤكد"
    cancelled = "cancelled"    # "ملغي"
    completed = "completed"    # "منتهي" (بعد تاريخ المغادرة)


def generate_booking_reference() -> str:
    """كود حجز قصير قابل للقراءة زي FSH-8X2K9Q، مش UUID طويل."""
    chars = string.ascii_uppercase + string.digits
    suffix = "".join(secrets.choice(chars) for _ in range(6))
    return f"FSH-{suffix}"


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_reference = Column(String, unique=True, index=True, default=generate_booking_reference)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("provider_profiles.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)

    # snapshot من بيانات الخدمة وقت الحجز - عشان لو المزود غيّر السعر
    # أو الاسم بعدين، سجل الحجز القديم يفضل زي ما كان وقتها بالظبط
    service_title_snapshot = Column(String, nullable=False)
    price_snapshot = Column(Float, nullable=False)

    guest_name = Column(String, nullable=False)
    guest_phone = Column(String, nullable=True)

    check_in_date = Column(Date, nullable=True)
    check_out_date = Column(Date, nullable=True)
    nights = Column(Integer, default=1)

    status = Column(SAEnum(BookingStatus), default=BookingStatus.pending)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="bookings")
    provider = relationship("ProviderProfile", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")