import logging
import time

import requests

from app.models.place import Place

logger = logging.getLogger("osm_fallback_service")

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"

# Nominatim بيشترط User-Agent واضح فيه معلومات تواصل، وإلا ممكن يمنعك (Policy).
# غيّر الإيميل ده لإيميلك الحقيقي أو دومين المشروع.
HEADERS = {
    "User-Agent": "Rehla-TripPlanner/1.0 (contact: your-email@example.com)"
}

# Nominatim rate limit صارم: 1 request/second بالظبط. لازم نلتزم بيه.
_last_request_time = 0.0
_MIN_INTERVAL = 1.1  # ثانية، هامش أمان بسيط فوق الـ 1 ثانية المطلوبة


def _respect_rate_limit():
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < _MIN_INTERVAL:
        time.sleep(_MIN_INTERVAL - elapsed)
    _last_request_time = time.time()


def search_place_osm(place_name: str, city: str | None = None) -> Place | None:
    """
    Fallback لما Google Places يفشل (429 quota / 500 server error).
    بيستخدم Nominatim (OpenStreetMap) عشان يجيب مكان بديل، حتى لو بيانات أقل تفصيلاً
    (مفيش rating حقيقي، مفيش reviews، مفيش صور من جوجل).
    ده أفضل من إن الرحلة تطلع بمكان فاضي (place_details = None) تمامًا.
    """

    if not place_name or not place_name.strip():
        return None

    query = f"{place_name}, {city}, Egypt" if city else f"{place_name}, Egypt"

    params = {
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "addressdetails": 1,
    }

    _respect_rate_limit()

    try:
        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=HEADERS,
            timeout=15,
        )
        response.raise_for_status()

    except requests.RequestException as e:
        logger.error("OSM fallback request failed | query=%s | error=%s", query, str(e))
        return None

    try:
        results = response.json()
    except ValueError:
        logger.error("OSM fallback: failed to parse JSON | query=%s", query)
        return None

    if not results:
        logger.info("OSM fallback: no results | query=%s", query)
        return None

    result = results[0]

    try:
        address = result.get("display_name", "")
        lat = float(result["lat"])
        lon = float(result["lon"])

        address_details = result.get("address", {})
        resolved_city = (
            address_details.get("city")
            or address_details.get("town")
            or address_details.get("state")
            or city
        )

        logger.info("OSM fallback SUCCESS | query=%s", query)

        return Place(
            name=place_name,
            address=address,
            city=resolved_city,
            country=address_details.get("country", "Egypt"),
            place_id=f"osm_{result.get('osm_id', '')}",
            # مفيش rating/reviews حقيقية من OSM، فبنحطها صفر بدل ما نختلق أرقام
            rating=0,
            reviews=0,
            latitude=lat,
            longitude=lon,
            google_maps=f"https://www.google.com/maps/search/?api=1&query={lat},{lon}",
            image_url="https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg",
        )

    except (KeyError, TypeError, ValueError) as e:
        logger.error("OSM fallback: malformed result | query=%s | error=%s", query, str(e))
        return None