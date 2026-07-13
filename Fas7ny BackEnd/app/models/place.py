from pydantic import BaseModel


class Place(BaseModel):

    name: str
    address: str

    city: str | None = None
    country: str | None = None

    # هنملاهم بعدين من Gemini
    rating: float | None = None
    reviews: int | None = None

    popularity_score: int = 0
    popularity: str = "Low"

    latitude: float
    longitude: float

    google_maps: str

    image_url: str | None = None
    place_id: str | None = None