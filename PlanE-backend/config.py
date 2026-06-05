from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "PitWall F1 Telemetry API"
    api_prefix: str = "/api"
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])

    # Environment: "development" or "production"
    environment: str = "development"

    database_url: str = "sqlite:///./pitwall.db"
    redis_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = ""

    telemetry_data_dir: Path = Path("./data/telemetry")
    fastf1_cache_dir: Path = Path("./data/fastf1-cache")
    reports_dir: Path = Path("./data/reports")

    use_live_data: bool = True
    openf1_base_url: str = "https://api.openf1.org/v1"
    ergast_base_url: str = "https://api.jolpi.ca/ergast/f1"

    distance_samples: int = 1000
    ensemble_min_laps: int = 3
    ensemble_max_laps: int = 5
    insight_consistency_threshold: float = 0.60

    # If True, disable the in-process preloader loop (saves memory on constrained hosts)
    disable_preloader: bool = False

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def effective_celery_backend(self) -> str:
        """Return the Celery result backend URL, defaulting to redis_url db 1."""
        if self.celery_result_backend:
            return self.celery_result_backend
        # Derive from redis_url: replace trailing /0 with /1
        base = self.redis_url.rsplit("/", 1)[0]
        return f"{base}/1"

    @property
    def redis_is_localhost(self) -> bool:
        return "localhost" in self.redis_url or "127.0.0.1" in self.redis_url

    def validate_production(self) -> None:
        """Log warnings for misconfigurations. Fatal errors raise."""
        if self.is_production and self.redis_is_localhost:
            logger.warning(
                "REDIS_URL points to localhost in production — Celery will be unavailable. "
                "Analysis will run in background threads (high memory risk on small instances)."
            )
        if self.is_production:
            logger.info(
                "Production mode — environment=%s, redis_localhost=%s, preloader_disabled=%s",
                self.environment, self.redis_is_localhost, self.disable_preloader or self.is_production,
            )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.telemetry_data_dir.mkdir(parents=True, exist_ok=True)
    settings.fastf1_cache_dir.mkdir(parents=True, exist_ok=True)
    settings.reports_dir.mkdir(parents=True, exist_ok=True)
    return settings
