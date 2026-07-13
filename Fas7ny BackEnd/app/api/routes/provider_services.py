"""
صفحة "My Services" - إدارة كاملة (إنشاء / عرض / تعديل / حذف)
لخدمات المزود. الـ toggle-status الموجود في provider_dashboard.py
اتسيب زي ما هو (بيتنادى من كارت الداشبورد)، والراوتر ده بيغطي
باقي العمليات.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_provider
from app.models.provider import ProviderProfile
from app.models.service import Service
from app.models.booking import Booking
from app.schemas.service import ServiceCreateRequest, ServiceUpdateRequest, ServiceDetailOut

router = APIRouter(prefix="/provider/services", tags=["Provider Services"])


@router.get("", response_model=list[ServiceDetailOut])
def list_services(
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    return (
        db.query(Service)
        .filter(Service.provider_id == provider.id)
        .order_by(Service.created_at.desc())
        .all()
    )


@router.post("", response_model=ServiceDetailOut, status_code=201)
def create_service(
    payload: ServiceCreateRequest,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    service = Service(provider_id=provider.id, **payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def _get_owned_service(service_id: int, provider: ProviderProfile, db: Session) -> Service:
    service = (
        db.query(Service)
        .filter(Service.id == service_id, Service.provider_id == provider.id)
        .first()
    )
    if not service:
        raise HTTPException(status_code=404, detail="الخدمة غير موجودة")
    return service


@router.get("/{service_id}", response_model=ServiceDetailOut)
def get_service(
    service_id: int,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    return _get_owned_service(service_id, provider, db)


@router.patch("/{service_id}", response_model=ServiceDetailOut)
def update_service(
    service_id: int,
    payload: ServiceUpdateRequest,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    service = _get_owned_service(service_id, provider, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service


@router.delete("/{service_id}", status_code=204)
def delete_service(
    service_id: int,
    provider: ProviderProfile = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    service = _get_owned_service(service_id, provider, db)

    has_bookings = (
        db.query(Booking).filter(Booking.service_id == service.id).first() is not None
    )
    if has_bookings:
        # منمنعش الحذف عشان مفيش حاجة تمسح تاريخ حجوزات حقيقي (فاتورة/تقرير).
        # الحل الصح: تعطيل الخدمة (status=disabled) بدل حذفها.
        raise HTTPException(
            status_code=409,
            detail="لا يمكن حذف خدمة لها حجوزات سابقة. عطّل الخدمة بدلاً من ذلك.",
        )

    db.delete(service)
    db.commit()
    return None
