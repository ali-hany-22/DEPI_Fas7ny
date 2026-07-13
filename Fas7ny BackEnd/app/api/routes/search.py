"""
app/api/routes/search.py

Endpoint حقيقي للبحث عن مكان بالاسم (زي فندق أو مطعم). بيدور بترتيب:

  1) الخدمات المسجلة داخليًا عندنا في النظام (Providers الحقيقيين
     اللي عندهم Dashboard وService مسجل - زي "Sama Alarish Hotel").
     لو لقى تطابق هنا، بيرجعه فورًا من غير أي طلب شبكة.

  2) لو مفيش تطابق داخلي، بيرجع للسلوك القديم: يدور في الكاش الدائم،
     وبعدين لايف عبر Nominatim (وOverpass كـ fallback) من خلال
     search_place() الموجودة في places_service.py، وبعد كده بيخزّنه
     تلقائيًا في الكاش عشان أي بحث تاني لنفس المكان يرجع فورًا من
     غير طلب شبكة جديد.

الفرق عن /places/cached:
  - /places/cached: بيقرا بس من الكاش، لو مش موجود بيرجع فاضي.
  - /search/place (هنا): بيدور داخليًا، وبعدين لايف لو محتاج.

استخدام من الفرونت (صفحة السيرش):
  GET /search/place?name=Royal House Hotel&city=العريش
"""

import logging

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.services.places_service import search_place
from app.services.provider_service import search_internal_services
from app.db.session import get_db

logger = logging.getLogger("search_routes")

router = APIRouter(prefix="/search", tags=["search"])


def _serialize_internal_service(service) -> dict:
    """
    بتحوّل Service + provider المرتبط بيه لنفس الشكل اللي الفرونت
    متوقعه من place.model_dump() (نفس الحقول اللي normalizeHotel في
    Search.vue بتقرا منها: name, price, image, amenities...).
    """
    provider = service.provider
    return {
        "id": service.id,
        "name": provider.business_name,
        "address": provider.city or "",
        "category": provider.business_type.value if provider.business_type else "hotel",
        "rating": 0,
        "review_count": 0,
        "price": service.price,
        "image": service.image_url,
        "tags": [],
        "amenities": {"wifi": False, "parking": False, "view": False},
        "lat": provider.latitude,
        "lng": provider.longitude,
    }


@router.get("/place")
def search_place_endpoint(
    name: str = Query(..., description="اسم المكان اللي المستخدم كاتبه في صندوق البحث"),
    city: str | None = Query(
        default=None,
        description="اسم المدينة (لو معروف) - بيحسّن دقة البحث كتير",
    ),
    category: str | None = Query(
        default=None,
        description="فئة المكان لو معروفة (hotels, restaurants...) - بتستخدم بس لو "
                     "البحث بالاسم فشل تمامًا، عشان نجيب بديل منطقي من نفس الفئة",
    ),
    db: Session = Depends(get_db),
):
    """
    بتدور على مكان واحد بالاسم بالترتيب ده:

      1) الخدمات المسجلة داخليًا عندنا (Providers الحقيقيين) - لو
         لقى تطابق، بيرجعه فورًا من غير أي طلب شبكة.
      2) لو مفيش تطابق داخلي: الكاش الدائم، وبعدين لايف من Nominatim
         (وOverpass كـ fallback أخير)، وتخزينه تلقائيًا لو نجح.

    بترجع "found": false لو مفيش أي نتيجة اتلاقت خالص (حتى بعد كل
    المحاولات)، بدل ما ترمي 404 - عشان الفرونت يقدر يعرض رسالة "لا
    توجد نتائج" بسهولة من غير error handling إضافي.
    """
    internal_match = search_internal_services(db=db, name=name, city=city)
    if internal_match is not None:
        logger.info("Internal provider match for name=%s city=%s", name, city)
        return {
            "found": True,
            "result": _serialize_internal_service(internal_match),
            "source": "internal",
        }

    place = search_place(place_name=name, city=city, category=category)

    if place is None:
        logger.info("Live search found nothing for name=%s city=%s", name, city)
        return {"found": False, "result": None}

    return {"found": True, "result": place.model_dump(), "source": "external"}