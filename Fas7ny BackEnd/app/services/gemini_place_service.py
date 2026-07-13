import json
import logging
import time

from google import genai
from google.genai.errors import ServerError, ClientError
from groq import Groq

from app.core.config import settings


logger = logging.getLogger("gemini_place_service")

# ---------------------------------------------------------------------------
# Rotation عبر أكتر من مزوّد/مفتاح
# ---------------------------------------------------------------------------
# بعد المقارنة: Groq بيدّي كوتة أسخى بكتير على الـ free tier (آلاف
# الطلبات في اليوم حسب الموديل) مقارنة بـ Gemini Free Tier (20
# request/day بس لكل مفتاح لكل موديل). عشان كده Groq بقى المحاولة
# الأولى دلوقتي، و Gemini (الأساسي ثم الاحتياطي) بقوا fallback لو
# Groq فشل أو رجع نتيجة مرفوضة. الترتيب الجديد:
#   1. GROQ_API_KEY         (المحاولة الأولى - كوتة يومية أعلى بكتير)
#   2. GEMINI_API_KEY       (fallback أول لو Groq فشل)
#   3. GEMINI_ALT_API_KEY   (fallback تاني/أخير)
#
# لو مفتاح Gemini معين ضرب quota (429) أو رجع رفض واضح، بننتقل للمحاولة
# اللي بعده فورًا (من غير أي sleep/retry على نفس المفتاح المستهلك). الـ
# exponential backoff (retry على نفس المفتاح) بيتطبق بس على أخطاء
# ServerError (503 مثلاً) اللي غالبًا مؤقتة وممكن تتحل بإعادة نفس الطلب.

_gemini_clients: dict[str, genai.Client] = {}


def _get_gemini_client(api_key: str) -> genai.Client:
    """بنعمل cache لكل genai.Client حسب المفتاح عشان منعيدش تهيئته كل مرة."""
    if api_key not in _gemini_clients:
        _gemini_clients[api_key] = genai.Client(api_key=api_key)
    return _gemini_clients[api_key]


def _is_quota_error(e: Exception) -> bool:
    """
    بتحدد لو الخطأ ده quota/rate-limit (429) - في الحالة دي مفيش أي
    فايدة من إعادة المحاولة على نفس المفتاح، لازم ننتقل للمفتاح/المزوّد
    اللي بعده فورًا.
    """
    if isinstance(e, ClientError):
        status = getattr(e, "status_code", None) or getattr(e, "code", None)
        if status == 429:
            return True
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
            return True
    return "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower()


def _build_prompt(place_name: str, city: str) -> str:
    return f"""
You are an expert about places in Egypt.

Return ONLY valid JSON.

Place: {place_name}
City: {city}

Return:

{{
    "rating": number,
    "reviews": integer
}}

Rules:
- Use real public information.
- rating must be between 0 and 5.
- reviews must be the approximate number of Google reviews.
- If you don't know:

{{
    "rating": null,
    "reviews": null
}}

No markdown. No explanation. Only JSON.
"""


def _parse_json_response(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)


class GeminiPlaceService:

    @staticmethod
    def _try_gemini_key(
        api_key: str,
        prompt: str,
        max_retries: int,
        key_label: str,
        parser=_parse_json_response,
    ):
        """
        بتجرب مفتاح Gemini واحد بالتحديد. بترجع نتيجة الـ parser عند
        النجاح، أو None لو الكوتة اتضربت أو فشل غير متوقع (عشان نعرف
        ننتقل للمفتاح/المزوّد التالي).
        """
        client = _get_gemini_client(api_key)

        for attempt in range(max_retries):
            try:
                response = client.models.generate_content(
                    model=settings.GEMINI_MODEL,
                    contents=prompt,
                )
                return parser(response.text)

            except ServerError as e:
                # أخطاء سيرفر مؤقتة (503 مثلاً) - يستاهل نعيد نفس المفتاح
                if attempt < max_retries - 1:
                    logger.warning(
                        "Gemini (%s) server error, retrying (attempt %s/%s) | error=%s",
                        key_label, attempt + 1, max_retries, str(e),
                    )
                    time.sleep(2 ** attempt)
                    continue
                logger.warning(
                    "Gemini (%s) failed after %s attempts (server error) | error=%s",
                    key_label, max_retries, str(e),
                )
                return None

            except Exception as e:
                if _is_quota_error(e):
                    logger.warning(
                        "Gemini (%s) quota exhausted, moving to next provider | error=%s",
                        key_label, str(e),
                    )
                    return None

                logger.error(
                    "Gemini (%s) place lookup failed: %s",
                    key_label, str(e),
                )
                return None

        return None

    @staticmethod
    def _try_groq(prompt: str, parser=_parse_json_response):
        """
        المحاولة الأولى دلوقتي - Groq عنده كوتة يومية أسخى بكتير من
        Gemini Free Tier. بترجع None لو فشلت لأي سبب (عشان نكمل على
        Gemini كـ fallback).
        """
        try:
            groq_client = Groq(api_key=settings.GROQ_API_KEY)

            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0,
            )
            text = completion.choices[0].message.content
            return parser(text)

        except Exception as e:
            logger.warning(
                "Groq primary attempt failed, falling back to Gemini | error=%s",
                str(e),
            )
            return None

    @staticmethod
    def get_place_details(
        place_name: str,
        city: str,
        max_retries: int = 3,
    ) -> dict:
        """
        بتجيب rating/reviews تقديرية لمكان، بمحاولة مصادر متعددة بالترتيب:
        1. GROQ_API_KEY (المحاولة الأولى - كوتة يومية أعلى بكتير)
        2. GEMINI_API_KEY (fallback أول لو Groq فشل)
        3. GEMINI_ALT_API_KEY (fallback أخير)

        بترجع {"rating": None, "reviews": None} لو كل المصادر فشلت -
        نفس الشكل القديم بالظبط، فمفيش أي تغيير مطلوب في الكود اللي
        بينادي الدالة دي.
        """
        prompt = _build_prompt(place_name, city)

        # المحاولة الأولى: Groq
        groq_result = GeminiPlaceService._try_groq(prompt)
        if groq_result is not None:
            return groq_result

        # Fallback: Gemini (الأساسي ثم الاحتياطي)
        providers = [
            ("GEMINI_API_KEY", settings.GEMINI_API_KEY),
            ("GEMINI_ALT_API_KEY", settings.GEMINI_ALT_API_KEY),
        ]

        for key_label, api_key in providers:
            if not api_key:
                continue

            result = GeminiPlaceService._try_gemini_key(
                api_key, prompt, max_retries, key_label,
            )
            if result is not None:
                return result

        logger.warning(
            "Couldn't fetch place details for %s (all providers exhausted)",
            place_name,
        )

        return {
            "rating": None,
            "reviews": None,
        }

    @staticmethod
    def get_alternate_language_place_name(
        place_name: str,
        city: str,
        max_retries: int = 2,
    ) -> str | None:
        """
        بتستخرج اسم المكان بلغة مختلفة عن اللي دخل بيها:
        - لو الاسم عربي (زي "بافلو برجر") -> بترجع أقرب اسم إنجليزي رسمي
          ("Buffalo Burger").
        - لو الاسم إنجليزي (زي "El Fishawy Cafe") -> بترجع أقرب اسم
          عربي شائع ("مقهى الفيشاوي").

        السبب: OSM/Nominatim مش متسق في لغة تسجيل الأماكن - بعضها
        بالعربي بس، وبعضها بالإنجليزي بس. مفيش طريقة نعرف مقدمًا أي
        اتجاه هيشتغل، فبنسيب الـ prompt يتعرف على لغة الإدخال ويرجع
        عكسها.

        بتستخدم نفس الـ rotation (Groq -> Gemini -> Gemini alt) وبترجع
        None لو كل المصادر فشلت أو الرد مش منطقي (فاضي/طويل جدًا).
        """
        prompt = f"""
You are an expert about places, restaurants, malls, and hotels in Egypt.

You will be given a place name in either Arabic or English.

- If the name is in Arabic, return its most common official English
  name as used on maps and review sites (Google Maps, OpenStreetMap,
  TripAdvisor, etc). If it's an international chain, return the
  chain's standard English name.
- If the name is in English, return its most common Arabic name as
  written locally in Egypt (the way an Egyptian would search for it
  or the way it's commonly labeled on Arabic maps/signage).

Place name: {place_name}
City: {city}

Return ONLY the alternate-language name as plain text. No quotes. No explanation. No markdown. No JSON.
If you genuinely don't know, return exactly: UNKNOWN
"""

        def _parse_plain_text(text: str) -> str | None:
            cleaned = text.strip().strip('"').strip("'")
            if not cleaned or cleaned.upper() == "UNKNOWN":
                return None
            # رد منطقي المفروض يكون قصير (اسم مكان مش فقرة)
            if len(cleaned) > 120:
                return None
            return cleaned

        # المحاولة الأولى: Groq
        groq_result = GeminiPlaceService._try_groq(prompt, parser=_parse_plain_text)
        if groq_result is not None:
            return groq_result

        # Fallback: Gemini (الأساسي ثم الاحتياطي)
        providers = [
            ("GEMINI_API_KEY", settings.GEMINI_API_KEY),
            ("GEMINI_ALT_API_KEY", settings.GEMINI_ALT_API_KEY),
        ]

        for key_label, api_key in providers:
            if not api_key:
                continue

            result = GeminiPlaceService._try_gemini_key(
                api_key, prompt, max_retries, key_label,
                parser=_parse_plain_text,
            )
            if result is not None:
                return result

        return None