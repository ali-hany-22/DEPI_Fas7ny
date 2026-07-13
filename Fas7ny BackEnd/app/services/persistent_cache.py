"""
persistent_cache.py

كاش دائم (على القرص) لنتائج Google Places بتاعة الأماكن حسب المدينة/الفئة.
الهدف: أي مدينة اتطلبت مرة واحدة (زي القاهرة، الإسكندرية، الغردقة)، النتايج
بتاعتها بتتخزن في ملف JSON محلي، وأي طلب تاني لنفس المدينة/الفئة بياخد
من الملف مباشرة من غير ما ينادي Google خالص - حتى لو السيرفر اتقفل واتشغل
تاني، أو حتى لو الطلب جه من مستخدم مختلف تماماً.

ده بيقلل الاستهلاك الفعلي للـ Quota بشكل جذري، لأن معظم الرحلات هتكون
لمدن مشهورة (القاهرة، الإسكندرية، الغردقة، الأقصر...) هتتكرر كتير.

طريقة الاستخدام:
    from app.services.persistent_cache import get_cached, set_cached

    cached = get_cached("Cairo", "hotels")
    if cached is not None:
        return cached

    result = ... # نادي جوجل عادي
    set_cached("Cairo", "hotels", result)
"""

import json
import logging
import os
import threading
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger("persistent_cache")

# مكان ملف الكاش - جوه المشروع، ممكن تغيره لأي path تاني تفضله
CACHE_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "places_cache.json",
)

# مدة صلاحية الكاش بالأيام - بعدها بنعتبر البيانات قديمة ونطلبها تاني من جوجل
# (عشان لو مكان اتقفل أو تقييمه اتغير مع الوقت)
CACHE_TTL_DAYS = 30

# lock عشان لو فيه أكتر من thread بيكتب في نفس الوقت (لأننا شغالين بـ ThreadPoolExecutor)
_lock = threading.Lock()

# الكاش بيتحمل في الذاكرة مرة واحدة وقت أول استخدام، وبيتحدث لما نضيف حاجة جديدة
_memory_cache: dict[str, Any] | None = None


def _ensure_cache_dir():
    os.makedirs(os.path.dirname(CACHE_FILE_PATH), exist_ok=True)


def _load_cache_from_disk() -> dict:
    _ensure_cache_dir()

    if not os.path.exists(CACHE_FILE_PATH):
        return {}

    try:
        with open(CACHE_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        logger.error("Failed to load persistent cache file | error=%s", str(e))
        return {}


def _save_cache_to_disk(cache: dict):
    _ensure_cache_dir()

    try:
        # بنكتب في ملف مؤقت الأول وبعدين نستبدل، عشان لو الكتابة اتقطعت
        # (زي إقفال السيرفر فجأة) الملف الأصلي ميتبهدلش
        tmp_path = CACHE_FILE_PATH + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, CACHE_FILE_PATH)
    except OSError as e:
        logger.error("Failed to save persistent cache file | error=%s", str(e))


def _get_memory_cache() -> dict:
    global _memory_cache
    if _memory_cache is None:
        with _lock:
            if _memory_cache is None:  # double-check جوه الـ lock
                _memory_cache = _load_cache_from_disk()
    return _memory_cache


def _make_key(city: str, category: str) -> str:
    return f"{city.strip().lower()}::{category.strip().lower()}"


def get_cached(city: str, category: str) -> list | None:
    """
    بترجع النتائج المخزّنة لو موجودة ومش قديمة (أقدم من CACHE_TTL_DAYS).
    بترجع None لو مفيش كاش أو الكاش قديم، وده معناه لازم تنادي جوجل عادي.
    """
    cache = _get_memory_cache()
    key = _make_key(city, category)

    entry = cache.get(key)
    if entry is None:
        return None

    try:
        cached_at = datetime.fromisoformat(entry["cached_at"])
    except (KeyError, ValueError):
        return None

    if datetime.now() - cached_at > timedelta(days=CACHE_TTL_DAYS):
        logger.info("Persistent cache EXPIRED for %s", key)
        return None

    logger.info("Persistent cache HIT for %s", key)
    return entry["data"]


def set_cached(city: str, category: str, data: list):
    """
    بتخزن النتائج على القرص عشان أي request تاني (حتى بعد إعادة تشغيل
    السيرفر) يلاقيها جاهزة من غير ما ينادي جوجل تاني.
    """
    key = _make_key(city, category)

    with _lock:
        cache = _get_memory_cache()
        cache[key] = {
            "cached_at": datetime.now().isoformat(),
            "data": data,
        }
        _save_cache_to_disk(cache)

    logger.info("Persistent cache SET for %s (%d items)", key, len(data) if data else 0)


def clear_cache():
    """مسح الكاش بالكامل - مفيدة وقت التطوير/التست بس."""
    global _memory_cache
    with _lock:
        _memory_cache = {}
        _save_cache_to_disk({})
    logger.info("Persistent cache cleared")


def list_all_entries(
    city: str | None = None,
    category: str | None = None,
    include_expired: bool = False,
) -> list[dict]:
    """
    بترجع كل الأماكن المخزّنة في الكاش كـ list مسطّح (flat)، بدل الشكل
    المفتاحي الداخلي (city::category -> {cached_at, data}).
 
    كل عنصر في الـ list الراجعة بيبقى dict فيه كل حقول Place العادية
    (name, city, rating, latitude, ...) بالإضافة لحقلين إضافيين:
      - "_cache_city": اسم المدينة زي ما اتخزن بيه في مفتاح الكاش
      - "_cache_category": اسم الفئة زي ما اتخزنت بيه في مفتاح الكاش
        (هتبقى "place" للأماكن المخزّنة من search_place بمفتاح
        "place::<name>"، أو اسم الفئة العادي زي "hotels"/"restaurants"
        للأماكن المخزّنة من search_places_by_category)
 
    الباراميترات:
      city: لو محدد، بيرجع بس الأماكن اللي city بتاعتها (جزء من مفتاح
            الكاش) بتطابق النص ده (case-insensitive, partial match)
      category: لو محدد، بيرجع بس الأماكن من الفئة دي
      include_expired: لو False (الافتراضي)، بيتجاهل أي entry أقدم من
            CACHE_TTL_DAYS بنفس منطق get_cached() بالظبط - عشان مانرجعش
            بيانات ممكن تكون عفا عليها الزمن للمستخدم النهائي
 
    الدالة دي read-only بالكامل - بتقرا من نفس _get_memory_cache()
    المستخدمة في get_cached()، ومبتعملش أي كتابة على القرص.
    """
    cache = _get_memory_cache()
    results: list[dict] = []
 
    city_filter = city.strip().lower() if city else None
    category_filter = category.strip().lower() if category else None
 
    for key, entry in cache.items():
        # مفتاح الكاش شكله "city::category" (زي "cairo::hotels" أو
        # "beni suef::place::مطعم أبو شامة" - لاحظ إن أسماء الأماكن
        # المفردة بتتخزن بمفتاح "place::<name>" فالفئة الفعلية بعد
        # الفصل الأول هتبقى "place")
        parts = key.split("::", 1)
        if len(parts) != 2:
            continue
        entry_city, entry_category = parts
 
        if city_filter and city_filter not in entry_city:
            continue
        if category_filter and category_filter != entry_category.split("::")[0]:
            continue
 
        if not include_expired:
            try:
                cached_at = datetime.fromisoformat(entry["cached_at"])
                if datetime.now() - cached_at > timedelta(days=CACHE_TTL_DAYS):
                    continue
            except (KeyError, ValueError):
                continue
 
        places = entry.get("data") or []
        for place in places:
            if not isinstance(place, dict):
                continue
            enriched_place = {
                **place,
                "_cache_city": entry_city,
                "_cache_category": entry_category,
            }
            results.append(enriched_place)
 
    return results
 