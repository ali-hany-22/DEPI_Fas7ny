import requests

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def get_coordinates(city: str) -> tuple[float, float] | None:

    params = {
        "name": city,
        "count": 1,
        "format": "json"
    }

    try:
        response = requests.get(
            GEOCODING_URL,
            params=params,
            timeout=20
        )
        response.raise_for_status()

    except requests.RequestException:
        return None

    results = response.json().get("results")

    if not results:
        return None

    return (
        results[0]["latitude"],
        results[0]["longitude"]
    )