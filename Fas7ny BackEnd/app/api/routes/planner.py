import json
import logging

from fastapi import APIRouter, HTTPException
from google.genai.errors import ServerError, ClientError
from pydantic import ValidationError

from app.models.request import TripRequest
from app.services.planner_service import generate_trip

logger = logging.getLogger("planner_routes")

router = APIRouter(
    prefix="/planner",
    tags=["Trip Planner"]
)

# كل الأنواع دي معناها فعليًا "كل مصادر الـ AI فشلت" - مش بس Gemini
# (ServerError/ClientError)، لكن كمان لما Groq نفسه يكون آخر محاولة
# وفشل بإرجاع JSON غير صالح (json.JSONDecodeError) أو JSON صالح لكن
# مش مطابق لـ TripPlan schema (pydantic ValidationError). اتأكدنا من
# ده بمراجعة _generate_with_groq() في gemini_service.py مباشرة.
AI_UNAVAILABLE_ERRORS = (ServerError, ClientError, json.JSONDecodeError, ValidationError)


@router.post("/generate")
async def generate(request: TripRequest):
    """
    بيولّد خطة رحلة كاملة. الأخطاء الجزئية (فشل جلب صورة/rating لمكان
    معين، أو فشل الطقس ليوم معين) متعالجة بالفعل جوه enrich_trip()
    ومبتوصلش هنا - الرحلة بترجع كاملة مع بعض الحقول الفارغة بس.

    اللي ممكن يوصل هنا فعليًا هو فشل توليد الخطة بالكامل. ده بيحصل في
    حالتين حسب مراجعة gemini_service.py:
      1) كل مفاتيح Gemini فشلوا بـ ServerError/ClientError، وGroq
         نفسه رمى نفس النوعين (نادر لكن ممكن لو في مشكلة شبكة).
      2) كل مفاتيح Gemini فشلوا، وGroq رجع رد لكن مش JSON صالح أو مش
         مطابق لـ TripPlan schema (json.JSONDecodeError أو
         pydantic.ValidationError من _generate_with_groq).

    في الحالتين دول منسربش تفاصيل تقنية داخلية (اسم الـ exception،
    stack trace، أي جزء من الـ API keys) للمستخدم - بنرجع رسالة عربية
    واضحة بس، ونسجل التفاصيل الكاملة في اللوج عشان التشخيص.
    """
    try:
        trip = generate_trip(request.model_dump(mode="json"))
        return trip

    except AI_UNAVAILABLE_ERRORS as e:
        logger.error(
            "All AI providers failed for trip generation | destinations=%s | error_type=%s | error=%s",
            request.destinations, type(e).__name__, str(e),
        )
        raise HTTPException(
            status_code=503,
            detail="الخدمة مشغولة جدًا حاليًا، برجاء المحاولة تاني بعد لحظات.",
        )

    except Exception as e:
        # يشمل حالة "raise Exception('Failed to generate trip.')" العامة
        # اللي بترجع من planner_service.py لو trip رجع None بطريقة ما،
        # وأي حاجة تانية غير متوقعة تمامًا.
        logger.exception(
            "Unexpected error during trip generation | destinations=%s",
            request.destinations,
        )
        raise HTTPException(
            status_code=500,
            detail="حدث خطأ غير متوقع أثناء إنشاء الرحلة، برجاء المحاولة تاني.",
        )