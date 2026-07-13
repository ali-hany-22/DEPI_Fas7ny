const API = "http://127.0.0.1:8000";

/**
 * خطأ مخصص بيحمل معلومات كافية للفرونت يقرر يعرض إيه للمستخدم:
 * - status: كود الـ HTTP (503 = مشغول مؤقتًا، 500 = خطأ غير متوقع، 422 = بيانات غير صالحة)
 * - detail: الرسالة العربية الجاهزة من الباك اند (planner_routes.py بيرجعها دايمًا نص واضح، مش تفاصيل تقنية)
 * - isRetryable: هل منطقي نقترح على المستخدم يجرب تاني فورًا
 */
export class TripGenerationError extends Error {
  constructor(status, detail) {
    super(detail || "حدث خطأ أثناء إنشاء الرحلة")
    this.name = "TripGenerationError"
    this.status = status
    this.detail = detail
    // 503 = الخدمة مشغولة مؤقتًا (كل مصادر الـ AI فشلت) - يستاهل تجربة تانية
    // 422 = بيانات الطلب نفسها فيها مشكلة - إعادة المحاولة بنفس البيانات مش هتفيد
    // 500 / أي حاجة تانية = خطأ غير متوقع
    this.isRetryable = status === 503
  }
}

export async function generateTrip(data) {
  let response
  try {
    response = await fetch(`${API}/planner/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    })
  } catch (networkError) {
    // فشل الـ fetch نفسه (السيرفر مش شغال، مفيش نت، CORS...) - مش رد
    // من الباك اند خالص، فبنفرّقه عن أخطاء الـ HTTP العادية
    throw new TripGenerationError(
      0,
      "تعذر الاتصال بالسيرفر. تأكد إن اتصالك بالإنترنت شغال وحاول تاني."
    )
  }

  if (!response.ok) {
    let detail = "حدث خطأ أثناء إنشاء الرحلة. حاول مرة أخرى."
    try {
      const body = await response.json()
      // FastAPI's HTTPException بيرجع { "detail": "..." } - ده الشكل
      // اللي planner_routes.py بيضمنه دايمًا (رسالة عربية جاهزة،
      // مفيش أي تفاصيل تقنية داخلية)
      if (body?.detail) detail = body.detail
    } catch {
      // الرد مش JSON أصلاً (نادر، ممكن لو حصل خطأ قبل FastAPI نفسه
      // زي proxy/gateway error) - نسيب الرسالة الافتراضية
    }
    throw new TripGenerationError(response.status, detail)
  }

  return await response.json()
}