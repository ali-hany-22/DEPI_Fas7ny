from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class TripRequest(BaseModel):
    # المدن المختارة
    destinations: List[str] = Field(
        ...,
        min_length=1,
        description="Selected destinations"
    )

    # نوع الرحلة
    trip_type: str = Field(
        ...,
        description="Historical, Beach, Adventure, Family, Safari..."
    )

    # مكان الإقامة
    accommodation: str = Field(
        ...,
        description="Hotel, Apartment, Resort, Hostel..."
    )

    # الميزانية اليومية بالجنيه
    daily_budget: int = Field(
        ...,
        gt=0,
        description="Daily budget in EGP"
    )

    # المواصلات
    transport: str = Field(
        ...,
        description="Car, Bus, Train, Flight..."
    )

    # الأكل
    food_preferences: List[str] = Field(
        default_factory=list
    )

    # عدد الأيام
    days: int = Field(
        ...,
        ge=1,
        le=30
    )

    # عدد الأفراد
    people: int = Field(
        ...,
        ge=1
    )

    # تاريخ البداية (اختياري)
    start_date: Optional[date] = None
    
    # هل المستخدم عنده أطفال؟
    has_children: bool = False

    # عدد الأطفال
    children_count: int = 0

    # مستوى الرحلة
    travel_style: str = "Balanced"

    # اهتمامات إضافية
    interests: List[str] = Field(
        default_factory=list
    )

    # لغة الرد
    language: str = "Arabic"

    # أي ملاحظات إضافية
    notes: Optional[str] = None