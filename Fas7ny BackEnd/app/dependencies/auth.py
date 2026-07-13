"""
Dependencies بتتحقق من الـ JWT وتجيب اليوزر الحالي، وتتأكد إن
اليوزر ده فعلاً provider قبل ما تسمحله يدخل على أي endpoint من
endpoints الداشبورد.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.provider import ProviderProfile

# tokenUrl بس بيستخدم لتوثيق Swagger UI، مش بيعمل أي حاجة فعلية هنا
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/provider/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="بيانات الدخول غير صالحة أو منتهية",
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_error

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_error

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None or not user.is_active:
        raise credentials_error

    return user


def get_current_provider(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProviderProfile:
    """
    بيتأكد إن اليوزر role=provider، وبيرجع الـ ProviderProfile
    بتاعه مباشرة (مش الـ User) عشان كل الـ endpoints بتاعت
    الداشبورد محتاجة provider_id مش user_id.
    """
    if current_user.role != UserRole.provider:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="الوصول مقصور على مزودي الخدمة فقط",
        )

    profile = (
        db.query(ProviderProfile)
        .filter(ProviderProfile.user_id == current_user.id)
        .first()
    )
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="لا يوجد ملف مزود خدمة مرتبط بهذا الحساب",
        )

    return profile
