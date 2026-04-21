from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://postgres:jero1123@127.0.0.1:5432/urlshortener"
    redis_url: str = "redis://127.0.0.1:6379/0"
    short_code_length: int = 6
    cache_ttl_seconds: int = 3600


settings = Settings()
