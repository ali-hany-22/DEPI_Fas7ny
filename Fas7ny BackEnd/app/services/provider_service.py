"""
app/services/provider_service.py

ملاحظة مهمة: Service مفهاش عمود city ولا category مباشر - المدينة
والفئة (business_type) مخزنين في ProviderProfile. عشان كده أي فلترة
بالمدينة أو الفئة لازم تعمل join مع ProviderProfile الأول، وإلا
هيرمي AttributeError وقت التشغيل (Service.city مش موجود أصلاً).
"""

from sqlalchemy.orm import Session, joinedload

from app.models.service import Service, ServiceStatus
from app.models.provider import ProviderProfile


def get_services_by_city(
    db: Session,
    city: str,
    category: str | None = None,
):
    """
    بترجع كل الخدمات النشطة (status=active) بتاعة الـ Providers
    المسجلين في مدينة معينة. بتعمل join مع ProviderProfile عشان نقدر
    نفلتر بالـ city وbusiness_type (اللي مش موجودين في جدول Service
    نفسه).
    """
    query = (
        db.query(Service)
        .join(ProviderProfile, Service.provider_id == ProviderProfile.id)
        .options(joinedload(Service.provider))
        .filter(ProviderProfile.city.ilike(city))
        .filter(Service.status == ServiceStatus.active)
    )

    if category:
        query = query.filter(ProviderProfile.business_type == category)

    return query.all()


def search_internal_services(
    db: Session,
    name: str,
    city: str | None = None,
):
    """
    بيدور في الخدمات المسجلة داخليًا (Providers الحقيقيين عندنا في
    النظام) باسم المزود (business_name / business_name_en) أو اسم
    الخدمة نفسها (title). بيستخدم partial match (ilike) عشان "سما
    العريش" يلاقي "فندق سما العريش" حتى لو الاسم مكتوب جزئيًا.

    ده بيتنادى من /search/place قبل ما نلجأ للبحث الخارجي
    (Nominatim/Overpass)، عشان نديل أولوية للفنادق المسجلة فعليًا
    عندنا في النظام قبل أي مصدر خارجي.

    بترجع أول تطابق (Service واحد) أو None لو مفيش حاجة اتلاقت.
    """
    query = (
        db.query(Service)
        .join(ProviderProfile, Service.provider_id == ProviderProfile.id)
        .options(joinedload(Service.provider))
        .filter(Service.status == ServiceStatus.active)
        .filter(
            ProviderProfile.business_name.ilike(f"%{name}%")
            | ProviderProfile.business_name_en.ilike(f"%{name}%")
            | Service.title.ilike(f"%{name}%")
        )
    )

    if city:
        query = query.filter(ProviderProfile.city.ilike(city))

    return query.first()