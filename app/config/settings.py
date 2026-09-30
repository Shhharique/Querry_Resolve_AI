from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# ResolveAI project root
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    database_url: str
    redis_url: str

    app_env: str = "development"
    log_level: str = "INFO"

    anthropic_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()