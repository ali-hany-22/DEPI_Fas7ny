from pydantic import BaseModel


class MonthlyPoint(BaseModel):
    month: str          # "2026-06"
    revenue: float
    bookings_count: int


class ServiceBreakdown(BaseModel):
    service_title: str
    bookings_count: int
    revenue: float


class AnalyticsOut(BaseModel):
    monthly_trend: list[MonthlyPoint]     # آخر 6 شهور
    top_services: list[ServiceBreakdown]  # أفضل الخدمات حسب الإيراد
    total_reviews: int
    average_rating: float
