"""
Endpoints الداشبورد الرئيسية لمزود الخدمة. كل حاجة هنا محمية بـ
get_current_provider، يعني لازم JWT صالح لـ user role=provider.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_provider
from app.models.provider import ProviderProfile
from app.models.service import Service, ServiceStatus
from app.models.booking import Booking
from app.models.review import Review
from app.schemas.dashboard import (
    DashboardOut, KPIOut, ServiceOut, BookingOut, ReviewOut,
    VerificationChecklistOut,
)
from app.schemas.booking import BookingStatusUpdateRequest
from app.services.dashboard_service import compute_kpis

router = APIRouter(prefix="/provider/dashboard", tags=["Provider Dashboard"])


@router.get("", response_model=DashboardOut)
def get_dashboard(
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    """نداء واحد بيرجع كل حاجة شاشة الداشبورد محتاجاها."""
    kpis = compute_kpis(db, provider.id)

    services = (
        db.query(Service)
        .filter(Service.provider_id == provider.id)
        .order_by(Service.created_at.desc())
        .all()
    )

    recent_bookings = (
        db.query(Booking)
        .filter(Booking.provider_id == provider.id)
        .order_by(Booking.created_at.desc())
        .limit(10)
        .all()
    )

    recent_reviews = (
        db.query(Review)
        .filter(Review.provider_id == provider.id)
        .order_by(Review.created_at.desc())
        .limit(10)
        .all()
    )

    return DashboardOut(
        business_name=provider.business_name,
        business_name_en=provider.business_name_en,
        tier=provider.tier.value,
        kpis=KPIOut(**kpis),
        services=[ServiceOut.model_validate(s) for s in services],
        recent_bookings=[
            BookingOut(
                id=b.id,
                customer_name=b.guest_name,
                service_title=b.service.title if b.service else "",
                booking_date=b.created_at,
                amount=b.amount,
                status=b.status,
            )
            for b in recent_bookings
        ],
        recent_reviews=[ReviewOut.model_validate(r) for r in recent_reviews],
        verification=VerificationChecklistOut(
            is_verified=provider.is_verified,
            phone_verified=provider.phone_verified,
            commercial_registry_uploaded=provider.commercial_registry_uploaded,
            photos_360_uploaded=provider.photos_360_uploaded,
            bank_account_verified=provider.bank_account_verified,
        ),
    )


@router.patch("/services/{service_id}/toggle-status", response_model=ServiceOut)
def toggle_service_status(
    service_id: int,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    """زرار 'تعطيل/تفعيل' الظاهر جنب كل خدمة."""
    service = (
        db.query(Service)
        .filter(Service.id == service_id, Service.provider_id == provider.id)
        .first()
    )
    if not service:
        raise HTTPException(status_code=404, detail="الخدمة غير موجودة")

    service.status = (
        ServiceStatus.disabled if service.status == ServiceStatus.active else ServiceStatus.active
    )
    db.commit()
    db.refresh(service)
    return service


@router.get("/bookings", response_model=list[BookingOut])
def list_all_bookings(
    status_filter: str | None = None,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    """
    قايمة الحجوزات الكاملة لصفحة Bookings (مش الملخص بس).
    status_filter اختياري: confirmed / pending / completed / cancelled
    """
    query = db.query(Booking).filter(Booking.provider_id == provider.id)
    if status_filter:
        query = query.filter(Booking.status == status_filter)

    bookings = query.order_by(Booking.created_at.desc()).all()
    return [
        BookingOut(
            id=b.id,
            customer_name=b.customer_name,
            service_title=b.service.title if b.service else "",
            booking_date=b.created_at,
            amount=b.amount,
            status=b.status,
        )
        for b in bookings
    ]


@router.patch("/bookings/{booking_id}/status", response_model=BookingOut)
def update_booking_status(
    booking_id: int,
    payload: BookingStatusUpdateRequest,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    """تغيير حالة حجز (مؤكد / قيد الانتظار / تم الإكمال / ملغي)."""
    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id, Booking.provider_id == provider.id)
        .first()
    )
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")

    booking.status = payload.status
    db.commit()
    db.refresh(booking)

    return BookingOut(
        id=booking.id,
        customer_name=booking.customer_name,
        service_title=booking.service.title if booking.service else "",
        booking_date=booking.created_at,
        amount=booking.price_snapshot,
        status=booking.status,
    )
