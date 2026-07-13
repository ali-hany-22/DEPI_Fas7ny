from app.prompts.trip_prompt import build_trip_prompt
from app.services.gemini_service import GeminiService
from app.services.enrichment_service import enrich_trip


def generate_trip(request_data: dict):

    prompt = build_trip_prompt(request_data)

    trip = GeminiService.generate(prompt)

    if trip is None:
        raise Exception("Failed to generate trip.")

    trip_dict = trip.model_dump(exclude_none=True)

    enriched_trip = enrich_trip(
        trip=trip_dict,
        start_date=request_data.get("start_date")
    )

    return enriched_trip