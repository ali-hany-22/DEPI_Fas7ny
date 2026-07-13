from app.models.place import Place
from app.services.places_service import search_places_by_category


def get_museums(city: str, limit: int = 5) -> tuple[Place]:
    """ترجع أفضل المتاحف في مدينة معينة."""

    return search_places_by_category(
        city=city,
        category="museums",
        limit=limit
    )

def get_parks(city: str, limit: int = 5) -> tuple[Place]:
    """ترجع أفضل الحدائق العامة في مدينة معينة."""

    return search_places_by_category(
        city=city,
        category="parks",
        limit=limit
    )