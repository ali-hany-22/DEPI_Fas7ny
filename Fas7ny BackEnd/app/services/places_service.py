"""
places_service.py (OpenStreetMap Edition)

نسخة بديلة من places_service.py بتستخدم بيانات OpenStreetMap (مجانية بالكامل،
بدون أي احتياج لـ API key أو billing أو كارت ائتمان) بدل Google Places API.

بتستخدم خدمتين مجانيتين من مشروع OpenStreetMap:
1. Nominatim: تحويل اسم مدينة لإحداثيات جغرافية (Geocoding)
2. Overpass API: البحث عن أماكن (فنادق، مطاعم، متاحف...) حسب الفئة والموقع

ملاحظات مهمة:
- الجودة أقل شوية من Google Places (مفيش تقييمات نجوم أو صور بنفس الجودة
  دايماً)، لكنها كافية جداً لمشروع تخرج ومفيهاش أي قيود دفع خالص.
- Overpass API عندها Fair Use Policy (استخدام عادل) - يعني معندهاش حد
  رسمي صارم زي Google، بس المفروض تتجنب آلاف الطلبات في وقت قصير جداً
  عشان متتحظرش مؤقتاً من السيرفر العام. الكاش الدائم اللي عملناه قبل كده
  (persistent_cache.py) بيساعد جداً في تقليل الطلبات المتكررة.
"""

import logging
import math
import time
import re

import requests
from functools import lru_cache, wraps

from app.city_mapping import normalize_city
from app.models.place import Place
from app.services.image_service import get_place_image
from app.services.persistent_cache import get_cached, set_cached, list_all_entries
from app.services.gemini_place_service import GeminiPlaceService
logger = logging.getLogger("places_service")

# سيرفرات Nominatim و Overpass العامة - مجانية بالكامل بدون API key
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
# سيرفرات Overpass عامة متعددة (mirrors) - لو واحد فشل أو رجع 429/timeout،
# بنجرب اللي بعده تلقائياً. ده بيحل مشكلة إن overpass-api.de لوحده بيبقى
# مزدحم جداً في أوقات معينة.
OVERPASS_SERVERS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
]

# User-Agent مطلوب من سياسة استخدام Nominatim/Overpass - لازم يكون واضح
# ومعرف للمشروع بدل ما يبقى فاضي (وإلا ممكن يترفض الطلب)
HEADERS = {
    "User-Agent": "Trip_Planner_GraduationProject/1.0 (student project)"
}

# أنواع الأنشطة اللي مفيش لها Place حقيقي (زي المواصلات)
IGNORED_CATEGORIES = {"transport", "transportation", "travel", "flight", "drive"}


def cache_success_only(maxsize: int = 500):
    """
    بديل لـ lru_cache بيحفظ بس النتائج الناجحة (مش None).

    المشكلة اللي بيحلها: lru_cache العادي بيحفظ None برضه لو الدالة
    رجعت None - وده بيلخبط بين حالتين مختلفتين تمامًا:
    1. فشل شبكة مؤقت (Nominatim timeout/429) - المفروض يتحاول تاني.
    2. المكان فعلاً مش موجود - نتيجة نهائية.
    بدون تفرقة، أي فشل مؤقت بيتقفل بشكل دائم على None لحد ما الـ process
    يعمل restart كامل - بالظبط نفس مشكلة الـ lru_cache اللي واجهناها في
    الـ POI fetcher بتاع Overpass قبل كده.

    هنا: None مبيتحفظش خالص، فأي نداء تاني بنفس الـ arguments هيحاول
    الشبكة تاني بدل ما يفضل عالق على None قديم.
    """
    def decorator(fn):
        cache: dict = {}

        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = (args, tuple(sorted(kwargs.items())))

            if key in cache:
                return cache[key]

            result = fn(*args, **kwargs)

            if result is not None:
                if len(cache) >= maxsize:
                    # شيل أقدم عنصر (FIFO بسيط) عشان الكاش ميكبرش للأبد
                    cache.pop(next(iter(cache)))
                cache[key] = result

            return result

        wrapper.cache_clear = cache.clear
        return wrapper

    return decorator

# تحويل الفئة لـ OSM tags. كل فئة ممكن يكون ليها أكتر من tag بديل
# (OSM بتخزن نفس نوع المكان بطرق مختلفة أحياناً)
CATEGORY_OSM_TAGS = {
    "hotels": [("tourism", "hotel")],

    "restaurants": [
        ("amenity", "restaurant")
    ],

    "cafes": [
        ("amenity", "cafe"),
        ("shop", "coffee"),
        ("cuisine", "coffee_shop")
    ],

    "museums": [
        ("tourism", "museum"),
        ("tourism", "gallery"),
        ("historic", "monument")
    ],

    "parks": [
        ("leisure", "park"),
        ("leisure", "garden")
    ],

    "shopping": [
        ("shop", "mall"),
        ("shop", "department_store"),
        ("shop", "supermarket"),
        ("shop", "convenience"),
        ("shop", "clothes"),
        ("shop", "gift"),
        ("shop", "marketplace"),
        ("marketplace", "yes"),
    ],

    "beaches": [
        ("natural", "beach"),
        ("leisure", "beach_resort")
    ],

    "entertainment": [
    ("tourism", "attraction"),
    ("tourism", "theme_park"),
    ("tourism", "zoo"),
    ("tourism", "aquarium"),
    ("leisure", "water_park"),
    ("amenity", "cinema"),
    ("leisure", "park"),
    ("leisure", "garden"),
    ("sport", "scuba_diving"),
    ("club", "diving"),
    ("shop", "scuba_diving"),
],
}

# ----------------------------------------------------------------------
# تحويل فئات الأنشطة الفعلية اللي بترجع من الـ trip prompt (زي "hotel"،
# "shopping"، "activity"، "cinema" - مفرد ومتنوعة) لمفاتيح CATEGORY_OSM_TAGS
# (زي "hotels"، "shopping"، "entertainment" - جمع وموحّدة). مستخدمة في
# _search_place_by_category_fallback بس (Overpass fallback لما search_place
# تفشل بالاسم بالكامل).
# ----------------------------------------------------------------------
TRIP_CATEGORY_TO_OSM_KEY: dict[str, str] = {
    "hotel": "hotels",
    "hotels": "hotels",
    "restaurant": "restaurants",
    "restaurants": "restaurants",
    "cafe": "cafes",
    "cafes": "cafes",
    "museum": "museums",
    "museums": "museums",
    "attraction": "entertainment",
    "attractions": "entertainment",
    "park": "parks",
    "parks": "parks",
    "shopping": "shopping",
    "beach": "beaches",
    "beaches": "beaches",
    "cinema": "entertainment",
    "amusement park": "entertainment",
    "amusement_park": "entertainment",
    "activity": "entertainment",
    "activities": "entertainment",
    "water sports": "entertainment",
    "water_sports": "entertainment",
    "diving": "entertainment",
}
# ملاحظة: الـ city normalization (تحويل الأحياء/القرى للمدينة الأم)
# بقت في app/city_mapping.py وبتغطي كل محافظات مصر بدل القاهرة والجيزة بس.
# normalize_city() هي نفس دور normalize_city() القديمة بالظبط.


# ----------------------------------------------------------------------
# تنظيف اسم المكان قبل البحث - نفس فكرة clean_hotel_name() في pipeline
# الفنادق، بس هنا بتتطبق على أي اسم مكان راجع من Gemini قبل ما نبعته
# لـ Nominatim. أسماء وصفية/تسويقية زي "the best restaurant in Luxor"
# أو أسماء فيها أقواس/تفاصيل زيادة بتفشل مع Nominatim غالبًا.
# ----------------------------------------------------------------------

_NOISE_PATTERNS = [
    r"\(.*?\)",           # أي حاجة جوه أقواس
    r"\bthe best\b",
    r"\bbest\b",
    r"\bfamous\b",
    r"\btop[- ]rated\b",
    r"\brecommended\b",
    r"\bpopular\b",
    r"\bin (cairo|luxor|aswan|giza|alexandria|hurghada|sharm el sheikh)\b",
]


def clean_place_name(raw_name: str) -> str:
    """
    بتشيل الكلام التسويقي/الوصفي الزيادة من اسم المكان قبل البحث،
    وبترجع اسم أنضف وأقرب للاسم الرسمي القابل للبحث في Nominatim.
    لو التنظيف رجّع string فاضي (زي لو الاسم كله كان وصفي)، بترجع
    الاسم الأصلي زي ما هو بدل ما تضيّعه.
    """
    if not raw_name:
        return raw_name

    cleaned = raw_name.strip()

    for pattern in _NOISE_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # مسافات زيادة وفواصل يتيمة بعد الشيل
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    cleaned = cleaned.strip(" ,-–—")

    return cleaned if cleaned else raw_name.strip()


# ----------------------------------------------------------------------
# Geocoding: تحويل اسم مكان/مدينة لإحداثيات (lat, lon)
# ----------------------------------------------------------------------

@lru_cache(maxsize=200)
def _geocode(query: str) -> tuple[float, float] | None:
    """
    بتحول اسم مكان (زي "Cairo, Egypt") لإحداثيات جغرافية.
    الكاش هنا في الذاكرة بس (lru_cache) لأن الإحداثيات نادراً ما تتغير
    وده بيقلل استدعاءات Nominatim المتكررة لنفس المدينة في نفس الـ run.
    """
    try:
        response = requests.get(
            NOMINATIM_URL,
            params={
                "q": query,
                "format": "json",
                "limit": 1,
            },
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        results = response.json()

        if not results:
            logger.info("Geocoding: no results for query=%s", query)
            return None

        lat = float(results[0]["lat"])
        lon = float(results[0]["lon"])

        # سياسة الاستخدام العادل لـ Nominatim بتطلب طلب واحد بالثانية كحد أقصى
        time.sleep(1)

        return lat, lon

    except (requests.RequestException, ValueError, KeyError) as e:
        logger.error("Geocoding failed for query=%s | error=%s", query, str(e))
        return None


def _reverse_geocode_city(lat: float, lon: float) -> tuple[str | None, str | None]:
    """
    بتاخد إحداثيات وبترجع (city, country) - عكس الـ geocode العادي.
    مفيدة لما نجيب مكان من Overpass ومعندوش اسم مدينة واضح في الـ tags.
    """
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={
                "lat": lat,
                "lon": lon,
                "format": "json",
            },
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        address = data.get("address", {})
        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("county")
        )
        country = address.get("country")

        time.sleep(1)

        return city, country

    except (requests.RequestException, ValueError, KeyError) as e:
        logger.error("Reverse geocoding failed | error=%s", str(e))
        return None, None


# ----------------------------------------------------------------------
# تحويل نتيجة Overpass لـ Place object
# ----------------------------------------------------------------------

def _place_from_osm_element(
    element: dict,
    fallback_city: str | None,
    trust_fallback_city: bool = False,
    enable_ai_details: bool = False,
) -> Place | None:
    """
    trust_fallback_city=True بتجبر الـ city يبقى دايماً fallback_city
    (المدينة اللي دورنا فيها فعلياً)، من غير ما نعتمد على addr:city من
    OSM خالص. ده مهم لـ search_places_by_category لأن الدايرة بتاعتنا
    (radius) أصلاً مركزها إحداثيات المدينة المطلوبة - فأي مكان راجع
    منطقيًا لازم يتحسب على إنه في المدينة دي، حتى لو الـ addr:city
    بتاعه في OSM هو اسم قرية/حي صغير تحتها (زي "قريه البعيرات" تحت
    الأقصر) ومش موجود في city_mapping.py.

    لـ search_place (بحث باسم مكان محدد)، trust_fallback_city بتفضل
    False زي القديم بالظبط - هناك addr:city فعلاً أدق من fallback.
    """
    tags = element.get("tags", {})

    name = (
        tags.get("name")
        or tags.get("name:en")
        or tags.get("name:ar")
    )

    if not name:
        return None

    name = name.strip()

    # أسماء غير صالحة أو داخلية في OSM
    INVALID_PREFIXES = (
        "LX_",
        "EG_",
        "ID_",
        "TMP_",
    )

    INVALID_NAMES = {
        "unnamed",
        "unknown",
        "no name",
        "null",
        "-",
        ".",
    }

    # Prefixes
    if name.startswith(INVALID_PREFIXES):
        return None

    # أسماء قصيرة جدًا
    if len(name) < 3:
        return None

    # أرقام فقط
    if name.isdigit():
        return None

    # أسماء غير مفيدة
    if name.lower() in INVALID_NAMES:
        return None

    # node12345 أو way12345
    if re.match(r"^(node|way)\d*$", name.lower()):
        return None

    # أكواد مثل LX_NW_P001_GREEN001
    if re.match(r"^[A-Z]{2,}[_A-Z0-9]+$", name):
        return None

    lat = element.get("lat") or element.get("center", {}).get("lat")
    lon = element.get("lon") or element.get("center", {}).get("lon")

    if lat is None or lon is None:
        return None

    # بناء عنوان تقريبي من الـ tags المتاحة (OSM مش دايماً بيدي عنوان كامل زي جوجل)
    address_parts = []
    if tags.get("addr:street"):
        address_parts.append(tags["addr:street"])
    if tags.get("addr:city"):
        address_parts.append(tags["addr:city"])

    address = ", ".join(address_parts) if address_parts else tags.get("addr:full", "")
    # لو العنوان فاضي نحاول نستخدم اسم الشارع أو المنطقة
    if not address:
        address = (
            tags.get("addr:place")
            or tags.get("addr:suburb")
            or tags.get("addr:district")
            or ""
        )


    if trust_fallback_city and fallback_city:
        city = normalize_city(fallback_city)
    else:
        city = tags.get("addr:city") or fallback_city
        city = normalize_city(city)

    image = get_place_image(name, city)

    
    if not image:
        image = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

    google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    osm_id = f"osm-{element.get('type', 'node')}-{element.get('id')}"

    # ملحوظة مهمة: كان فيه نداء غير مشروط لـ GeminiPlaceService هنا بيتنادى
    # لكل عنصر راجع من Overpass (يعني عشرات المرات لكل category search واحد،
    # مش بس للأنشطة الفعلية في الرحلة). ده كان بيستهلك الـ Free Tier quota
    # بتاع Gemini (20 request/day) بسرعة جدًا، وبمجرد ما الكوتة تخلص، أي
    # نداء تاني كان بيرمي 429 RESOURCE_EXHAUSTED - ولإن الاستدعاء مكانش
    # محاط بـ try/except، الاستثناء كان بيكسر الدالة كلها ويرجعها None،
    # وده اللي كان بيسبب كل الـ place_details تطلع null بعد استهلاك الكوتة،
    # وكمان بيسبب تخزين نتايج فاضية في الكاش الدائم.
    #
    # الحل: (1) نحط الاستدعاء وراء enable_ai_details زي search_place بالظبط
    # (افتراضيًا False - رخيص وسريع، من غير Gemini)، و(2) نحيط أي نداء فعلي
    # بـ try/except عشان فشله (كوتة/نت) مايكسرش المكان كله ويرجّعه None.
    rating = None
    reviews = None
    if enable_ai_details:
        try:
            details = GeminiPlaceService.get_place_details(
                place_name=name,
                city=city or fallback_city or "",
            )
            rating = details.get("rating")
            reviews = details.get("reviews")
        except Exception as e:
            logger.warning(
                "GeminiPlaceService failed for place=%s city=%s | error=%s",
                name, city or fallback_city, str(e),
            )

    popularity_score, popularity = _compute_popularity(rating, reviews)

    return Place(
        name=name,
        address=address or (city or ""),
        city=city,
        country=tags.get("addr:country") or "مصر",

        popularity_score=popularity_score,
        popularity=popularity,

        rating=rating,
        reviews=reviews,

        latitude=lat,
        longitude=lon,

        google_maps=google_maps_link,

        image_url=image,
        place_id=osm_id,
    )


# ----------------------------------------------------------------------
# Overpass query builder + caller
# ----------------------------------------------------------------------

def _build_overpass_query(lat: float, lon: float, osm_tags: list[tuple[str, str]], radius_m: int = 10000) -> str:
    """
    بتبني Overpass QL query للبحث عن عناصر (node/way) في دايرة نصف قطرها
    radius_m متر حوالين الإحداثيات المعطاة، بفلاتر tags معينة.

    قللنا الـ radius لـ 10 كم (كان 20) لأن نطاق أوسع في مدن مزدحمة زي
    القاهرة بيخلي وقت معالجة الاستعلام عند السيرفر طويل جداً، حتى لو
    السيرفر نفسه مش مشغول بطلبات تانية (زي ما تأكدنا من /api/status).

    ملحوظة مهمة: شلنا شرط ["name"] الإجباري من هنا. كان بيستبعد نسبة كبيرة
    من الأماكن (خصوصاً cafes/shops/beaches) اللي مسجلة على OSM بـ
    name:en أو name:ar بس من غير مفتاح "name" العادي، أو من غير أي اسم
    خالص - وده كان سبب رئيسي في رجوع نتايج فاضية لفئات معينة. الفلترة
    دلوقتي بتحصل في بايثون في _place_from_osm_element (اللي أصلاً
    بيتأكد من name/name:en/name:ar وبيرفض العنصر لو مفيش أي واحد منهم).
    """
    filters = "".join(
        f'node["{key}"="{value}"](around:{radius_m},{lat},{lon});'
        f'way["{key}"="{value}"](around:{radius_m},{lat},{lon});'
        for key, value in osm_tags
    )

    return f"""
    [out:json][timeout:40];
    (
      {filters}
    );
    out center 60;
    """


def _query_overpass(query: str) -> list[dict] | None:
    """
    بتبعت الاستعلام لأول سيرفر Overpass شغال من قائمة OVERPASS_SERVERS.
    لو سيرفر فشل (timeout, 429, 5xx)، بتجرب اللي بعده تلقائياً قبل ما
    ترجع None. ده بيحل مشكلة إن سيرفر واحد بس (زي overpass-api.de)
    ممكن يبقى مزدحم جداً في أوقات معينة من اليوم.
    """
    for server_url in OVERPASS_SERVERS:
        try:
            response = requests.post(
                server_url,
                data={"data": query},
                headers=HEADERS,
                timeout=55,
            )

            if response.status_code == 429:
                logger.warning("Overpass server %s: 429 rate limited, trying next mirror", server_url)
                continue

            if response.status_code >= 500:
                logger.warning("Overpass server %s: %s server error, trying next mirror", server_url, response.status_code)
                continue

            response.raise_for_status()
            return response.json().get("elements", [])

        except requests.Timeout:
            logger.warning("Overpass server %s: timed out, trying next mirror", server_url)
            continue

        except requests.RequestException as e:
            logger.warning("Overpass server %s: request failed (%s), trying next mirror", server_url, str(e))
            continue

    logger.error("All Overpass mirrors failed for this query")
    return None


def _search_place_by_category_fallback(
    place_name: str,
    city: str | None,
    category: str | None,
    exclude_place_ids: set[str] | None = None,
    enable_ai_details: bool = False,
) -> Place | None:
    """
    محاولة أخيرة لما search_place تفشل تمامًا بالاسم (كل الأشكال: منضف،
    أصلي، من غير مدينة، وبديل اللغة). بدل ما نرجع None على طول، بندور
    بـ Overpass عن **أقرب مكان من نفس الفئة** حوالين مركز المدينة -
    حتى لو اسمه مختلف تمامًا عن اللي جه من Gemini.

    السبب: أماكن كتير (سينمات ومراكز غوص جوه منتجعات، مطاعم بأسماء
    تجارية مش دقيقة) مش موجودة في OSM بالاسم بالظبط، لكن فيه أماكن
    تانية من نفس الفئة فعلاً موجودة وقريبة. الأفضل نرجع "مكان بديل
    منطقي من نفس النوع" بدل null تمامًا - المستخدم النهائي مستفيد من
    نشاط حقيقي حتى لو مش بنفس الاسم اللي اقترحه Gemini بالظبط.

    exclude_place_ids: مجموعة place_id اتستخدمت بالفعل كـ fallback في
    نفس الرحلة. لاحظنا إن نشاطين مختلفين تمامًا (زي "سينما رويال" و
    "شاطئ صن رايز") ممكن ياخدوا نفس فئة Gemini العامة ("attraction")،
    فلو مانستبعدش، الاتنين هياخدوا نفس أقرب عنصر Overpass بالظبط -
    وده بيوهم المستخدم إنهم نفس المكان. عشان كده بنستبعد أي عنصر
    place_id بتاعه موجود في المجموعة دي، وناخد أقرب عنصر تاني بدلًا
    منه.

    بترجع None لو: مفيش category، أو الفئة مش معروفة، أو المدينة مش
    موجودة في _CITY_CENTROIDS (مفيش نقطة نبحث حواليها)، أو Overpass
    فشلت، أو مفيش أي عنصر صالح قريب (بعد استبعاد المُستخدم بالفعل).
    """
    if not category:
        return None

    exclude_place_ids = exclude_place_ids or set()

    osm_key = TRIP_CATEGORY_TO_OSM_KEY.get(category.strip().lower())
    if not osm_key:
        return None

    osm_tags = CATEGORY_OSM_TAGS.get(osm_key)
    if not osm_tags:
        return None

    normalized_city = normalize_city(city) if city else None
    centroid = _CITY_CENTROIDS.get(normalized_city) if normalized_city else None
    if centroid is None:
        logger.info(
            "Category fallback skipped for place=%s: no known centroid for city=%s",
            place_name, city,
        )
        return None

    city_lat, city_lon, radius_km = centroid
    radius_m = int(radius_km * 1000)

    query = _build_overpass_query(city_lat, city_lon, osm_tags, radius_m=radius_m)
    elements = _query_overpass(query)

    if not elements:
        logger.info(
            "Category fallback: Overpass returned nothing for category=%s (osm_key=%s) near city=%s",
            category, osm_key, city,
        )
        return None

    # ناخد أقرب عنصر صالح لمركز المدينة (مش أول عنصر عشوائي)، عشان
    # النتيجة تكون منطقية جغرافيًا حتى لو فيه عناصر كتير راجعة.
    def _element_distance(element: dict) -> float:
        lat = element.get("lat") or (element.get("center") or {}).get("lat")
        lon = element.get("lon") or (element.get("center") or {}).get("lon")
        if lat is None or lon is None:
            return float("inf")
        return _haversine_km(city_lat, city_lon, lat, lon)

    elements_sorted = sorted(elements, key=_element_distance)

    for element in elements_sorted:
        element_place_id = f"osm-{element.get('type', 'node')}-{element.get('id')}"
        if element_place_id in exclude_place_ids:
            continue

        place = _place_from_osm_element(
            element,
            fallback_city=normalized_city,
            trust_fallback_city=True,
            enable_ai_details=enable_ai_details,
        )
        if place is not None:
            logger.info(
                "Category fallback SUCCESS: found '%s' (category=%s) as substitute for '%s' in city=%s",
                place.name, category, place_name, city,
            )
            return place

    logger.info(
        "Category fallback: no valid named element found for category=%s near city=%s",
        category, city,
    )
    return None


# ----------------------------------------------------------------------
# Public API - نفس التوقيعات (signatures) بتاعة النسخة القديمة بالظبط،
# عشان enrichment_service.py وباقي الكود يشتغل من غير أي تعديل تاني.
# ----------------------------------------------------------------------

def _get_ai_details_safe(place_name: str, city: str) -> dict:
    """
    نداء اختياري لـ GeminiPlaceService، محاط بـ try/except عشان فشله
    (أو بطؤه) مايكسرش search_place. بيتنادى بس لو enable_ai_details=True.
    """
    try:
        return GeminiPlaceService.get_place_details(
            place_name=place_name,
            city=city or "",
        )
    except Exception as e:
        logger.warning(
            "GeminiPlaceService failed | place=%s city=%s error=%s",
            place_name, city, str(e),
        )
        return {}


@cache_success_only(maxsize=500)
# ----------------------------------------------------------------------
# حساب popularity_score / popularity بناءً على rating و reviews الحقيقية
# ----------------------------------------------------------------------
# قبل كده كانت popularity_score=0 و popularity="Low" قيم ثابتة (defaults
# من Place model) بتتحط لكل مكان أيًا كان تقييمه الفعلي، لأن search_place
# و_place_from_osm_element مكانوش بيحطوا أي قيمة لهم خالص. الدالة دي
# بتحسب Score حقيقي (0-100) من مزيج التقييم (rating) وعدد المراجعات
# (reviews) - مكان معندوش بيانات (rating/reviews = None) بيفضل طبيعيًا
# على الـ default (0, "Low") لأننا معندناش أي دليل نحكم بيه.

def _compute_popularity(rating: float | None, reviews: int | None) -> tuple[int, str]:
    """
    بترجع (popularity_score, popularity_label) بناءً على:
      - rating (0-5): كل نجمة = 15 نقطة (rating=5 -> 75 نقطة)
      - reviews: بونص لوغاريتمي حتى 25 نقطة إضافية (عشان عدد كبير
        جدًا من المراجعات - زي 30 ألف - مايطلعش أعلى من مكان بـ 500
        مراجعة بس بشكل غير متناسب، لكن لسه بيدي فرق واضح)

    لو مفيش rating أو reviews خالص، بترجع (0, "Low") - نفس الـ default
    القديم بالظبط، لأن مفيش أي بيانات نبني عليها حكم مختلف.
    """
    if rating is None and reviews is None:
        return 0, "Low"

    score = 0.0

    if rating is not None:
        score += max(0.0, min(5.0, rating)) * 15  # لحد 75 نقطة

    if reviews is not None and reviews > 0:
        # bonus لوغاريتمي: 10 مراجعات -> ~7 نقاط، 1000 -> ~21 نقطة،
        # 30000 -> ~25 نقطة (السقف الأقصى)
        review_bonus = min(25.0, math.log10(reviews + 1) * 7)
        score += review_bonus

    score = int(round(min(100.0, score)))

    if score >= 70:
        label = "High"
    elif score >= 40:
        label = "Medium"
    else:
        label = "Low"

    return score, label


# ----------------------------------------------------------------------
# مسافة جغرافية (Haversine) - مستخدمة في التحقق من قرب النتيجة لمدينتها
# ----------------------------------------------------------------------

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """مسافة تقريبية بالكيلومتر بين نقطتين جغرافيتين."""
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    )
    return 2 * R * math.asin(math.sqrt(a))


# ----------------------------------------------------------------------
# إحداثيات مركزية تقريبية لأشهر المدن السياحية المصرية + نصف قطر خاص
# بكل مدينة (كم) - مستخدمة فقط للتحقق الجغرافي (مش لعرضها للمستخدم).
# المصدر: نفس أسماء المدن الموجودة في app/city_mapping.py (TOURISTIC_CITIES).
#
# ليه نصف قطر مختلف لكل مدينة بدل رقم ثابت واحد؟ لأن رقم عام واحد
# (كنا مجربين 100 ثم 50) بيفشل في الاتجاهين:
#   - مدن كبيرة مترامية زي القاهرة الكبرى (تضم القاهرة + الجيزة + القاهرة
#     الجديدة) محتاجة نصف قطر أكبر، وإلا هنرفض نتايج صحيحة فعلًا.
#   - مدن ساحلية سياحية صغيرة ومتقاربة من بعض جغرافيًا (الغردقة/شرم
#     الشيخ/دهب/الساحل الشمالي) محتاجة نصف قطر أصغر، لأن لو استخدمنا
#     رقم كبير هنقبل غلط نتيجة من مدينة مجاورة (زي حالة "سيناي بيتش"
#     في الغردقة اللي رجعت شرم الشيخ على بعد 98.6 كم).
#
# القيمة: (lat, lon, radius_km)
# ----------------------------------------------------------------------
_CITY_CENTROIDS: dict[str, tuple[float, float, float]] = {
    # مدن كبرى مترامية - نصف قطر أكبر (40-45 كم)
    "Cairo": (30.0444, 31.2357, 45.0),
    "Giza": (30.0131, 31.2089, 45.0),
    "Alexandria": (31.2001, 29.9187, 40.0),

    # مدن سياحية ساحلية/صحراوية صغيرة ومتقاربة من بعضها - نصف قطر أصغر
    # (20-25 كم) عشان نفرّق بينها وبين المدن المجاورة بدقة
    "Luxor": (25.6872, 32.6396, 25.0),
    "Aswan": (24.0889, 32.8998, 25.0),
    "Hurghada": (27.2579, 33.8116, 25.0),
    "Red Sea": (26.5000, 34.0000, 30.0),
    "Sharm El Sheikh": (27.9158, 34.3300, 20.0),
    "Dahab": (28.5091, 34.5136, 15.0),
    "South Sinai": (28.5000, 33.9000, 30.0),
    "North Sinai": (31.1300, 33.8000, 30.0),

    # مدن متوسطة الحجم - نصف قطر متوسط (30 كم افتراضي)
    "Ismailia": (30.5965, 32.2715, 30.0),
    "Suez": (29.9668, 32.5498, 30.0),
    "Port Said": (31.2653, 32.3019, 30.0),
    "Damietta": (31.4165, 31.8133, 30.0),
    "Mansoura": (31.0409, 31.3785, 30.0),
    "Zagazig": (30.5877, 31.5020, 30.0),
    "Tanta": (30.7865, 31.0004, 30.0),
    "Shibin El Kom": (30.5545, 31.0100, 30.0),
    "Banha": (30.4667, 31.1833, 30.0),
    "Damanhour": (31.0341, 30.4682, 30.0),
    "Kafr El Sheikh": (31.1107, 30.9388, 30.0),
    "Beni Suef": (29.0744, 31.0979, 30.0),
    "Fayoum": (29.3084, 30.8428, 30.0),
    "Minya": (28.1099, 30.7503, 30.0),
    "Assiut": (27.1809, 31.1837, 30.0),
    "Sohag": (26.5591, 31.6957, 30.0),
    "Qena": (26.1551, 32.7160, 30.0),
    "New Valley": (25.4515, 30.5464, 40.0),  # واحات متباعدة، محتاجة مساحة أكبر
    "Matrouh": (31.3543, 27.2373, 30.0),
}

# نصف قطر افتراضي (كم) لأي مدينة موجودة في city_mapping.py بس مش
# مضافة هنا بالاسم - قيمة متوسطة معقولة.
_DEFAULT_CITY_RADIUS_KM = 30.0


def _is_within_city(lat: float, lon: float, city: str | None) -> bool:
    """
    بتتأكد لو نقطة معينة (lat, lon) قريبة بشكل معقول من مركز مدينة
    مصرية معروفة، باستخدام نصف قطر خاص بكل مدينة (مش رقم ثابت عام).
    بترجع True لو مش عندنا بيانات كافية نتحقق بيها (مدينة مش موجودة
    في _CITY_CENTROIDS، أو city=None) - في الحالة دي بنسيب النتيجة
    تعدي، لأن مفيش أساس نرفض عليه.
    """
    if not city:
        return True

    normalized = normalize_city(city)
    centroid = _CITY_CENTROIDS.get(normalized)
    if centroid is None:
        return True

    city_lat, city_lon, radius_km = centroid
    distance_km = _haversine_km(lat, lon, city_lat, city_lon)
    return distance_km <= radius_km


def _get_alternate_language_name(place_name: str, city: str | None) -> str | None:
    """
    بتستخدم نفس مصادر GeminiPlaceService (Gemini + Gemini alt + Groq
    rotation) عشان تستخرج الاسم بلغة مختلفة عن اللي دخل بيها (لو الاسم
    عربي بترجع أقرب اسم إنجليزي رسمي، ولو إنجليزي بترجع أقرب اسم عربي
    شائع). السبب: OSM مش متسق - بعض الأماكن مسجلة بالعربي بس (زي "مقهى
    الفيشاوي")، وبعضها بالإنجليزي بس (زي "Buffalo Burger")، فمينفعش
    نفترض اتجاه واحد بس.

    بترجع None لو فشلت كل المصادر أو الرد مش منطقي، عشان الكود اللي
    بينادي الدالة يكمل عادي من غير ما يقع.
    """
    try:
        result = GeminiPlaceService.get_alternate_language_place_name(place_name, city or "")
        if result and isinstance(result, str) and result.strip():
            return result.strip()
        return None
    except Exception as e:
        logger.warning(
            "Failed to get alternate-language name for place=%s city=%s | error=%s",
            place_name, city, str(e),
        )
        return None


def search_place(
    place_name: str,
    city: str | None = None,
    category: str | None = None,
    enable_ai_details: bool = False,
    exclude_place_ids: set[str] | None = None,
) -> Place | None:
    """
    بتدور على مكان بالاسم داخل مدينة معينة، باستخدام Nominatim مباشرة
    (أدق وأسرع من Overpass لما بندور على اسم محدد بدل فئة عامة).

    enable_ai_details=False (الافتراضي): سريعة - بتاخد بس بيانات OSM
    (اسم، عنوان، إحداثيات، صورة). دي القيمة المستخدمة في enrichment_service
    لأنها بتتنادى لكل activity في كل رحلة (high frequency) - نداء Gemini
    إضافي هنا كان بيبطّئ توليد الرحلة بشكل كبير من غير داعي.

    enable_ai_details=True: بتضيف نداء لـ GeminiPlaceService لجلب rating/
    reviews تقديرية. استخدمها فقط في سياقات low-frequency (زي شاشة تفاصيل
    مكان واحد يطلبها المستخدم بنفسه).

    exclude_place_ids: مجموعة place_id من أنشطة سابقة في نفس الرحلة.
    بتتمرر لـ category fallback بس (لما البحث بالاسم يفشل تمامًا)
    عشان منرجعش نفس المكان البديل لنشاطين مختلفين (زي "سينما رويال"
    و"شاطئ صن رايز" اللي ممكن ياخدوا نفس فئة Gemini العامة).
    """
    if category and category.lower() in IGNORED_CATEGORIES:
        logger.info("Skipping search_place for non-place category: %s", category)
        return None

    if not place_name or not place_name.strip():
        return None

    # ----------------------------------------------------------------
    # كاش دائم على مستوى المكان الواحد (اسم + مدينة) - قبل كده كان
    # persistent_cache متوصّل بس بـ search_places_by_category (بحث حسب
    # فئة عامة)، ومكانش بيتنادى خالص من search_place (اللي هي فعليًا
    # المستخدمة من enrichment_service لكل نشاط في كل رحلة). ده كان
    # سبب إن places_cache.json يفضل فاضي رغم إن كل رحلة بتعمل عشرات
    # نداءات Nominatim/Gemini اللي المفروض تتخزن.
    #
    # المفتاح هنا "مكان" مش "فئة" زي الدالة التانية، فبنستخدم بادئة
    # "place::" عشان منختلطش مع مفاتيح search_places_by_category.
    # ----------------------------------------------------------------
    cache_city = normalize_city(city) if city else "unknown"
    cache_key_name = f"place::{place_name.strip().lower()}"

    cached_entry = get_cached(cache_city, cache_key_name)
    if cached_entry is not None:
        if cached_entry == []:
            # كنا خزّنا "مفيش نتيجة" قبل كده - نرجع None بدل ما نعيد
            # البحث من الصفر (وده اللي كان بيوفر النداءات فعليًا)
            return None

        cached_place = cached_entry[0]
        # لو الطلب الحالي محتاج rating/reviews (enable_ai_details=True)
        # لكن النسخة المخزّنة اتحفظت من غير rating (طلب سابق كان
        # enable_ai_details=False)، منستخدمش الكاش هنا ونكمل البحث
        # عادي عشان ناخد فرصة نجيب الـ rating الفعلي. أي حالة تانية
        # (الكاش فيه rating، أو الطلب الحالي مش محتاج rating أصلًا)
        # الكاش كافي ومنرجعه على طول.
        if not (enable_ai_details and cached_place.get("rating") is None):
            return Place(**cached_place)

    # ----------------------------------------------------------------
    # Cross-city cache lookup: لو الطلب جه من غير city محددة (زي بحث
    # حر من صفحة /search في الفرونت اللي مبيبعتش city خالص)، كنا لحد
    # دلوقتي بندور بس تحت مفتاح "unknown::place::<name>" - وده تقريبًا
    # مستحيل يلاقي حاجة، لأن نفس المكان ده غالبًا اتخزن قبل كده تحت
    # مدينة حقيقية (زي "luxor") من مصدر تاني (enrichment_service وقت
    # توليد رحلة مثلاً). فبنستني هنا: قبل ما نستسلم لمفتاح "unknown"
    # ونعمل بحث لايف كامل من الصفر، ندور عبر كل المدن المخزّنة فعلاً
    # عن نفس اسم المكان بالظبط (بعد نفس التطبيع/lowercase المستخدم في
    # cache_key_name). لو لقينا تطابق، نرجعه فورًا من غير أي طلب شبكة.
    #
    # ده بيتنفذ بس لو الطلب الأصلي مجاش بـ city (city is None/empty)،
    # عشان لو المستخدم فعلاً حدد مدينة معينة، نحترم اختياره ومنرجعش
    # نتيجة من مدينة تانية بدون علمه.
    # ----------------------------------------------------------------
    if not city:
        try:
            all_place_entries = list_all_entries(category="place")
        except Exception as e:
            logger.warning("list_all_entries failed during cross-city lookup | error=%s", str(e))
            all_place_entries = []

        target_key = cache_key_name  # "place::<name>" بنفس التطبيع

        for entry in all_place_entries:
            entry_category = entry.get("_cache_category", "")
            if entry_category != target_key:
                continue

            if enable_ai_details and entry.get("rating") is None:
                # نفس منطق الكاش العادي فوق: لو محتاجين rating ومش
                # موجود في النسخة المخزّنة، منستخدمهاش - نكمل بحث لايف
                continue

            clean_entry = {
                k: v for k, v in entry.items()
                if k not in ("_cache_city", "_cache_category")
            }
            logger.info(
                "Cross-city cache HIT for place='%s' found under city='%s' "
                "(original request had no city)",
                place_name, entry.get("_cache_city"),
            )
            return Place(**clean_entry)

    search_name = clean_place_name(place_name)

    def _run_nominatim_query(name: str) -> list:
        query = f"{name}, {city}, Egypt" if city else f"{name}, Egypt"
        try:
            response = requests.get(
                NOMINATIM_URL,
                params={
                    "q": query,
                    "format": "json",
                    "limit": 1,
                    "addressdetails": 1,
                },
                headers=HEADERS,
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            time.sleep(1)  # احترام سياسة الاستخدام العادل لـ Nominatim
            return data
        except requests.RequestException as e:
            logger.error("search_place request failed | query=%s | error=%s", query, str(e))
            return []

    def _run_nominatim_query_no_city(name: str) -> list:
        """
        نفس اللي فوق بس من غير الـ city qualifier (بس الاسم + Egypt).
        بعض الأماكن (زي "Citystars Mall") رجعت صفر نتايج لما الاستعلام
        كان "Citystars Mall, Cairo, Egypt" بينما الاستعلام الأبسط بينجح.

        خطر: من غير قيد المدينة، Nominatim ممكن يرجع أول نتيجة تطابق
        الاسم في مصر كلها، حتى لو في مدينة تانية تمامًا (لاحظنا حالة
        "شاطئ كليوباترا" برجعت نتيجة في الغردقة بدل الإسكندرية). عشان
        كده بنفلتر النتايج هنا: أي نتيجة بعيدة جغرافيًا عن المدينة
        المطلوبة (city) بترفض، حتى لو كانت أول/نتيجة وحيدة راجعة.
        """
        query = f"{name}, Egypt"
        try:
            response = requests.get(
                NOMINATIM_URL,
                params={
                    "q": query,
                    "format": "json",
                    "limit": 3,
                    "addressdetails": 1,
                },
                headers=HEADERS,
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            time.sleep(1)

            if not city:
                return data

            filtered = []
            for item in data:
                try:
                    lat, lon = float(item["lat"]), float(item["lon"])
                except (KeyError, ValueError, TypeError):
                    continue
                if _is_within_city(lat, lon, city):
                    filtered.append(item)
                else:
                    logger.info(
                        "Rejecting no-city result for '%s': too far from city=%s (lat=%s, lon=%s)",
                        name, city, lat, lon,
                    )

            return filtered

        except requests.RequestException as e:
            logger.error("search_place (no-city) request failed | query=%s | error=%s", query, str(e))
            return []

    results = _run_nominatim_query(search_name)

    # لو الاسم المنضف فشل ومختلف عن الأصلي، نجرب الاسم الأصلي كـ fallback
    if not results and search_name != place_name.strip():
        logger.info(
            "Cleaned name '%s' returned nothing, retrying with original '%s'",
            search_name, place_name,
        )
        results = _run_nominatim_query(place_name.strip())

    # لو لسه مفيش نتيجة، نجرب من غير الـ city qualifier في الاستعلام.
    # لاحظنا حالات زي "Citystars Mall, Cairo, Egypt" رجعت صفر نتايج،
    # بينما البحث بالاسم لوحده (أو مع "Egypt" بس) كان بينجح - على
    # الأغلب لأن الـ query المُركّب بيضيّق النتيجة أكتر من اللازم لما
    # الاسم نفسه مش مطابق لحرفية العنوان المسجل في OSM.
    if not results and city:
        logger.info(
            "City-qualified query for '%s' returned nothing, retrying without city",
            search_name,
        )
        results = _run_nominatim_query_no_city(search_name)
        if not results and search_name != place_name.strip():
            results = _run_nominatim_query_no_city(place_name.strip())

    # لو لسه مفيش نتيجة، نجرب الترجمة الصوتية (transliteration) في
    # الاتجاهين - مش بس عربي->إنجليزي زي ما افترضنا الأول. لاحظنا حالات
    # (زي "El Fishawy Cafe") فشلت بالإنجليزي بينما نفس المكان بالعربي
    # ("مقهى الفيشاوي") نجح في رحلة تانية. يعني OSM مش متسق: بعض
    # الأماكن مسجلة بالعربي بس، وبعضها بالإنجليزي بس. فبنجرب نحول
    # الاسم للاتجاه التاني (مهما كان الاتجاه الأصلي) ونعيد المحاولة.
    if not results:
        alt_name = _get_alternate_language_name(place_name, city)
        if alt_name and alt_name.strip().lower() != place_name.strip().lower():
            logger.info(
                "'%s' returned nothing in any form, retrying with alternate-language name '%s'",
                place_name, alt_name,
            )
            results = _run_nominatim_query(alt_name)
            if not results:
                results = _run_nominatim_query_no_city(alt_name)
    if not results:
        logger.info("No place found for place_name=%s (cleaned=%s)", place_name, search_name)

        # آخر محاولة قبل ما نستسلم: نجرب نلاقي أقرب مكان من نفس الفئة
        # (مش بالاسم) عبر Overpass. مفيد خصوصًا للأماكن اللي أسماءها
        # التجارية مش مسجلة في OSM (سينمات/مراكز غوص جوه منتجعات، إلخ)
        # لكن فيه أماكن تانية حقيقية من نفس النوع موجودة فعلًا قريبة.
        fallback_place = _search_place_by_category_fallback(
            place_name, city, category,
            exclude_place_ids=exclude_place_ids,
            enable_ai_details=enable_ai_details,
        )
        if fallback_place is not None:
            set_cached(cache_city, cache_key_name, [fallback_place.model_dump()])
            return fallback_place

        set_cached(cache_city, cache_key_name, [])
        return None

    result = results[0]
    address = result.get("address", {})

    result_city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or city
    )
    result_city = normalize_city(result_city)

    lat = float(result["lat"])
    lon = float(result["lon"])

    image = get_place_image(place_name, result_city)
    if not image:
        image = "https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg"

    rating = None
    reviews = None
    if enable_ai_details:
        details = _get_ai_details_safe(place_name, result_city or "")
        rating = details.get("rating")
        reviews = details.get("reviews")

    popularity_score, popularity = _compute_popularity(rating, reviews)

    place_obj = Place(
        name=place_name,
        address=result.get("display_name", ""),
        city=result_city,
        country=address.get("country"),

        rating=rating,
        reviews=reviews,

        popularity_score=popularity_score,
        popularity=popularity,

        latitude=lat,
        longitude=lon,

        google_maps=f"https://www.google.com/maps?q={lat},{lon}",

        image_url=image,
        place_id=f"osm-{result.get('osm_type', 'node')}-{result.get('osm_id')}",
    )

    # ------------------------------------------------------------------
    # Safety net ضد تكرار المكان الحرفي عبر الرحلة: لو Gemini طلب نفس
    # الاسم بالظبط (أو اسم مختلف رجع بنفس place_id) في يومين مختلفين،
    # المسار العادي فوق كان بيرجع نفس المكان تاني من غير أي مانع، لأن
    # exclude_place_ids كانت بتتفحص بس جوه category fallback. هنا
    # بنتحقق منها كمان على نتيجة المسار العادي الناجح: لو الـ place_id
    # ده اتحط في exclude_place_ids قبل كده، منرجعوش تاني - نجرب بدلاً
    # منه أقرب مكان حقيقي من نفس الفئة عبر category fallback. لو حتى
    # الـ fallback فشل أو رجع نفس المكان تاني، نرجع None بدل ما نكرر
    # (أفضل من نشاط بلا تفاصيل عن نشاط مكرر جغرافيًا).
    # ------------------------------------------------------------------
    if exclude_place_ids and place_obj.place_id in exclude_place_ids:
        logger.info(
            "search_place primary result for '%s' duplicates an already-used "
            "place_id=%s across the trip - trying category fallback instead",
            place_name, place_obj.place_id,
        )
        fallback_place = _search_place_by_category_fallback(
            place_name, city, category,
            exclude_place_ids=exclude_place_ids,
            enable_ai_details=enable_ai_details,
        )
        if fallback_place is not None and fallback_place.place_id not in exclude_place_ids:
            return fallback_place

        logger.info(
            "No non-duplicate alternative found for '%s' - returning None "
            "instead of repeating place_id=%s",
            place_name, place_obj.place_id,
        )
        return None

    set_cached(cache_city, cache_key_name, [place_obj.model_dump()])
    return place_obj


@lru_cache(maxsize=200)
def search_places_by_category(
    city: str,
    category: str,
    limit: int = 10,
) -> tuple[Place, ...]:
    """
    بتدور على أماكن حسب الفئة (hotels, restaurants, ...) داخل مدينة،
    باستخدام Overpass API. بتتأكد الأول من الكاش الدائم على القرص قبل
    ما تعمل أي طلب فعلي.
    """
    if category.lower() in IGNORED_CATEGORIES:
        logger.info("Skipping search_places_by_category for: %s", category)
        return tuple()

    # الكاش الدائم بيتخزن كـ list of dicts، فلو لقينا كاش، نحوله لـ Place objects
    cached = get_cached(city, category)
    if cached is not None:
        try:
            return tuple(Place(**item) for item in cached)
        except Exception as e:
            logger.warning("Failed to rebuild Place objects from cache | error=%s", str(e))
            # لو فشل التحويل لأي سبب، كمل عادي واطلب البيانات من جديد

    osm_tags = CATEGORY_OSM_TAGS.get(category)
    if not osm_tags:
        logger.warning("No OSM tag mapping for category=%s", category)
        return tuple()

    coords = _geocode(f"{city}, Egypt")
    if coords is None:
        logger.error("Could not geocode city=%s", city)
        # منخزنش حاجة هنا - فشل الـ geocoding مؤقت وممكن ينجح المرة الجاية
        return tuple()

    lat, lon = coords

    query = _build_overpass_query(lat, lon, osm_tags)
    elements = _query_overpass(query)

    if elements is None:
        # الفرق المهم هنا: elements=None معناها كل سيرفرات Overpass فشلت
        # (timeout, 429, 5xx) - ده فشل شبكة مؤقت، مش "مفيش نتائج فعلاً".
        # منخزنش [] في الكاش الدائم عشان المرة الجاية تحاول تاني بدل ما
        # تفضل عالقة على نتيجة فاضية للأبد.
        logger.warning(
            "Overpass fully failed for category=%s city=%s - NOT caching (will retry next time)",
            category, city
        )
        return tuple()

    if not elements:
        # هنا الحالة التانية: Overpass رد فعلاً بس مفيش عناصر مطابقة -
        # دي نتيجة صحيحة ومستقرة، تستاهل تتخزن في الكاش.
        logger.info("No places found for category=%s city=%s (confirmed empty result)", category, city)
        set_cached(city, category, [])
        return tuple()

    results = []
    seen_names = set()

    for element in elements:
        place_obj = _place_from_osm_element(
            element,
            fallback_city=city,
            trust_fallback_city=True
        )

        if place_obj is None:
            continue

        name = place_obj.name.lower()

        # استبعاد الأماكن الواضح إنها مش مناسبة للسياحة
        BAD_WORDS = (
    "atm",
    "bank",
    "office",
    "clinic",
    "hospital",
    "pharmacy",
    "church",
    "parking",
    "garage",
    "government",
    "police",
    "fuel",
    "petrol",
    "gas",
    "toilet",
    "wc",
    "cemetery",
    "embassy",
    "consulate",
)

        if any(word in name for word in BAD_WORDS):
            continue

        dedup_key = name
        if dedup_key in seen_names:
            continue

        seen_names.add(dedup_key)

        results.append(place_obj)

        if len(results) >= limit:
            break
    # ترتيب النتائج حسب جودة الاسم
        GOOD_WORDS = (
            "hotel",
            "resort",
            "palace",
            "hilton",
            "marriott",
            "sofitel",
            "steigenberger",
            "sheraton",
            "museum",
            "temple",
            "park",
            "mall",
            "restaurant",
            "cafe",
        )

        def score(place: Place):
            name = place.name.lower()

            s = 0

            # الأماكن اللي اسمها معروف
            for word in GOOD_WORDS:
                if word in name:
                    s += 20

            # وجود عنوان
            if place.address:
                s += 5

            # وجود صورة
            if "No_image_available" not in place.image_url:
                s += 5

            return s


    results.sort(key=score, reverse=True)

    # بنخزن في الكاش الدائم كـ list of dicts عشان يبقى قابل لل JSON serialization
    set_cached(category=category, city=city, data=[p.model_dump() for p in results])

    return tuple(results)