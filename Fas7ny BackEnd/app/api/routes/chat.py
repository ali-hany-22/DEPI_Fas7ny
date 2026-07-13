"""
app/api/routes/chat.py

Endpoint للشات بوت: بياخد رسالة نصية حرة من المستخدم (زي "فنادق في
الأقصر؟" أو "عايز أعرف مطاعم في الغردقة")، ويرجع رد نصي + قائمة أماكن
حقيقية لو الرسالة بتطلب أماكن.

طريقة العمل:
  1. نفهم الرسالة عبر Gemini (نفس الـ rotation الموجودة في
     GeminiPlaceService) ونطلع منها city + category بشكل منظم.
  2. لو الرسالة مش بتطلب أماكن خالص (سؤال عام/تحية)، نرجع رد نصي بسيط
     من غير أي بحث.
  3. لو بتطلب أماكن: نستخدم search_places_by_category اللي أصلًا بتتأكد
     من الكاش الدائم الأول (places_cache.json) قبل أي بحث حي - يعني لو
     حد سأل عن نفس المدينة/الفئة قبل كده (من أي رحلة سابقة أو رسالة
     شات سابقة)، هيرجع فورًا من غير أي نداء شبكة.
  4. لو الكاش فاضي، search_places_by_category بتعمل بحث حي عبر Overpass
     وتخزّن النتيجة تلقائيًا - يعني المرة الجاية أي حد يسأل نفس السؤال
     (حتى لو مستخدم مختلف) هياخد الرد فورًا من الكاش.

ده بيخلي الشات بوت "يتعلم" تدريجيًا من غير أي endpoint إضافي أو تكرار
منطق - بنعيد استخدام نفس الكاش والبحث اللي الـ Planner أصلًا بيستخدمهم.
"""

import json
import logging

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.places_service import search_places_by_category, CATEGORY_OSM_TAGS
from app.services.gemini_place_service import GeminiPlaceService
from app.city_mapping import normalize_city, TOURISTIC_CITIES

logger = logging.getLogger("chat_routes")

router = APIRouter(prefix="/chat", tags=["chat"])

# الفئات المتاحة فعليًا للبحث (نفس مفاتيح CATEGORY_OSM_TAGS في
# places_service.py) - بنمررها لـ Gemini عشان يختار من بينها بس.
AVAILABLE_CATEGORIES = list(CATEGORY_OSM_TAGS.keys())


class ChatMessageRequest(BaseModel):
    message: str


class ChatPlaceResult(BaseModel):
    name: str
    address: str | None = None
    city: str | None = None
    rating: float | None = None
    reviews: int | None = None
    popularity: str = "Low"
    latitude: float
    longitude: float
    google_maps: str
    image_url: str | None = None


class ChatMessageResponse(BaseModel):
    reply: str
    city: str | None = None
    category: str | None = None
    places: list[ChatPlaceResult] = []
    from_cache: bool = False


def _parse_chat_intent(message: str) -> dict:
    """
    بتستخدم نفس الـ rotation بتاعت GeminiPlaceService (Gemini + Gemini
    alt + Groq) عشان تفهم رسالة اليوزر الحرة وتطلع:
      - wants_places: هل الرسالة بتطلب أماكن فعلًا؟
      - city: اسم المدينة (لو موجود) بأي صيغة (عربي/إنجليزي)
      - category: واحدة من AVAILABLE_CATEGORIES (لو قدرنا نحددها)

    بترجع dict بقيم افتراضية آمنة (wants_places=False) لو كل مصادر AI
    فشلت أو الرد مش JSON صالح - عشان الشات بوت يفضل شغال (برد عام) حتى
    لو النية معرفتش تتحدد.
    """
    categories_str = ", ".join(AVAILABLE_CATEGORIES)
    cities_str = ", ".join(TOURISTIC_CITIES)

    prompt = f"""
You are an intent parser for a travel chatbot about Egypt.

Given a user's free-text message (in Arabic or English), extract:
- wants_places: true if the user is asking to find/see/recommend actual
  places (hotels, restaurants, attractions, etc), false if it's small
  talk, a general question, or anything else.
- city: the Egyptian city mentioned, normalized to one of these exact
  values if possible: {cities_str}. Use null if no city is mentioned or
  recognized.
- category: exactly one of these values if the message matches:
  {categories_str}. Use null if none clearly match.

User message:
{message}

Return ONLY valid JSON, no markdown, no explanation:
{{
    "wants_places": true or false,
    "city": "string or null",
    "category": "string or null"
}}
"""

    def _parse_json_response(text: str) -> dict | None:
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        try:
            data = json.loads(cleaned)
            if not isinstance(data, dict):
                return None
            return {
                "wants_places": bool(data.get("wants_places", False)),
                "city": data.get("city") or None,
                "category": data.get("category") or None,
            }
        except (json.JSONDecodeError, TypeError):
            return None

    # بنستخدم نفس آلية الـ rotation الموجودة أصلًا - بنعمل استدعاء
    # مباشر بنفس أسلوب GeminiPlaceService._try_gemini_key/_try_groq
    # (مش بننادي get_place_details لأنها مبنية لبرومبت مختلف تمامًا).
    from app.core.config import settings

    providers = [
        ("GEMINI_ALT2_API_KEY", settings.GEMINI_ALT_API_KEY),
        ("GEMINI_API_KEY", settings.GEMINI_API_KEY),
        ("GEMINI_ALT_API_KEY", settings.GEMINI_ALT_API_KEY),
    ]

    for key_label, api_key in providers:
        if not api_key:
            continue
        result = GeminiPlaceService._try_gemini_key(
            api_key, prompt, max_retries=2, key_label=key_label,
            parser=_parse_json_response,
        )
        if result is not None:
            return result

    groq_result = GeminiPlaceService._try_groq(prompt, parser=_parse_json_response)
    if groq_result is not None:
        return groq_result

    logger.warning("Chat intent parsing failed for all providers | message=%s", message)
    return {"wants_places": False, "city": None, "category": None}


@router.post("/message", response_model=ChatMessageResponse)
def send_chat_message(payload: ChatMessageRequest):
    """
    نقطة الدخول الوحيدة للشات بوت. بتاخد رسالة، تفهمها، وترجع رد + أماكن
    (لو الرسالة بتطلب أماكن).
    """
    message = payload.message.strip()

    if not message:
        return ChatMessageResponse(reply="تقدر تسألني عن فنادق أو مطاعم أو أماكن سياحية في أي مدينة مصرية.")

    intent = _parse_chat_intent(message)

    if not intent["wants_places"]:
        return ChatMessageResponse(
            reply="ممكن أساعدك تلاقي فنادق، مطاعم، أو أماكن سياحية في أي مدينة مصرية - جرّب تسألني مثلاً 'فنادق في الأقصر' أو 'مطاعم في الغردقة'.",
        )

    city = intent["city"]
    category = intent["category"]

    if not city:
        return ChatMessageResponse(
            reply="تمام، بس محتاج أعرف في أي مدينة بالظبط؟",
            category=category,
        )

    if not category:
        return ChatMessageResponse(
            reply=f"تمام، عايز أدور على إيه في {city}؟ فنادق، مطاعم، أماكن سياحية، وللا حاجة تانية؟",
            city=city,
        )

    normalized_city = normalize_city(city) or city

    try:
        results = search_places_by_category(normalized_city, category, limit=6)
    except Exception as e:
        logger.error(
            "Chat place search failed | city=%s category=%s error=%s",
            normalized_city, category, str(e),
        )
        return ChatMessageResponse(
            reply="حصل خطأ أثناء البحث، جرّب تاني كمان شوية.",
            city=normalized_city,
            category=category,
        )

    if not results:
        return ChatMessageResponse(
            reply=f"معنديش بيانات كافية عن {category} في {normalized_city} دلوقتي. جرّب مدينة تانية أو فئة مختلفة.",
            city=normalized_city,
            category=category,
        )

    category_labels = {
        "hotels": "فنادق",
        "restaurants": "مطاعم",
        "cafes": "كافيهات",
        "museums": "متاحف",
        "parks": "حدائق",
        "shopping": "أماكن تسوق",
        "beaches": "شواطئ",
        "entertainment": "أماكن ترفيهية",
    }
    label = category_labels.get(category, category)

    places = [
        ChatPlaceResult(
            name=p.name,
            address=p.address,
            city=p.city,
            rating=p.rating,
            reviews=p.reviews,
            popularity=p.popularity,
            latitude=p.latitude,
            longitude=p.longitude,
            google_maps=p.google_maps,
            image_url=p.image_url,
        )
        for p in results
    ]

    return ChatMessageResponse(
        reply=f"لقيتلك {len(places)} من أفضل {label} في {normalized_city}:",
        city=normalized_city,
        category=category,
        places=places,
    )