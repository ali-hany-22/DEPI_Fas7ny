from app.models.place import Place
from app.services.places_service import search_places_by_category


def get_cafes(city: str, limit: int = 5) -> tuple[Place]:
    """ترجع أفضل الكافيهات في مدينة معينة."""

    return search_places_by_category(
        city=city,
        category="cafes",
        limit=limit
    )