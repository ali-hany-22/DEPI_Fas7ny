import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.planner import router as planner_router
from app.api.routes.recommendations import router as recommendations_router
from app.api.routes.cached_places import router as cached_places_router
from app.api.routes.chat import router as chat_router
from app.core.config import settings
from app.api.routes.search import router as search_router
from app.api.routes.bookings import router as bookings_router

# Provider Dashboard
from app.db.session import Base, engine
import app.models  # noqa: F401

from app.api.routes.provider_auth import router as provider_auth_router
from app.api.routes.provider_dashboard import router as provider_dashboard_router
from app.api.routes.provider_services import router as provider_services_router
from app.api.routes.provider_analytics import router as provider_analytics_router
from app.api.routes.provider_support import router as provider_support_router
from app.api.routes.public_tracking import router as public_tracking_router

# Tourist Auth (السائح العادي - منفصل منطقيًا عن provider_auth)
from app.api.routes.auth import router as auth_router

# لازم يتحط هنا (مش في run.py) لأن uvicorn --reload=True بيشغل السيرفر
# الفعلي في subprocess منفصل بيحمّل app.main:app من جديد - أي إعداد
# logging في run.py نفسه معندوش تأثير على الـ subprocess ده.
#
# من غير السطر ده، كل الـ logger.info/logger.warning بتاعت
# enrichment_service/places_service/gemini_place_service كانت بتحصل
# فعليًا بس ملهاش أي handler يطبعها في التيرمنال - يعني الأخطاء
# (زي "No place found for...", "Geocoding failed...", "GeminiPlaceService
# quota exhausted...") كانت بتضيع بصمت وتفضل الـ 200 OK بس هو الظاهر.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION
)

# الفرونت (Vue) شغال على origin مختلف (زي localhost:5173 وقت التطوير)،
# فمحتاجين CORS عشان المتصفح يسمح للطلبات توصل للـ API. في الإنتاج،
# استبدل "*" بدومين الفرونت الفعلي بدل ما تسيبه مفتوح للكل.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(planner_router)
app.include_router(recommendations_router)
app.include_router(cached_places_router)
app.include_router(chat_router)
app.include_router(search_router)
app.include_router(bookings_router)

# Tourist Auth
app.include_router(auth_router)

# Provider Dashboard
app.include_router(provider_auth_router)
app.include_router(provider_dashboard_router)
app.include_router(provider_services_router)
app.include_router(provider_analytics_router)
app.include_router(provider_support_router)
app.include_router(public_tracking_router)

# إنشاء جداول SQLite
Base.metadata.create_all(bind=engine)
@app.get("/")
def home():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "Running"
    }