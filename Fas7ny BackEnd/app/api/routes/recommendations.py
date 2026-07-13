import logging

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from app.services.persistent_cache import get_cached, set_cached
from app.services.recommendation_config import RecommendationConfig

from app.services.hotel_service import get_hotels
from app.services.restaurants_service import get_restaurants
from app.services.cafe_service import get_cafes
from app.services.entertainment_service import get_entertainment
from app.services.shopping_service import get_shopping
from app.services.beach_service import get_beaches
from app.services.attraction_service import get_museums, get_parks

logger = logging.getLogger("recommendations_api")

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

ALL_FETCHERS = {
    "hotels": get_hotels,
    "restaurants": get_restaurants,
    "cafes": get_cafes,
    "entertainment": get_entertainment,
    "shopping": get_shopping,
    "museums": get_museums,
    "parks": get_parks,
    "beaches": get_beaches,
}


class RecommendationResponse(BaseModel):
    city: str
    category: str
    results: list


def _safe_call(label: str, fn, *args, **kwargs) -> list:
    try:
        result = fn(*args, **kwargs)
        return [item.model_dump() for item in result]
    except Exception as e:
        logger.error("Failed to fetch %s | error=%s", label, str(e))
        return []


def _fetch_category(label: str, fn, city: str, limit: int) -> list:
    cached = get_cached(city, label)

    if cached is not None:
        return cached[:limit]

    hard_caps = RecommendationConfig.get_hard_caps()
    fetch_limit = hard_caps[label]

    result = _safe_call(label, fn, city, fetch_limit)

    set_cached(city, label, result)

    return result[:limit]


@router.get("", response_model=RecommendationResponse)
def get_recommendations(
    city: str = Query(..., description="Egyptian city name"),
    category: str = Query(
        ...,
        description="One of: hotels, restaurants, cafes, entertainment, "
                     "shopping, museums, parks, beaches",
    ),
    limit: int = Query(5, ge=1, le=20),
):
    """
    On-demand recommendations for a single category in a single city.
    Used by the frontend when the user explicitly asks to see e.g.
    'restaurants near me' instead of pre-fetching everything at trip
    generation time.
    """

    category = category.lower().strip()

    if category not in ALL_FETCHERS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown category '{category}'. "
                   f"Valid categories: {sorted(ALL_FETCHERS.keys())}",
        )

    fn = ALL_FETCHERS[category]

    results = _fetch_category(category, fn, city, limit)

    return RecommendationResponse(
        city=city,
        category=category,
        results=results,
    )


@router.get("/all", response_model=dict[str, list])
def get_all_recommendations(
    city: str = Query(..., description="Egyptian city name"),
    interests: list[str] = Query(default=[]),
    trip_type: str | None = Query(default=None),
    days: int = Query(default=1, ge=1, le=30),
):
    """
    Optional bulk endpoint: returns recommendations for all categories
    relevant to the given interests/trip_type in one call. Useful for a
    'nearby recommendations' screen instead of calling /recommendations
    once per category.
    """

    categories = RecommendationConfig.get_categories(interests)
    limits = RecommendationConfig.get_limits(
        days=days,
        interests=interests,
        trip_type=trip_type,
    )

    output: dict[str, list] = {}

    for label in categories:
        fn = ALL_FETCHERS[label]
        output[label] = _fetch_category(label, fn, city, limits[label])

    return output