from typing import List
from pydantic import BaseModel
from app.models.weather import Weather
from app.models.place import Place


class Activity(BaseModel):
    time: str
    place: str
    city: str
    category: str
    description: str
    estimated_cost: int
    duration: str

    # ملحوظة مهمة: الحقل ده مش بيتملي هنا في اللحظة اللي Gemini بيرجّع
    # فيها الخطة. enrichment_service.py هو اللي بيحقنه بعدين مباشرة في
    # الـ dict (activity["place_details"] = place.model_dump()) قبل ما
    # يرجع trip كـ dict خام من /planner/generate (مفيش response_model
    # على الـ endpoint، فمفيش أي قص أو validation بيحصل).
    #
    # يبقى None لو النشاط من IGNORED_ACTIVITY_CATEGORIES (transport,
    # taxi, train...) أو لو search_place() فشلت في إيجاد المكان.
    place_details: Place | None = None


class DayPlan(BaseModel):
    day: int
    title: str
    total_cost: float
    activities: List[Activity]
    weather: Weather | None = None


class BudgetBreakdown(BaseModel):
    accommodation: float
    transportation: float
    food: float
    attractions: float
    miscellaneous: float


class TripPlan(BaseModel):
    trip_title: str
    summary: str
    total_estimated_cost: float
    transportation_tips: List[str]
    packing_list: List[str]
    budget_breakdown: BudgetBreakdown
    days: List[DayPlan]