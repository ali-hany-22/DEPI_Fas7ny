import logging
import math
import re
from datetime import datetime, timedelta

import requests

from app.services.places_service import search_place
from app.services.weather_service import get_weather

logger = logging.getLogger("enrichment_service")

IGNORED_ACTIVITY_CATEGORIES = {
    "transport",
    "transportation",
    "travel",
    "flight",
    "internal flight",
    "internal_flight",
    "domestic flight",
    "drive",
    "train",
    "bus",
    "taxi",
    "uber",
    "metro",
    "subway",
    "ferry",
    "boat transfer",
    "car rental",
    "car_rental",
    "rental car",
}

# فئات "الأنشطة الرئيسية" اللي بتستاهل نداء Gemini إضافي لجلب rating/
# reviews تقديري. كانت مقصورة على attraction/museum/hotel بس عشان
# نتجنب كتر نداءات Gemini على مفتاح واحد فقط. دلوقتي بعد ما بقى عندنا
# 3 مصادر (GEMINI_API_KEY -> GEMINI_ALT_API_KEY -> GROQ_API_KEY) بترتيب
# تلقائي في GeminiPlaceService، بقى آمن نوسّع القائمة لتشمل shopping
# و restaurant كمان عشان كل الأنشطة تقريبًا تاخد rating/reviews حقيقية.
MAIN_ACTIVITY_CATEGORIES = {
    "attraction",
    "museum",
    "hotel",
    "shopping",
    "restaurant",
}

ROUTE_CATEGORIES = {
    "attraction",
    "museum",
    "park",
    "shopping",
    "beach",
    "activity",
}

# ---------------------------------------------------------------------------
# إعدادات حساب الوقت
# ---------------------------------------------------------------------------

# مدة افتراضية (دقايق) للأنشطة اللي معندهاش duration محدد، حسب الفئة.
DEFAULT_DURATION_MINUTES = {
    "attraction": 90,
    "museum": 120,
    "park": 60,
    "shopping": 90,
    "beach": 120,
    "activity": 60,
    "restaurant": 60,
    "cafe": 45,
    "hotel": 30,  # مجرد check-in/drop-off, مش إقامة كاملة
}
DEFAULT_DURATION_FALLBACK = 60

# متوسط سرعة افتراضية للتنقل بين نشاطين لهم إحداثيات (كم/ساعة) -
# تقدير محافظ لتنقل داخل المدينة (مشي + مواصلات + زحمة).
AVG_TRAVEL_SPEED_KMH = 20.0
MIN_TRAVEL_MINUTES = 10   # حتى لو المسافة صفر، افترض وقت تنقل/استعداد أدنى
MAX_TRAVEL_MINUTES = 60   # سقف معقول عشان مسافات غريبة متخربش اليوم كله

DAY_START_HOUR = 9  # الافتراضي لو مفيش أي وقت أصلي من Gemini نقدر نستنتج منه بداية اليوم

# OSRM public demo server - بيحسب وقت تنقل حقيقي (مش خط مستقيم) بناءً
# على شبكة الطرق الفعلية من OpenStreetMap. مجاني وبدون API key، بس فيه
# rate limits وممكن يبطأ أو يفشل تحت ضغط - عشان كده فيه fallback لـ
# Haversine estimate القديم لو الطلب فشل أو تأخر.
OSRM_BASE_URL = "https://router.project-osrm.org/route/v1/driving"
OSRM_TIMEOUT_SECONDS = 3


def _haversine_km(lat1, lon1, lat2, lon2) -> float:
    """مسافة تقريبية بالكيلومتر بين نقطتين جغرافيتين (Haversine formula)."""
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))


def _reorder_day_activities(activities: list[dict]) -> list[dict]:
    """
    بتعيد ترتيب الأنشطة داخل اليوم الواحد لتقليل التنقل الجغرافي،
    باستخدام nearest-neighbor على الأنشطة اللي في ROUTE_CATEGORIES وليها
    إحداثيات صالحة فقط.

    باقي الأنشطة (وجبات، أنشطة بلا إحداثيات، transport) بتفضل "ملتصقة"
    بأقرب نشاط route كان قبلها في الترتيب الأصلي، فمينفكش الترابط
    المنطقي (مطعم بعد نشاط معين) حتى بعد إعادة الترتيب الجغرافي.
    """
    route_indices = []
    coords_by_index: dict[int, tuple[float, float]] = {}

    for i, act in enumerate(activities):
        category = (act.get("category") or "").lower()
        details = act.get("place_details")

        if category in ROUTE_CATEGORIES and details:
            lat = details.get("latitude")
            lon = details.get("longitude")
            if lat is not None and lon is not None:
                route_indices.append(i)
                coords_by_index[i] = (lat, lon)

    if len(route_indices) < 2:
        return activities

    def _route_length(order: list[int]) -> float:
        total = 0.0
        for a, b in zip(order, order[1:]):
            lat1, lon1 = coords_by_index[a]
            lat2, lon2 = coords_by_index[b]
            total += _haversine_km(lat1, lon1, lat2, lon2)
        return total

    def _nearest_neighbor_from(start: int) -> list[int]:
        remaining = [i for i in route_indices if i != start]
        order = [start]
        while remaining:
            last_lat, last_lon = coords_by_index[order[-1]]
            nearest_idx = min(
                remaining,
                key=lambda i: _haversine_km(last_lat, last_lon, *coords_by_index[i]),
            )
            order.append(nearest_idx)
            remaining.remove(nearest_idx)
        return order

    best_order = min(
        (_nearest_neighbor_from(start) for start in route_indices),
        key=_route_length,
    )
    ordered_route = best_order

    attachments: dict[int, list[int]] = {idx: [] for idx in ordered_route}
    route_set = set(route_indices)
    last_seen_route_idx = None

    for i, act in enumerate(activities):
        if i in route_set:
            last_seen_route_idx = i
            continue
        anchor = last_seen_route_idx if last_seen_route_idx is not None else ordered_route[0]
        attachments[anchor].append(i)

    new_order: list[int] = []
    for route_idx in ordered_route:
        new_order.append(route_idx)
        new_order.extend(attachments[route_idx])

    return [activities[i] for i in new_order]


# ---------------------------------------------------------------------------
# الجزء المُصلح: حساب الأوقات فعليًا بدل إعادة توزيع القديمة
# ---------------------------------------------------------------------------

def _parse_time_to_minutes(t: str | None) -> int | None:
    """
    يحول time string زي '09:00 صباحاً' أو '06:30 PM' لعدد دقايق من نص
    الليل (0-1439). بيرجع None لو مقدرش يفهم الفورمات.
    """
    if not t:
        return None
    match = re.search(r"(\d{1,2}):(\d{2})", t)
    if not match:
        return None
    hour, minute = int(match.group(1)), int(match.group(2))
    is_pm = "مساء" in t or "pm" in t.lower()
    is_am = "صباح" in t or "am" in t.lower()
    if is_pm and hour != 12:
        hour += 12
    if is_am and hour == 12:
        hour = 0
    return hour * 60 + minute


def _minutes_to_time_str(total_minutes: int) -> str:
    """يحول عدد الدقايق لـ time string بصيغة 24 ساعة 'HH:MM'."""
    total_minutes = total_minutes % (24 * 60)
    hour, minute = divmod(total_minutes, 60)
    return f"{hour:02d}:{minute:02d}"


def _get_activity_duration_minutes(activity: dict) -> int:
    """
    بيرجع مدة النشاط بالدقايق. لو فيه duration صريح في البيانات
    (من Gemini أو مصدر تاني) بيستخدمه، وإلا بيرجع لقيمة افتراضية
    حسب الفئة.
    """
    explicit = activity.get("duration_minutes")
    if isinstance(explicit, (int, float)) and explicit > 0:
        return int(explicit)

    category = (activity.get("category") or "").lower()
    return DEFAULT_DURATION_MINUTES.get(category, DEFAULT_DURATION_FALLBACK)


def _haversine_travel_minutes(lat1, lon1, lat2, lon2) -> int:
    """تقدير وقت التنقل من خط مستقيم (Haversine) - الاستخدام الاحتياطي."""
    distance_km = _haversine_km(lat1, lon1, lat2, lon2)
    travel_minutes = (distance_km / AVG_TRAVEL_SPEED_KMH) * 60
    return int(max(MIN_TRAVEL_MINUTES, min(MAX_TRAVEL_MINUTES, travel_minutes)))


def _osrm_travel_minutes(lat1, lon1, lat2, lon2) -> int | None:
    """
    بيسأل OSRM public demo server عن وقت تنقل حقيقي (بالسيارة) بين
    نقطتين، بناءً على شبكة الطرق الفعلية مش خط مستقيم.

    بيرجع None لو الطلب فشل أو استغرق وقت أطول من OSRM_TIMEOUT_SECONDS،
    عشان الكود اللي بينادي الدالة يقدر يرجع لـ Haversine fallback.
    """
    try:
        url = f"{OSRM_BASE_URL}/{lon1},{lat1};{lon2},{lat2}"
        response = requests.get(
            url,
            params={"overview": "false"},
            timeout=OSRM_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        data = response.json()

        if data.get("code") != "Ok":
            return None

        duration_seconds = data["routes"][0]["duration"]
        return int(duration_seconds / 60)

    except Exception as e:
        logger.warning(
            "OSRM request failed, falling back to Haversine estimate | error=%s",
            str(e),
        )
        return None


def _get_travel_minutes(prev_activity: dict | None, activity: dict) -> int:
    """
    بيحسب وقت التنقل التقديري بين نشاطين. بيحاول الأول ينادي OSRM
    عشان ياخد وقت تنقل حقيقي على شبكة الطرق، ولو فشل (نت/timeout/رد
    غير متوقع) بيرجع لتقدير Haversine (خط مستقيم + سرعة افتراضية).

    لو مفيش إحداثيات لأي من النشاطين أصلاً، بيرجع قيمة افتراضية صغيرة
    (استعداد/انتقال عام) من غير ما يحاول ينادي OSRM.
    """
    if prev_activity is None:
        return 0

    prev_details = prev_activity.get("place_details")
    curr_details = activity.get("place_details")

    if not prev_details or not curr_details:
        return MIN_TRAVEL_MINUTES

    lat1, lon1 = prev_details.get("latitude"), prev_details.get("longitude")
    lat2, lon2 = curr_details.get("latitude"), curr_details.get("longitude")

    if None in (lat1, lon1, lat2, lon2):
        return MIN_TRAVEL_MINUTES

    osrm_minutes = _osrm_travel_minutes(lat1, lon1, lat2, lon2)
    if osrm_minutes is not None:
        return int(max(MIN_TRAVEL_MINUTES, min(MAX_TRAVEL_MINUTES, osrm_minutes)))

    return _haversine_travel_minutes(lat1, lon1, lat2, lon2)


def _recompute_schedule(activities: list[dict]) -> None:
    """
    بيعيد بناء الجدول الزمني بالكامل بعد إعادة الترتيب الجغرافي، بدل
    إعادة توزيع الأوقات القديمة (اللي كانت بتفسد الجدول لأنها مش
    بتاخد في الاعتبار الترتيب الجديد ولا مدة كل نشاط).

    المنطق:
      1. وقت بداية اليوم = أول time صالح كان موجود أصلاً عند Gemini
         (لو مفيش، بنستخدم DAY_START_HOUR الافتراضي).
      2. لكل نشاط: وقت البداية = نهاية النشاط اللي قبله + وقت تنقل
         تقديري (محسوب من المسافة الجغرافية لو متاحة).
      3. IGNORED_ACTIVITY_CATEGORIES (transport, إلخ) بتاخد وقت لكن
         مبتضيفش مدة "زيارة" كبيرة، بتتحسب كخطوة انتقال فقط.
    """
    if not activities:
        return

    # نحدد وقت بداية اليوم من أول وقت أصلي صالح، وإلا نستخدم الافتراضي
    original_times = [
        _parse_time_to_minutes(act.get("time"))
        for act in activities
        if act.get("time")
    ]
    valid_original_times = [t for t in original_times if t is not None]
    current_minutes = (
        min(valid_original_times) if valid_original_times else DAY_START_HOUR * 60
    )

    prev_activity: dict | None = None

    for activity in activities:
        category = (activity.get("category") or "").lower()

        travel_minutes = _get_travel_minutes(prev_activity, activity)
        current_minutes += travel_minutes

        activity["time"] = _minutes_to_time_str(current_minutes)

        if category in IGNORED_ACTIVITY_CATEGORIES:
            # خطوة انتقال بس، مدتها قصيرة ومبتحسبش duration كامل
            current_minutes += MIN_TRAVEL_MINUTES
        else:
            duration = _get_activity_duration_minutes(activity)
            current_minutes += duration

        prev_activity = activity


def enrich_trip(
    trip: dict,
    start_date: str | None
) -> dict:
    """
    Enriches a Gemini-generated trip plan with:
      - place_details for every activity (via search_place)
        * main activities (attraction/museum/hotel) get AI-enriched
          rating/reviews (enable_ai_details=True)
        * frequent categories (restaurant/cafe/...) stay fast, no rating
      - weather for the day's primary city
      - geographic reordering of route activities per day (nearest-
        neighbor) to minimize travel distance, with meals/transport
        staying attached to their nearest preceding route activity
      - a recomputed, internally-consistent time schedule that reflects
        both activity durations and real travel time between consecutive
        stops (via OSRM road-network routing, falling back to a
        Haversine straight-line estimate if OSRM is unreachable),
        instead of merely reusing Gemini's original time values in the
        new order

    Does NOT fetch category recommendations (hotels/restaurants/etc).
    Those are served on-demand via the /recommendations endpoint.
    """

    if "days" not in trip:
        return trip

    try:
        start = (
            datetime.fromisoformat(start_date)
            if start_date
            else datetime.today()
        )
    except Exception:
        start = datetime.today()

    weather_cache: dict[tuple[str, str], dict | None] = {}

    def get_weather_cached(city: str, date: str):
        key = (city, date)

        if key in weather_cache:
            return weather_cache[key]

        try:
            weather = get_weather(city=city, date=date)
        except Exception as e:
            logger.error(
                "Failed to fetch weather | city=%s date=%s error=%s",
                city,
                date,
                str(e),
            )
            weather = None

        weather_cache[key] = weather
        return weather

    # مجموعة place_id المُستخدمة كـ "بديل فئة" (category fallback) عبر
    # الرحلة كلها (مش بس اليوم الواحد) - عشان لو نشاطين مختلفين (حتى
    # في يومين مختلفين) رجعوا نفس الفئة العامة (زي "attraction")
    # ومحتاجين fallback، منرجعش نفس المكان البديل مرتين.
    used_fallback_place_ids: set[str] = set()

    for day in trip["days"]:

        current_date = (
            start + timedelta(days=day["day"] - 1)
        ).strftime("%Y-%m-%d")

        current_city = None
        activities = day.get("activities", [])

        for activity in activities:
            place_name = activity.get("place")
            category = activity.get("category")
            city = activity.get("city")

            if not place_name:
                continue

            if category and category.lower() in IGNORED_ACTIVITY_CATEGORIES:
                activity["place_details"] = None
                if current_city is None:
                    current_city = city
                continue

            try:
                is_main_activity = (
                    category and category.lower() in MAIN_ACTIVITY_CATEGORIES
                )
                place = search_place(
                    place_name,
                    city,
                    category,
                    enable_ai_details=is_main_activity,
                    exclude_place_ids=used_fallback_place_ids,
                )
            except Exception as e:
                logger.error(
                    "Failed to search place | place=%s city=%s error=%s",
                    place_name,
                    city,
                    str(e),
                )
                place = None

            if place:
                activity["place_details"] = place.model_dump()
                if current_city is None:
                    current_city = place.city or city
                if place.place_id:
                    used_fallback_place_ids.add(place.place_id)
            else:
                activity["place_details"] = None
                if current_city is None:
                    current_city = city

        # 1) رتب جغرافيًا
        day["activities"] = _reorder_day_activities(activities)
        # 2) أعد بناء الجدول الزمني بالكامل بناءً على الترتيب الجديد
        _recompute_schedule(day["activities"])

        if not current_city:
            continue

        weather = get_weather_cached(current_city, current_date)
        if weather:
            day["weather"] = weather

    return trip