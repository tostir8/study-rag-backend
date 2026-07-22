from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings.

    Values are automatically loaded from the .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # -------------------------
    # Application
    # -------------------------

    APP_NAME: str = "Study RAG Platform"

    # -------------------------
    # PostgreSQL
    # -------------------------

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # -------------------------
    # ChromaDB
    # -------------------------

    CHROMA_HOST: str
    CHROMA_PORT: int

    # -------------------------
    # AI Provider
    # -------------------------

    LLM_PROVIDER: str = "groq"

    GROQ_API_KEY: str

    LLM_MODEL: str = "llama-3.3-70b-versatile"

    LLM_TEMPERATURE: float = 0.2

    LLM_MAX_TOKENS: int = 2048

    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()
