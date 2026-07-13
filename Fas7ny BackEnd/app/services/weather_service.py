import requests
from datetime import datetime, date as date_cls

from app.services.coordinates_service import get_coordinates

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

MAX_FORECAST_DAYS = 16

METEOCONS_BASE_URL = "https://cdn.jsdelivr.net/npm/@meteocons/svg/fill"

WEATHER_CODE_MAP = {
    0: {"text": "صافي", "icon": "clear-day"},
    1: {"text": "غائم جزئياً", "icon": "partly-cloudy-day"},
    2: {"text": "غائم جزئياً", "icon": "partly-cloudy-day"},
    3: {"text": "غائم", "icon": "cloudy"},
    45: {"text": "ضباب", "icon": "fog"},
    48: {"text": "ضباب كثيف", "icon": "fog"},
    51: {"text": "رذاذ خفيف", "icon": "drizzle"},
    53: {"text": "رذاذ", "icon": "drizzle"},
    55: {"text": "رذاذ كثيف", "icon": "drizzle"},
    61: {"text": "مطر خفيف", "icon": "rain"},
    63: {"text": "مطر", "icon": "rain"},
    65: {"text": "مطر غزير", "icon": "rain"},
    71: {"text": "ثلج خفيف", "icon": "snow"},
    73: {"text": "ثلج", "icon": "snow"},
    75: {"text": "ثلج كثيف", "icon": "snow"},
    80: {"text": "زخات مطر خفيفة", "icon": "rain"},
    81: {"text": "زخات مطر", "icon": "rain"},
    82: {"text": "زخات مطر غزيرة", "icon": "rain"},
    95: {"text": "عاصفة رعدية", "icon": "thunderstorms"},
}


def get_weather_info(code: int) -> dict:
    """
    تحويل Weather Code إلى وصف عربي + رابط الأيقونة.
    """

    info = WEATHER_CODE_MAP.get(
        code,
        {
            "text": "غير معروف",
            "icon": "not-available"
        }
    )

    return {
        "text": info["text"],
        "icon_url": f"{METEOCONS_BASE_URL}/{info['icon']}.svg"
    }


def get_weather(city: str, date: str) -> dict | None:
    """
    جلب حالة الطقس لمدينة وتاريخ معين.
    """

    try:
        requested_date = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()

        days_ahead = (
            requested_date - date_cls.today()
        ).days

        if days_ahead < 0 or days_ahead > MAX_FORECAST_DAYS:
            return None

    except ValueError:
        return None

    coords = get_coordinates(city)

    if coords is None:
        return None

    lat, lon = coords

    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "temperature_2m_mean,"
            "weathercode"
        ),
        "timezone": "auto",
        "start_date": date,
        "end_date": date
    }

    try:

        response = requests.get(
            FORECAST_URL,
            params=params,
            timeout=20
        )

        response.raise_for_status()

    except requests.RequestException:
        return None

    data = response.json()

    daily = data.get("daily")

    if not daily or not daily.get("time"):
        return None

    try:

        code = daily["weathercode"][0]

        weather = get_weather_info(code)

        return {
            "temperature": daily["temperature_2m_mean"][0],
            "max_temp": daily["temperature_2m_max"][0],
            "min_temp": daily["temperature_2m_min"][0],
            "condition": weather["text"],
            "icon": weather["icon_url"]
        }

    except (KeyError, IndexError):
        return None