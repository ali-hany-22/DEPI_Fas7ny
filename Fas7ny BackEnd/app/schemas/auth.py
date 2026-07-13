"""
Schemas الخاصة بالـ Auth: التسجيل، الدخول، والـ token اللي بيرجع.
"""

from pydantic import BaseModel, EmailStr

from app.models.provider import BusinessType


class TouristRegisterRequest(BaseModel):
    """
    طلب تسجيل سائح عادي جديد. أبسط من ProviderRegisterRequest لأنه
    مش محتاج بيانات نشاط تجاري - بس بيانات الحساب الأساسية.
    """
    email: EmailStr
    password: str
    full_name: str
    phone: str | None = None


class ProviderRegisterRequest(BaseModel):
    """
    طلب تسجيل مزود خدمة جديد. بيعمل حاجتين في خطوة واحدة:
    إنشاء User (role=provider) + إنشاء ProviderProfile مربوط بيه.
    """
    email: EmailStr
    password: str
    full_name: str
    phone: str | None = None

    business_name: str
    business_name_en: str | None = None
    business_type: BusinessType = BusinessType.hotel
    city: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class ProviderProfileOut(BaseModel):
    id: int
    business_name: str
    business_name_en: str | None
    business_type: BusinessType
    city: str | None
    is_verified: bool
    logo_url: str | None

    class Config:
        from_attributes = True