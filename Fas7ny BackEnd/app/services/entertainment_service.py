from app.models.place import Place
from app.services.places_service import search_places_by_category


def get_entertainment(city: str, limit: int = 5) -> tuple[Place]:
    """ترجع أماكن الترفيه في مدينة معينة (ملاهي، سينمات، ملاهي مائية...)."""

    return search_places_by_category(
        city=city,
        category="entertainment",
        limit=limit
    )