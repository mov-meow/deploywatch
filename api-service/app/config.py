"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "DeployWatch API")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://devpulse:change-me@localhost:5432/devpulse",
    )
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
