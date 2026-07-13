from app.models.place import Place
from app.services.places_service import search_places_by_category


def get_restaurants(city: str, limit: int = 6) -> tuple[Place]:
    """
    ترجع أفضل المطاعم في مدينة معينة.
    limit أعلى شوية من الفندق لأن الرحلة الطويلة محتاجة اختيارات متنوعة كل يوم.
    """

    return search_places_by_category(
        city=city,
        category="restaurants",
        limit=limit
    )