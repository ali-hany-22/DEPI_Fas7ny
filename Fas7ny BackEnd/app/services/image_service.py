import requests

from app.core.config import settings

UNSPLASH_URL = "https://api.unsplash.com/search/photos"


def get_place_image(place_name: str, city: str | None = None) -> str | None:
    """
    Return a representative image URL from Unsplash.

    Search order:
    1- Place + City + Egypt
    2- Place + Egypt
    3- Place
    4- City
    """

    queries = []

    if city:
        queries.append(f"{place_name} {city} Egypt")

    queries.append(f"{place_name} Egypt")
    queries.append(place_name)

    if city:
        queries.append(city)

    headers = {
        "Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"
    }

    for query in queries:

        try:
            response = requests.get(
                UNSPLASH_URL,
                headers=headers,
                params={
                    "query": query,
                    "per_page": 1,
                    "orientation": "landscape"
                },
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            results = data.get("results", [])

            if results:
                return results[0]["urls"]["regular"]

        except requests.RequestException:
            continue

    return None