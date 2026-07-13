from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Fas7ny AI Trip Planner"
    APP_VERSION: str = "1.0.0"

    GEMINI_API_KEY: str
    GEMINI_ALT_API_KEY: str
    GEMINI_ALT2_API_KEY: str
    GEMINI_MODEL: str = "gemini-3.5-flash"

    GOOGLE_MAPS_API_KEY: str
    UNSPLASH_ACCESS_KEY: str
    WEATHER_API_KEY: str
    GROQ_API_KEY: str

    # =========================
    # Provider Dashboard
    # =========================
    DATABASE_URL: str = "sqlite:///./rehla.db"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

settings = Settings()