from app.models.place import Place
from app.services.places_service import search_places_by_category


def get_beaches(city: str, limit: int = 5) -> tuple[Place]:
    """ترجع أفضل الشواطئ في مدينة معينة (مفيد للمدن الساحلية بس)."""

    return search_places_by_category(
        city=city,
        category="beaches",
        limit=limit
    )