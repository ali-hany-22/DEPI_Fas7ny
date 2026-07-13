"""
سكريبت تصحيح بيانات لمرة واحدة - شغّله من روت المشروع بالأمر:

    python fix_data.py

بيصحح:
  1) الخطأ الإملائي "فادق سما العريش" -> "فندق سما العريش" (provider id=2)
  2) حالة الخدمة المرتبطة بيه من disabled -> active

بعد التشغيل، البحث عن "فندق سما العريش" المفروض يلاقي provider id=2
لأنه هو اللي معاه خدمة فعلية.

ملحوظة: provider id=1 معندوش أي خدمات، فمش هيظهر في نتائج البحث
حتى لو اسمه صح - محتاج تضيفله خدمة من الـ Dashboard لو ده provider
حقيقي منفصل، أو تمسحه لو كان اتعمل بالغلط (duplicate).
"""

from app.db.session import SessionLocal
from app.models.provider import ProviderProfile
from app.models.service import Service, ServiceStatus

db = SessionLocal()

# 1) تصحيح الاسم الغلط
provider = db.query(ProviderProfile).filter(ProviderProfile.id == 2).first()
if provider:
    print(f"قبل التصحيح: {provider.business_name!r}")
    provider.business_name = "فندق سما العريش"
    print(f"بعد التصحيح: {provider.business_name!r}")

# 2) تفعيل الخدمة المعطلة
service = db.query(Service).filter(Service.provider_id == 2).first()
if service:
    print(f"قبل التفعيل: status={service.status}")
    service.status = ServiceStatus.active
    print(f"بعد التفعيل: status={service.status}")

db.commit()
print("\nتم الحفظ بنجاح.")

db.close()