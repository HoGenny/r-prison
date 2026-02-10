from functools import lru_cache

from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    jwt_secret: str
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as exc:
        keys = [".".join(str(part) for part in err["loc"]) for err in exc.errors()]
        message = "Missing or invalid environment variables: " + ", ".join(sorted(set(keys)))
        raise RuntimeError(message) from exc


settings = get_settings()
