"""
منطق حساب أرقام الداشبورد. النسب المئوية (+21%, +5.2%...) بتتحسب
بمقارنة الشهر الحالي بالشهر اللي قبله - مفيش حاجة hardcoded.
"""

from datetime import datetime, timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.booking import Booking, BookingStatus
from app.models.review import Review
from app.models.provider import ProviderProfile
from app.models.page_view import PageView


def month_bounds(reference: datetime, months_back: int = 0):
    """يرجع بداية ونهاية الشهر (reference - months_back شهور)."""
    year = reference.year
    month = reference.month - months_back
    while month <= 0:
        month += 12
        year -= 1
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    return start, end


def _pct_change(current: float, previous: float) -> float:
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    return round(((current - previous) / previous) * 100, 1)


def compute_kpis(db: Session, provider_id: int) -> dict:
    now = datetime.utcnow()
    this_start, this_end = month_bounds(now, 0)
    last_start, last_end = month_bounds(now, 1)

    def revenue_in(start, end):
        result = (
            db.query(func.coalesce(func.sum(Booking.price_snapshot), 0.0))
            .filter(
                Booking.provider_id == provider_id,
                Booking.created_at >= start,
                Booking.created_at < end,
                Booking.status != BookingStatus.cancelled,
            )
            .scalar()
        )
        return float(result or 0)

    def bookings_count_in(start, end):
        return (
            db.query(func.count(Booking.id))
            .filter(
                Booking.provider_id == provider_id,
                Booking.created_at >= start,
                Booking.created_at < end,
            )
            .scalar()
        ) or 0

    revenue_this = revenue_in(this_start, this_end)
    revenue_last = revenue_in(last_start, last_end)

    bookings_this = bookings_count_in(this_start, this_end)
    bookings_last = bookings_count_in(last_start, last_end)

    avg_rating = (
        db.query(func.coalesce(func.avg(Review.rating), 0.0))
        .filter(Review.provider_id == provider_id)
        .scalar()
    )
    avg_rating = round(float(avg_rating or 0), 1)

    avg_rating_last_month = (
        db.query(func.coalesce(func.avg(Review.rating), 0.0))
        .filter(
            Review.provider_id == provider_id,
            Review.created_at < this_start,
        )
        .scalar()
    )
    avg_rating_last_month = round(float(avg_rating_last_month or avg_rating), 1)

    def views_in(start, end):
        return (
            db.query(func.count(PageView.id))
            .filter(
                PageView.provider_id == provider_id,
                PageView.viewed_at >= start,
                PageView.viewed_at < end,
            )
            .scalar()
        ) or 0

    views_this = views_in(this_start, this_end)
    views_last = views_in(last_start, last_end)

    return {
        "revenue": revenue_this,
        "revenue_change_pct": _pct_change(revenue_this, revenue_last),
        "rating": avg_rating,
        "rating_change_pct": _pct_change(avg_rating, avg_rating_last_month),
        "bookings_count": bookings_this,
        "bookings_change_pct": _pct_change(bookings_this, bookings_last),
        "views": views_this,
        "views_change_pct": _pct_change(views_this, views_last),
    }
