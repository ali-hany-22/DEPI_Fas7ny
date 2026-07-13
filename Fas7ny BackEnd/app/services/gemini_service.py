import json
import logging
import time

from google import genai
from google.genai.types import GenerateContentConfig
from google.genai.errors import ServerError,ClientError
from groq import Groq
from groq import APIStatusError as GroqAPIStatusError
from pydantic import ValidationError

from app.core.config import settings
from app.models.response import TripPlan

logger = logging.getLogger("gemini_service")

GEMINI_KEYS = [
    settings.GEMINI_API_KEY,
    settings.GEMINI_ALT_API_KEY,
]

groq_client = Groq(
    api_key=settings.GROQ_API_KEY
)

GROQ_MODEL = "llama-3.3-70b-versatile"


class GeminiService:

    @staticmethod
    def generate(prompt: str, max_retries: int = 3) -> TripPlan:
        """
        بتنادي Gemini الأول. لو فشلت كل محاولات Gemini بسبب ServerError
        (زي 503 high demand)، بتعمل fallback تلقائي لـ Groq (Llama 3.3 70B)
        بدل ما الطلب يفشل بالكامل قدام المستخدم.

        لو الـ error من Gemini مش ServerError (زي مشكلة في الـ schema)،
        منعملش fallback خالص - بنرمي الـ error فورًا لأنها مش مشكلة
        توفر (availability) وغالبًا هتفشل في Groq كمان.
        """
        try:
            return GeminiService._generate_with_gemini(prompt, max_retries)

        except (ServerError, ClientError) as gemini_error:
            logger.warning(
                "Gemini exhausted all %s retries, falling back to Groq | last_error=%s",
                max_retries, str(gemini_error)
            )

            try:
                return GeminiService._generate_with_groq(prompt)
            except Exception as groq_error:
                logger.error(
                    "Groq fallback also failed | groq_error=%s | original_gemini_error=%s",
                    str(groq_error), str(gemini_error)
                )
                raise groq_error

    @staticmethod
    def _generate_with_gemini(prompt: str, max_retries: int) -> TripPlan:

        last_error = None

        for api_key in GEMINI_KEYS:

            if not api_key:
                continue

            client = genai.Client(api_key=api_key)

            logger.info("Trying Gemini API Key...")

            for attempt in range(max_retries):

                try:

                    response = client.models.generate_content(
                        model=settings.GEMINI_MODEL,
                        contents=prompt,
                        config=GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=TripPlan
                        )
                    )

                    logger.info(
                        "Gemini succeeded using current API key on attempt %s",
                        attempt + 1
                    )

                    return response.parsed

                except ClientError as e:

                    last_error = e

                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        logger.warning(
                            "Quota exceeded for current Gemini key. Trying next key..."
                        )
                        break

                    raise

                except ServerError as e:

                    last_error = e

                    logger.warning(
                        "Gemini ServerError attempt %s/%s",
                        attempt + 1,
                        max_retries
                    )

                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue

                    break

                except Exception as e:
                    logger.error(str(e))
                    raise

        raise last_error

    @staticmethod
    def _generate_with_groq(prompt: str) -> TripPlan:
        """
        Fallback على Groq (Llama 3.3 70B) لما Gemini يبقى مش متاح تمامًا.
        Groq مبيدعمش structured output بـ Pydantic model مباشر زي Gemini،
        فبنطلب JSON صريح في الـ prompt نفسه وبعدين نتحقق منه يدوياً.
        """
        schema_hint = json.dumps(TripPlan.model_json_schema(), ensure_ascii=False)

        groq_prompt = (
            f"{prompt}\n\n"
            "IMPORTANT: Respond with ONLY valid JSON matching this exact schema, "
            "no markdown, no code fences, no extra text before or after:\n"
            f"{schema_hint}"
        )

        completion = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": groq_prompt}],
            response_format={"type": "json_object"},
            temperature=0.4,
        )

        raw_content = completion.choices[0].message.content

        try:
            parsed_json = json.loads(raw_content)
            trip_plan = TripPlan(**parsed_json)
        except (json.JSONDecodeError, ValidationError) as e:
            logger.error("Groq returned invalid JSON/schema | error=%s", str(e))
            raise

        logger.info("Groq fallback generation succeeded")
        return trip_plan