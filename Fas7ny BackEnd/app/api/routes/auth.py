"""
Endpoints تسجيل الدخول والتسجيل الخاصة بالسياح (المستخدم العادي).

نفس نمط app/api/provider_auth.py بالظبط، بس من غير خطوة إنشاء
ProviderProfile - السائح محتاج بس صف في جدول users بـ
role=UserRole.tourist.

مسار الـ router تحت /auth (من غير /provider) عشان يبقى واضح إنه
منفصل منطقيًا عن auth بتاع مزودي الخدمة، حتى لو الجدول (users) واحد.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.auth import TouristRegisterRequest, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register_tourist(payload: TouristRegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="البريد الإلكتروني مستخدم بالفعل")

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
        phone=payload.phone,
        role=UserRole.tourist,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return TokenResponse(access_token=token, role=user.role.value)


@router.post("/login", response_model=TokenResponse)
def login_tourist(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="البريد الإلكتروني أو كلمة المرور غير صحيحة")

    # بنسمح بالدخول من هنا لأي حساب مش provider (يعني tourist أو
    # admin)، عشان محدش "يتحبس" برة النظام لو حسابه مش provider.
    # حساب الـ provider نفسه لازم يدخل من /provider/auth/login عشان
    # الـ 403 هناك توضحله إنه لازم يستخدم بوابة المزودين.
    if user.role == UserRole.provider:
        raise HTTPException(
            status_code=403,
            detail="هذا حساب مزود خدمة، سجّل الدخول من صفحة مزودي الخدمة",
        )

    token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return TokenResponse(access_token=token, role=user.role.value)