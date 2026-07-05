from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    database_url: str = "postgresql+asyncpg://primer:primer_dev@localhost:5432/primer"
    redis_url: str = "redis://localhost:6379"
    gemini_api_key: str = ""


settings = Settings()
