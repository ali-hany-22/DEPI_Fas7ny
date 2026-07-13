"""
app/api/routes/cached_places.py

Endpoint للقراءة فقط (read-only) من الكاش الدائم بتاع الأماكن
(persistent_cache.py). الهدف: أي جزء تاني في البروجيكت (شات بوت،
ميزة بحث/ترشيح في الموقع) يقدر يعرض أماكن حقيقية اتخزنت مسبقًا من
غير ما يستهلك أي كوتة Gemini/Nominatim/Overpass جديدة.

مهم: الـ endpoint ده مبينداش Gemini ولا Nominatim ولا Overpass أبدًا -
بيقرا بس من الملف المحلي اللي persistent_cache.py بيديره. لو الكاش
فاضي لمدينة معينة (لسه محدش عمل رحلة ليها قبل كده)، هيرجع list فاضية
بدل ما يحاول يجيب بيانات جديدة.
"""

import logging

from fastapi import APIRouter, Query

from app.services.persistent_cache import list_all_entries

logger = logging.getLogger("cached_places_routes")

router = APIRouter(prefix="/places", tags=["cached-places"])


@router.get("/cached")
def get_cached_places(
    city: str | None = Query(
        default=None,
        description="فلترة بالمدينة (بحث جزئي، غير حساس لحالة الأحرف). مثال: 'Cairo' أو 'بني سويف'",
    ),
    category: str | None = Query(
        default=None,
        description="فلترة بالفئة، مثال: hotels, restaurants, museums, place (للأماكن المفردة المخزّنة بالاسم)",
    ),
    search: str | None = Query(
        default=None,
        description="بحث نصي في اسم المكان (بحث جزئي، غير حساس لحالة الأحرف) - مفيدة للشات بوت",
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=500,
        description="أقصى عدد نتائج ترجع (افتراضي 50)",
    ),
):
    """
    بترجع الأماكن المخزّنة في الكاش الدائم، مع فلاتر اختيارية.

    أمثلة استخدام:
      GET /places/cached?city=Cairo
      GET /places/cached?category=restaurants
      GET /places/cached?search=كبابجي
      GET /places/cached?city=Cairo&category=hotels&limit=10
    """
    entries = list_all_entries(city=city, category=category)

    if search:
        search_lower = search.strip().lower()
        entries = [
            e for e in entries
            if search_lower in (e.get("name") or "").lower()
        ]

    total_found = len(entries)
    entries = entries[:limit]

    logger.info(
        "Cached places query | city=%s category=%s search=%s -> %d/%d results",
        city, category, search, len(entries), total_found,
    )

    return {
        "count": len(entries),
        "total_available": total_found,
        "results": entries,
    }


@router.get("/cached/cities")
def get_cached_cities():
    """
    بترجع قائمة بكل أسماء المدن الموجودة فعليًا في الكاش دلوقتي (مفيدة
    لعرض "المدن المتاحة بدون AI" في الفرونت، أو كـ autocomplete).
    """
    entries = list_all_entries()
    cities = sorted({e["_cache_city"] for e in entries if e.get("_cache_city")})
    return {"count": len(cities), "cities": cities}

"""
app/api/routes/cached_places.py (إضافة على نفس الملف)

/places/combined: بترجع الأماكن الخارجية (من persistent_cache، زي
/places/cached بالظبط) + الأماكن الداخلية (Providers المسجلين
فعليًا عندنا في النظام) مع بعض في list واحدة موحّدة الشكل، عشان
Map.vue تقدر تعرض الاتنين كنقط على نفس الخريطة من طلب واحد.

كل عنصر برجع بنفس الشكل (name, lat, lng, category, source...) بغض
النظر عن مصدره، والفرونت يقدر يميّز المصدر لو حابب من خلال "source".
"""

import logging

from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session

from app.services.persistent_cache import list_all_entries
from app.services.provider_service import get_services_by_city
from app.db.session import get_db

logger = logging.getLogger("cached_places_routes")

router = APIRouter(prefix="/places", tags=["cached-places"])


def _serialize_internal(service) -> dict:
    """توحيد شكل الـ Service/Provider الداخلي مع شكل الكاش الخارجي."""
    provider = service.provider
    return {
        "id": f"internal-{service.id}",
        "name": provider.business_name,
        "category": provider.business_type.value if provider.business_type else "hotel",
        "city": provider.city,
        "lat": provider.latitude,
        "lng": provider.longitude,
        "price": service.price,
        "image": service.image_url,
        "rating": 0,
        "source": "internal",
    }


@router.get("/combined")
def get_combined_places(
    city: str = Query(..., description="اسم المدينة - مطلوب عشان نجيب أماكن داخلية وخارجية ليها"),
    category: str | None = Query(default=None, description="فلترة بالفئة (hotels, restaurants...)"),
    limit: int = Query(default=50, ge=1, le=500),
    db: Session = Depends(get_db),
):
    """
    بترجع الأماكن الخارجية (كاش) + الداخلية (Providers مسجلين) مع
    بعض لمدينة معينة، عشان تُستخدم مباشرة في عرض الخريطة (Map.vue).

    الأماكن الداخلية اللي معندهاش lat/lng (لسه متسجلتش إحداثياتها)
    بتتستبعد من النتيجة، عشان منحطش marker في مكان غلط أو فاضي.
    """
    external_entries = list_all_entries(city=city, category=category)
    for e in external_entries:
        e["source"] = "external"
    external_entries = external_entries[:limit]

    internal_services = get_services_by_city(db=db, city=city, category=category)
    internal_entries = [
        _serialize_internal(s) for s in internal_services
        if s.provider.latitude is not None and s.provider.longitude is not None
    ]

    combined = external_entries + internal_entries

    logger.info(
        "Combined places query | city=%s category=%s -> external=%d internal=%d",
        city, category, len(external_entries), len(internal_entries),
    )

    return {"count": len(combined), "results": combined}