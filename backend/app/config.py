from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Full URLs (used locally / docker-compose via DATABASE_URL and REDIS_URL)
    database_url: str = "postgresql+psycopg://postgres:postgres@127.0.0.1:5432/urlshortener"
    redis_url: str = "redis://127.0.0.1:6379/0"

    # Split components (injected by the ECS task definition). If present, they
    # take precedence over database_url / redis_url so the same image works in
    # local and in ECS without changes.
    db_host: str | None = None
    db_port: int = 5432
    db_name: str = "urlshortener"
    db_user: str = "urlshortener"
    db_password: str | None = None

    redis_host: str | None = None
    redis_port: int = 6379

    short_code_length: int = 6
    cache_ttl_seconds: int = 3600

    def model_post_init(self, _ctx: object) -> None:
        if self.db_host and self.db_password:
            self.database_url = (
                f"postgresql+psycopg://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        if self.redis_host:
            self.redis_url = f"redis://{self.redis_host}:{self.redis_port}/0"


settings = Settings()
