"""
Endpoints تسجيل الدخول والتسجيل الخاصة بمزودي الخدمة.

مسار الـ router كله تحت /provider عشان يبقى واضح إنه منفصل
منطقيًا عن أي auth بتاع السائحين لو اتعمل بعدين، حتى لو الجدول
(users) واحد.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.provider import ProviderProfile
from app.schemas.auth import ProviderRegisterRequest, LoginRequest, TokenResponse

router = APIRouter(prefix="/provider/auth", tags=["Provider Auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_provider(payload: ProviderRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مستخدم بالفعل")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        phone=payload.phone,
        role=UserRole.provider,
    )
    db.add(user)
    db.flush()  # عشان ناخد user.id من غير ما نعمل commit كامل لسه

    profile = ProviderProfile(
        user_id=user.id,
        business_name=payload.business_name,
        business_name_en=payload.business_name_en,
        business_type=payload.business_type,
        city=payload.city,
    )
    db.add(profile)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return TokenResponse(access_token=token, role=user.role.value)


@router.post("/login", response_model=TokenResponse)
def login_provider(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="البريد الإلكتروني أو كلمة المرور غير صحيحة")

    if user.role != UserRole.provider:
        raise HTTPException(status_code=403, detail="هذا الحساب ليس حساب مزود خدمة")

    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return TokenResponse(access_token=token, role=user.role.value)
