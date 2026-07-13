"""
Endpoint عام (بدون auth) بينادى من صفحة عرض الخدمة اللي بيشوفها
السائح، عشان نسجل زيارة حقيقية في جدول page_views. مش تحت
/provider عشان مش محتاج JWT provider.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.page_view import PageView
from app.models.service import Service

router = APIRouter(prefix="/public", tags=["Public Tracking"])


@router.post("/services/{service_id}/track-view", status_code=204)
def track_service_view(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="الخدمة غير موجودة")

    db.add(PageView(provider_id=service.provider_id, service_id=service.id))
    db.commit()
    return None
