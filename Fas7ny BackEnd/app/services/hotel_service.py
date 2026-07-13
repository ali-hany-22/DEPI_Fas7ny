from app.models.place import Place
from app.services.places_service import search_places_by_category


def get_hotels(city: str, limit: int = 3) -> tuple[Place]:
    """
    ترجع أفضل الفنادق في مدينة معينة.
    بتنادي الدالة العامة في places_service.py وممكن تضيف فلترة خاصة بالفنادق هنا لاحقاً
    (مثلاً استبعاد الفنادق اللي مالهاش صورة أو rating منخفض).
    """

    hotels = search_places_by_category(
        city=city,
        category="hotels",
        limit=limit
    )

    return hotels


def get_best_hotel(city: str) -> Place | None:
    """
    ترجع أفضل فندق واحد بس في المدينة (المستخدم في enrichment_service لكل يوم).
    """

    hotels = get_hotels(city=city, limit=1)

    if not hotels:
        return None

    return hotels[0]