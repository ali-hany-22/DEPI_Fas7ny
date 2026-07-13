"""صفحة Analytics."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_provider
from app.models.provider import ProviderProfile
from app.schemas.analytics import AnalyticsOut, MonthlyPoint, ServiceBreakdown
from app.services.analytics_service import get_monthly_trend, get_top_services, get_reviews_summary

router = APIRouter(prefix="/provider/analytics", tags=["Provider Analytics"])


@router.get("", response_model=AnalyticsOut)
def get_analytics(
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    trend = get_monthly_trend(db, provider.id)
    top = get_top_services(db, provider.id)
    reviews_summary = get_reviews_summary(db, provider.id)

    return AnalyticsOut(
        monthly_trend=[MonthlyPoint(**t) for t in trend],
        top_services=[ServiceBreakdown(**t) for t in top],
        total_reviews=reviews_summary["total_reviews"],
        average_rating=reviews_summary["average_rating"],
    )
