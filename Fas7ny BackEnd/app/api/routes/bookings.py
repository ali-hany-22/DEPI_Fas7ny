"""
app/api/routes/bookings.py

Endpoint لإنشاء حجز وهمي (مفيش بوابة دفع فعلية دلوقتي). العميل لازم
يكون مسجّل دخول (tourist) عشان يقدر يحجز. الحجز بيتربط تلقائيًا
بالـ Service والـ ProviderProfile بتاعته، فيظهر فورًا في داشبورد
المزود (Bookings tab + KPIs).

استخدام من الفرونت (صفحة الـ checkout):
  POST /bookings
  body: { service_id, guest_name, guest_phone, check_in_date, check_out_date, nights }
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.booking import Booking
from app.models.service import Service
from app.models.user import User
from app.schemas.booking import BookingCreate, BookingOut
from app.dependencies.auth import get_current_user  # عدّل الاسم لو ملف الـ dependencies عندك اسمه مختلف

logger = logging.getLogger("bookings_routes")

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingOut, status_code=status.HTTP_201_CREATED)
def create_booking(
    payload: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    بتنشئ حجز وهمي جديد. بتاخد snapshot من عنوان وسعر الخدمة وقت
    الحجز، عشان لو المزود غيّرهم بعدين، سجل الحجز القديم يفضل زي
    ما كان بالظبط.
    """
    service = db.query(Service).filter(Service.id == payload.service_id).first()
    if service is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="الخدمة غير موجودة")

    booking = Booking(
        user_id=current_user.id,
        provider_id=service.provider_id,
        service_id=service.id,
        service_title_snapshot=service.title,
        price_snapshot=service.price,
        guest_name=payload.guest_name,
        guest_phone=payload.guest_phone,
        check_in_date=payload.check_in_date,
        check_out_date=payload.check_out_date,
        nights=payload.nights,
    )

    db.add(booking)

    # تحديث عداد "الحجوزات هذا الشهر" اللي ظاهر في كارت الخدمة بالداشبورد
    service.bookings_this_month = (service.bookings_this_month or 0) + 1

    db.commit()
    db.refresh(booking)

    logger.info(
        "New booking created | ref=%s user_id=%s service_id=%s",
        booking.booking_reference, current_user.id, service.id,
    )

    return booking


@router.get("/{booking_reference}", response_model=BookingOut)
def get_booking(
    booking_reference: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    بترجع تفاصيل حجز واحد بالـ reference بتاعه - مستخدمة في صفحة
    تأكيد الحجز (booking confirmation) عشان تعرض التفاصيل بعد ما
    المستخدم يتحوّل من صفحة الـ checkout.
    """
    booking = (
        db.query(Booking)
        .filter(Booking.booking_reference == booking_reference)
        .filter(Booking.user_id == current_user.id)
        .first()
    )
    if booking is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="الحجز غير موجود")

    return booking