"""
إعداد الاتصال بقاعدة البيانات (SQLite via SQLAlchemy).

استخدمنا SQLite بدل JSON عشان الداشبورد محتاج queries حقيقية
(حساب KPIs، فلترة حجوزات بتاريخ، علاقات بين جداول). لو المشروع كبر
وبقينا محتاجين Postgres، التغيير هيبقى مجرد تعديل DATABASE_URL
في .env من غير أي تعديل في الكود.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

# check_same_thread=False لازم لـ SQLite عشان FastAPI بيستخدم
# threads متعددة للـ requests، وSQLite افتراضيًا بيمنع مشاركة
# الاتصال بين threads مختلفة.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency بتفتح session وتقفلها تلقائيًا لكل request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
