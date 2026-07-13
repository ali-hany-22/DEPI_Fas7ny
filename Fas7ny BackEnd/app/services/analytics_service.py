"""
منطق حساب صفحة Analytics: اتجاه الإيرادات آخر 6 شهور، وأفضل
الخدمات حسب الإيراد.
"""

from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.service import Service
from app.models.review import Review
from app.services.dashboard_service import month_bounds


def get_monthly_trend(db: Session, provider_id: int, months: int = 6) -> list[dict]:
    now = datetime.utcnow()
    result = []

    for i in range(months - 1, -1, -1):
        start, end = month_bounds(now, i)
        revenue = (
            db.query(func.coalesce(func.sum(Booking.price_snapshot), 0.0))
            .filter(
                Booking.provider_id == provider_id,
                Booking.created_at >= start,
                Booking.created_at < end,
                Booking.status != BookingStatus.cancelled,
            )
            .scalar()
        )
        count = (
            db.query(func.count(Booking.id))
            .filter(
                Booking.provider_id == provider_id,
                Booking.created_at >= start,
                Booking.created_at < end,
            )
            .scalar()
        )
        result.append({
            "month": start.strftime("%Y-%m"),
            "revenue": float(revenue or 0),
            "bookings_count": count or 0,
        })

    return result


def get_top_services(db: Session, provider_id: int, limit: int = 5) -> list[dict]:
    rows = (
        db.query(
            Service.title,
            func.count(Booking.id).label("bookings_count"),
            func.coalesce(func.sum(Booking.price_snapshot), 0.0).label("revenue"),
        )
        .join(Booking, Booking.service_id == Service.id)
        .filter(
            Service.provider_id == provider_id,
            Booking.status != BookingStatus.cancelled,
        )
        .group_by(Service.id)
        .order_by(func.sum(Booking.price_snapshot).desc())
        .limit(limit)
        .all()
    )
    return [
        {"service_title": r.title, "bookings_count": r.bookings_count, "revenue": float(r.revenue)}
        for r in rows
    ]


def get_reviews_summary(db: Session, provider_id: int) -> dict:
    total = db.query(func.count(Review.id)).filter(Review.provider_id == provider_id).scalar() or 0
    avg = (
        db.query(func.coalesce(func.avg(Review.rating), 0.0))
        .filter(Review.provider_id == provider_id)
        .scalar()
    )
    return {"total_reviews": total, "average_rating": round(float(avg or 0), 1)}
