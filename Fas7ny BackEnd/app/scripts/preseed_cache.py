"""
preseed_cache.py

سكريبت مستقل تشغله يدوياً **مرة واحدة قبل أي demo أو تسليم للمشروع**،
بيملى الكاش الدائم (persistent_cache.py) ببيانات المدن المتوقع استخدامها
كتير (القاهرة، الإسكندرية، الغردقة، الأقصر، أسوان...).

الهدف: بدل ما تستنى Overpass وقت العرض الفعلي أمام الدكتور/اللجنة
(واللي ممكن ياخد وقت أو يفشل لو السيرفر مزدحم في اللحظة دي)، تشغل
السكريبت ده الليلة اللي قبل العرض، وكل البيانات هتبقى جاهزة فوراً
من الكاش وقت الحاجة.

طريقة التشغيل (من مجلد المشروع الرئيسي):
    python -m app.scripts.preseed_cache

أو لو مش حابب تستخدمه كـ module:
    python app/scripts/preseed_cache.py
    (لازم تشغله وانت واقف في مجلد Trip_Planner نفسه عشان الـ imports تشتغل)
"""

import logging
import sys
import time

# لو شغلته مباشرة كملف (مش كـ module)، نضيف مسار المشروع لـ sys.path
if __name__ == "__main__":
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.persistent_cache import get_cached, set_cached
from app.services.hotel_service import get_hotels
from app.services.restaurants_service import get_restaurants
from app.services.cafe_service import get_cafes
from app.services.entertainment_service import get_entertainment
from app.services.shopping_service import get_shopping
from app.services.beach_service import get_beaches
from app.services.attraction_service import get_museums, get_parks

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("preseed_cache")

# المدن اللي متوقع تتكرر كتير في المشروع - عدّل اللستة دي حسب احتياجك
CITIES_TO_PRESEED = [
    "Cairo",
    "Giza",
    "Alexandria",
    "Hurghada",
    "Luxor",
    "Aswan",
    "Sharm El Sheikh",
]

CATEGORY_FETCHERS = {
    "hotels": get_hotels,
    "restaurants": get_restaurants,
    "cafes": get_cafes,
    "entertainment": get_entertainment,
    "shopping": get_shopping,
    "museums": get_museums,
    "parks": get_parks,
    "beaches": get_beaches,
}

# تأخير بين كل طلب فعلي والتاني (بالثواني) عشان منضربش rate limit
DELAY_BETWEEN_REQUESTS = 2.0


def preseed_city(city: str):
    logger.info("=" * 60)
    logger.info("Pre-seeding city: %s", city)
    logger.info("=" * 60)

    for label, fn in CATEGORY_FETCHERS.items():
        cached = get_cached(city, label)

        if cached is not None:
            logger.info("  [SKIP] %s already cached (%d items)", label, len(cached))
            continue

        logger.info("  [FETCH] %s ...", label)

        try:
            result = fn(city)
            data = [item.model_dump() for item in result]
            set_cached(city, label, data)
            logger.info("  [OK] %s -> %d items cached", label, len(data))
        except Exception as e:
            logger.error("  [FAIL] %s -> %s", label, str(e))
            # بنخزن list فاضية عشان منحاولش تاني بلا داعي في نفس الجلسة
            set_cached(city, label, [])

        time.sleep(DELAY_BETWEEN_REQUESTS)


def main():
    logger.info("Starting pre-seed for %d cities: %s", len(CITIES_TO_PRESEED), ", ".join(CITIES_TO_PRESEED))

    for city in CITIES_TO_PRESEED:
        preseed_city(city)

    logger.info("Pre-seeding complete for all cities.")


if __name__ == "__main__":
    main()