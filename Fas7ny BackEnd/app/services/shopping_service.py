from app.models.place import Place
from app.services.places_service import search_places_by_category


def get_shopping(city: str, limit: int = 5) -> tuple[Place]:
    """ترجع أماكن التسوق في مدينة معينة (مولات، أسواق...)."""

    return search_places_by_category(
        city=city,
        category="shopping",
        limit=limit
    )