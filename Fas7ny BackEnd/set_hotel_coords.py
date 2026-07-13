"""
سكريبت لحط إحداثيات (lat/lng) لفندق "سما العريش" التجريبي، عشان
يظهر على الخريطة. عدّل القيم لو عندك إحداثيات فعلية أدق.

شغّله من روت المشروع:

    python set_hotel_coords.py
"""

from app.db.session import SessionLocal
from app.models.provider import ProviderProfile

db = SessionLocal()

# إحداثيات تقريبية لمدينة العريش (وسط المدينة، كورنيش البحر)
provider = db.query(ProviderProfile).filter(ProviderProfile.id == 2).first()

if provider:
    provider.latitude = 31.1316
    provider.longitude = 33.7984
    db.commit()
    print(f"تم تحديث إحداثيات {provider.business_name}: ({provider.latitude}, {provider.longitude})")
else:
    print("لم يتم العثور على provider id=2")

db.close()