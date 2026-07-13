"""
Schemas مخرجات الداشبورد - مبنية بالظبط على الحقول الظاهرة في
تصميم الصفحة (KPIs، الخدمات، الحجوزات، التقييمات، checklist التحقق).
"""

from datetime import datetime

from pydantic import BaseModel

from app.models.service import ServiceStatus
from app.models.booking import BookingStatus


class KPIOut(BaseModel):
    revenue: float              # الإيرادات (ج.م)
    revenue_change_pct: float   # +21%
    rating: float                # التقييم العام
    rating_change_pct: float
    bookings_count: int          # الحجوزات
    bookings_change_pct: float
    views: int                   # المشاهدات
    views_change_pct: float


class ServiceOut(BaseModel):
    id: int
    title: str
    image_url: str | None
    status: ServiceStatus
    requires_confirmation: bool
    bookings_this_month: int
    price: float

    class Config:
        from_attributes = True


class BookingOut(BaseModel):
    id: int
    customer_name: str
    service_title: str
    booking_date: datetime
    amount: float
    status: BookingStatus

    class Config:
        from_attributes = True


class ReviewOut(BaseModel):
    id: int
    customer_name: str
    rating: float
    title: str | None
    comment: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class VerificationChecklistOut(BaseModel):
    is_verified: bool
    phone_verified: bool
    commercial_registry_uploaded: bool
    photos_360_uploaded: bool
    bank_account_verified: bool


class DashboardOut(BaseModel):
    """الرد الكامل اللي شاشة الداشبورد بتحتاجه في نداء واحد."""
    business_name: str
    business_name_en: str | None
    tier: str
    kpis: KPIOut
    services: list[ServiceOut]
    recent_bookings: list[BookingOut]
    recent_reviews: list[ReviewOut]
    verification: VerificationChecklistOut
